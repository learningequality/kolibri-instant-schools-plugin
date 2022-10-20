import logging
import os
import requests

from kolibri.core.tasks.decorators import register_task
from kolibri.core.tasks.job import State
from kolibri.core.tasks.main import job_storage

USER_DATA_POST_FUNC = "kolibri_instant_schools_plugin.auth.api.send_user_data_to_opco"


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

@register_task()
def send_user_data_to_opco(raw_user_data, **kwargs):
    url = os.environ.get("POST_USER_URL", None)
    if url:
        requests.post(url, data=raw_user_data).raise_for_status()
    else:
        logging.warn(
            "No URL set to post data. If you are expecting to send data to the OpCos,\
                      you should set POST_USER_URL and restart the server. After a week \
                      failures the data will be anonymized and it will be lost permanently"
        )
        