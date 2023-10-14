from app.settings import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "thss",
        "USER": "root",
        "PASSWORD": "2020012385",
        "HOST": "mysql",
        "PORT": "3306",
    }
}
