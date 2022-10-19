from django.apps import AppConfig
from datetime import timedelta
from kolibri.core.tasks.decorators import register_task
from kolibri.core.tasks.job import State
from kolibri.core.tasks.main import job_storage
from kolibri.utils.time_utils import local_now

USER_DATA_POST_FUNC = "kolibri_instant_schools_plugin.auth.api.send_user_data_to_opco"



class KolibriInstantSchoolsConfig(AppConfig):
    name = "kolibri_instant_schools_plugin"

    def ready(self):
        @register_task()
        def requeue_failed_user_data_requests():
            """
            Requeues failed jobs that tried to post user data and bumps their failure_
            count
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
                # Remove these PII items from the job if they're set on it
                for pii in ["phone", "full_name", "birth_year", "gender"]:
                    if pii in job.args[0]:
                        del job.args[0][pii]

                # Update the job and pass the newly updated args to it
                job.storage._update_job(
                    job.job_id,
                    state=State.COMPLETED,
                    result="Completed and anonymized",
                    args=job.args,
                )
        """
        When the app starts, set a daily run starting now cleaning up completed jobs removing their user data;
        then setup for 24 hours from now to start running the requeuing of failed attempts, if any
        """
        in_an_hour = local_now() + timedelta(hours=1)
        and_a_day = in_an_hour + timedelta(days=1)

        anonymize_compeleted_user_posts.enqueue_at(
            in_an_hour, interval=24 * 60 * 60, repeat=None
        )

        requeue_failed_user_data_requests.enqueue_at(
            and_a_day, interval=24 * 60 * 60, repeat=None
        )
