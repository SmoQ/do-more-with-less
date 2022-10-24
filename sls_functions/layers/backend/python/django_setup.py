try:
    import unzip_requirements  # noqa: F401
except (ImportError, FileNotFoundError):
    pass
import os

from django import setup as django_setup
from django.conf import settings
from do_more_with_less import settings as web_api_settings

if not settings.configured:
    INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.auth", "todo"]
    SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
    attributes = {
        attr_name: getattr(web_api_settings, attr_name)
        for attr_name in dir(web_api_settings)
        if attr_name.isupper()
    }
    settings.configure(
        **{
            **attributes,
            "USE_TZ": True,
            "DEBUG": False,
            "LOCAL": os.getenv("IS_OFFLINE") or False,
            "INSTALLED_APPS": INSTALLED_APPS,
        }
    )
    django_setup()
