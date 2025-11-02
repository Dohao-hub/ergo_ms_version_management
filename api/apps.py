from django.apps import AppConfig

class VersionManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.version_management.api'
    label = 'version_management'