class InstantSchoolsRouter(object):
    """
    A router to ensure queries to Instant Schools plugin models use the correct database.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "kolibri_instant_schools_plugin":
            return 'instant_schools'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "kolibri_instant_schools_plugin":
            return 'instant_schools'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "kolibri_instant_schools_plugin" and \
           obj2._meta.app_label == "kolibri_instant_schools_plugin":
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'instant_schools':
            return app_label == "kolibri_instant_schools_plugin"
        return None