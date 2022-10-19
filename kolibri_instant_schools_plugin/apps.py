from django.apps import AppConfig
from kolibri.core.tasks.decorators import register_task
from kolibri.core.tasks.job import State
from kolibri.core.tasks.main import job_storage
from kolibri.utils.time_utils import local_now

USER_DATA_POST_FUNC = "kolibri_instant_schools_plugin.auth.api.send_user_data_to_opco"


@register_task()
def requeue_failed_user_data_requests():
    """
    Requeues failed jobs that tried to post user data
    """
    failed_user_data_jobs = [
        job
        for job in job_storage.get_all_jobs()
        if (job.state == State.FAILED and job.func == USER_DATA_POST_FUNC)
    ]

    for failed_job in failed_user_data_jobs:
        _failure_count = failed_job.args[0].get("failures_count")

        # We'll complete this job and start a new one with the same data
        failed_job.storage.complete_job(failed_job.job_id, result="Restarted")

        if _failure_count >= 7:
            # If we've failed more than 7 times just let it get cleaned up when the
            # anonymize_completed_user_posts job is run next
            # This effectively means:
            # - We keep user data raw in the DB for up to 8 days
            # - We have 7 days to identify any errors on FAILED state jobs and not
            #   lose the raw data to the anonymization job
            return
        else:
            failed_job.args[0]["failures_count"] = _failure_count + 1
            failed_job.storage.enqueue_job(failed_job, None)


@register_task()
def anonymize_compeleted_user_posts():
    """
    For any jobs that are completed, anonymize the data.
    Note that jobs will not be "COMPLETE" until they've failed 7 times
    or until it actually completed properly
    """
    completed_user_data_requests = [
        job
        for job in job_storage.get_all_jobs()
        if (job.state == State.COMPLETED and job.func == USER_DATA_POST_FUNC)
    ]
    for job in completed_user_data_requests:
        # Clear the args and kwargs that we don't want to keep forever
        del job.args[0]["phone"]
        del job.args[0]["full_name"]
        del job.args[0]["birth_year"]
        del job.args[0]["gender"]

        # Update the job and pass new args so that they're updated
        # business needed to save to the DB the updated args
        job.storage._update_job(
            job.job_id,
            state=State.COMPLETED,
            result="Completed and anonymized",
            args=job.args,
        )


class KolibriCoreConfig(AppConfig):
    name = "kolibri_instant_schools_plugin"

    def ready(self):
        """
        When the app starts, set a daily run starting now cleaning up completed jobs removing their user data;
        then setup for 24 hours from now to start running the requeuing of failed attempts, if any
        """
        start_time = local_now()
        anonymize_compeleted_user_posts.enqueue_at(
            start_time, interval=24 * 60 * 60, repeat=None
        )
        requeue_failed_user_data_requests.enqueue_at(
            start_time.timedelta(days=1), interval=24 * 60 * 60, repeat=None
        )
