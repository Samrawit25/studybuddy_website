from django.apps import AppConfig


class StudybuddyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studybuddy'

    def ready(self):
        import studybuddy.signals
