import hashlib
import warnings

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from kolibri.auth.constants.role_kinds import ADMIN
from kolibri.auth.constants.facility_presets import mappings
from kolibri.auth.models import Facility, FacilityUser, Role
from kolibri.core.device.models import DevicePermissions, DeviceSettings
from kolibri.logger.models import ContentSummaryLog, ContentSessionLog, MasteryLog, UserSessionLog, AttemptLog
from ...models import PhoneToUsernameMapping

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

USER_ID_MAPPING = {}
SUMMARYLOG_ID_MAPPING = {}
MASTERYLOG_ID_MAPPING = {}
SESSIONLOG_ID_MAPPING = {}

class Command(BaseCommand):
    help = "Migrate data from the old Instant Schools v1 database into the v2 database."

    requires_system_checks = False

    def handle(self, *args, **options):

        # ensure the new databases have both been migrated
        call_command("migrate")
        call_command("migrate", database="instant_schools")

        # load the old databases
        old_db_session, old_classes = self.load_database(settings.OLD_DB_PATH)
        old_hash_db_session, old_hash_classes = self.load_database(settings.OLD_HASH_DB_PATH)

        # load the SQLAlchemy ORM classes for the old databases
        Collection_ = old_classes.kolibriauth_collection
        DeviceOwner_ = old_classes.kolibriauth_deviceowner
        FacilityUser_ = old_classes.kolibriauth_facilityuser
        ContentSummaryLog_ = old_classes.logger_contentsummarylog
        ContentSessionLog_ = old_classes.logger_contentsessionlog
        AttemptLog_ = old_classes.logger_attemptlog
        MasteryLog_ = old_classes.logger_masterylog
        UserSessionLog_ = old_classes.logger_usersessionlog

        # try to load the phone hashing lookup table, if it exists
        try:
            Lookup_ = old_hash_classes.lookup
        except AttributeError:
            Lookup_ = None

        # MIGRATE: Facility
        old_facility = old_db_session.query(Collection_).filter(Collection_.kind == "facility")[0]
        new_facility, _ = Facility.objects.get_or_create(name=old_facility.name)
        new_facility.dataset.preset = "nonformal"
        new_facility.dataset.learner_can_edit_username = False
        new_facility.dataset.save()

        # MIGRATE: DeviceOwner
        for deviceowner in old_db_session.query(DeviceOwner_).all():
            superuser, _ = FacilityUser.objects.get_or_create(
                username=deviceowner.username,
                full_name=deviceowner.full_name,
                password=deviceowner.password,
                date_joined=deviceowner.date_joined,
                last_login=deviceowner.last_login,
                facility=new_facility,
            )
            Role.objects.get_or_create(user=superuser, collection=new_facility, kind=ADMIN)
            DevicePermissions.objects.get_or_create(user=superuser, is_superuser=True)

        # MIGRATE: FacilityUser
        for old_user in old_db_session.query(FacilityUser_).all():

            # migrate the phone number mapping
            old_username = old_user.username
            if len(old_username) == 30:
                # skip the user if we don't have the lookup table, as we can't get their phone number
                if Lookup_ is None:
                    continue
                phonenumber = old_hash_db_session.query(Lookup_).filter(Lookup_.hashval == old_username).first().phone
            else:
                phonenumber = old_username
                old_username = hashlib.md5(phonenumber).hexdigest()[:30]

            PhoneToUsernameMapping.objects.get_or_create(username=old_username, phone=phonenumber)

            new_user, _ = FacilityUser.objects.get_or_create(
                username=old_username,
                full_name=old_user.full_name,
                password=old_user.password,
                date_joined=old_user.date_joined,
                last_login=old_user.last_login,
                facility=new_facility,
            )
            USER_ID_MAPPING[old_user.id] = new_user.id

        # MIGRATE: ContentSummaryLog
        for old_log in old_db_session.query(ContentSummaryLog_).all():
            if old_log.user_id not in USER_ID_MAPPING:
                continue
            new_log, _ = ContentSummaryLog.objects.get_or_create(
                user_id=USER_ID_MAPPING[old_log.user_id],
                content_id=old_log.content_id,
                channel_id=old_log.channel_id,
                start_timestamp=old_log.start_timestamp,
                end_timestamp=old_log.end_timestamp,
                completion_timestamp=old_log.completion_timestamp,
                time_spent=old_log.time_spent,
                progress=old_log.progress,
                kind=old_log.kind,
                extra_fields=old_log.extra_fields,
            )
            SUMMARYLOG_ID_MAPPING[old_log.id] = new_log.id

        # MIGRATE: ContentSessionLog
        for old_log in old_db_session.query(ContentSessionLog_).all():
            if old_log.user_id not in USER_ID_MAPPING:
                continue
            new_log, _ = ContentSessionLog.objects.get_or_create(
                user_id=USER_ID_MAPPING[old_log.user_id],
                content_id=old_log.content_id,
                channel_id=old_log.channel_id,
                start_timestamp=old_log.start_timestamp,
                end_timestamp=old_log.end_timestamp,
                time_spent=old_log.time_spent,
                progress=old_log.progress,
                kind=old_log.kind,
                extra_fields=old_log.extra_fields,
            )
            SESSIONLOG_ID_MAPPING[old_log.id] = new_log.id

        # MIGRATE: UserSessionLog
        for old_log in old_db_session.query(UserSessionLog_).all():
            if old_log.user_id not in USER_ID_MAPPING:
                continue
            new_log, _ = UserSessionLog.objects.get_or_create(
                user_id=USER_ID_MAPPING[old_log.user_id],
                channels=old_log.channels,
                start_timestamp=old_log.start_timestamp,
                last_interaction_timestamp=old_log.last_interaction_timestamp,
                pages=old_log.pages,
            )

        # MIGRATE: MasteryLog
        for old_log in old_db_session.query(MasteryLog_).all():
            if old_log.summarylog_id not in SUMMARYLOG_ID_MAPPING:
                continue
            summarylog = ContentSummaryLog.objects.get(id=SUMMARYLOG_ID_MAPPING[old_log.summarylog_id])
            new_log, _ = MasteryLog.objects.get_or_create(
                user_id=summarylog.user_id,
                summarylog_id=summarylog.id,
                mastery_criterion=old_log.mastery_criterion,
                start_timestamp=old_log.start_timestamp,
                end_timestamp=old_log.end_timestamp,
                completion_timestamp=old_log.completion_timestamp,
                mastery_level=old_log.mastery_level,
                complete=old_log.complete,
            )
            MASTERYLOG_ID_MAPPING[old_log.id] = new_log.id

        # MIGRATE: AttemptLog
        for old_log in old_db_session.query(AttemptLog_).all():
            if old_log.masterylog_id not in MASTERYLOG_ID_MAPPING or old_log.sessionlog_id not in SESSIONLOG_ID_MAPPING:
                continue
            sessionlog = ContentSessionLog.objects.get(id=SESSIONLOG_ID_MAPPING[old_log.sessionlog_id])
            new_log, _ = AttemptLog.objects.get_or_create(
                user_id=sessionlog.user_id,
                item=old_log.item,
                start_timestamp=old_log.start_timestamp,
                end_timestamp=old_log.end_timestamp,
                completion_timestamp=old_log.completion_timestamp,
                time_spent=old_log.time_spent,
                complete=old_log.complete,
                correct=old_log.correct,
                hinted=old_log.hinted,
                answer=old_log.answer,
                simple_answer=old_log.simple_answer,
                interaction_history=old_log.interaction_history,
                masterylog_id=MASTERYLOG_ID_MAPPING[old_log.masterylog_id],
                sessionlog_id=sessionlog.id,
            )

        # CREATE: DeviceSettings
        device_settings, _ = DeviceSettings.objects.get_or_create()
        device_settings.is_provisioned = True
        device_settings.save()

        self.stdout.write(self.style.SUCCESS(
            "Database has been successfully migrated! You may now start the server."
        ))

    def load_database(self, path):

        engine = create_engine("sqlite:///" + path, convert_unicode=True)

        Base = automap_base()

        Base.prepare(engine, reflect=True)

        session = sessionmaker(bind=engine, autoflush=False)()

        return session, Base.classes