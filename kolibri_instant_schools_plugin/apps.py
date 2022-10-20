from django.apps import AppConfig
from datetime import timedelta

from kolibri.utils.time_utils import local_now
from kolibri.core.tasks.main import scheduler

from .tasks import SCH_ANONYMIZE_JOB_ID
from .tasks import SCH_REQUEUE_FAILED_USER_JOB_ID


class KolibriInstantSchoolsConfig(AppConfig):
    name = "kolibri_instant_schools_plugin"

    def ready(self):
        """
        When the app starts, set a daily run starting now cleaning up completed jobs removing their user data;
        then setup for 24 hours from now to start running the requeuing of failed attempts, if any
        """
        in_an_hour = local_now() + timedelta(hours=1)
        and_a_day = in_an_hour + timedelta(days=1)

        if SCH_ANONYMIZE_JOB_ID not in scheduler:
            from .tasks import anonymize_compeleted_user_posts
            anonymize_compeleted_user_posts.enqueue_at(
                in_an_hour, interval=24 * 60 * 60, repeat=None
            )
        if SCH_REQUEUE_FAILED_USER_JOB_ID not in scheduler:
            from .tasks import requeue_failed_user_data_requests
            requeue_failed_user_data_requests.enqueue_at(
                and_a_day, interval=24 * 60 * 60, repeat=None
            )
