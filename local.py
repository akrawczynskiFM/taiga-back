# -*- coding: utf-8 -*-
import os
from .common import * # noqa

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = False
PUBLIC_REGISTER_ENABLED = False  # możesz zmienić na True

# Domeny
SITES["front"]["scheme"] = os.getenv("TAIGA_SCHEME", "https")
SITES["front"]["domain"] = os.environ.get("TAIGA_DOMAIN", "localhost")

# Baza (Cloud SQL via unix socket)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "taiga"),
        "USER": os.getenv("POSTGRES_USER", "taiga"),
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        # Usunięcie pola HOST i dodanie OPTIONS dla gniazda unix
        "HOST": "", # pole HOST musi być puste!
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "disable",
            "sslrootcert": None,
            "sslcert": None,
            "sslkey": None,
            "ssl_ca": None,
            "ssl_cert": None,
            "ssl_key": None,
            "connect_timeout": 10,
            "sslcompression": 1,
            "ssl_min_version": "TLSv1.2",
            "ssl_max_version": "TLSv1.3",
            "options": f"-c cloudsql.instance={os.getenv('INSTANCE_CONNECTION_NAME')}"
        }
    }
}
# Dodatkowo, jeśli używasz `INSTANCE_CONNECTION_NAME` w swoim skrypcie,
# możesz przekazać go jako zmienną środowiskową do kontenera.
# Poniższa linia nie jest wymagana w pliku local.py, ale ilustruje, jak to zrobić.
# INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")

# Media i pliki statyczne
MEDIA_URL = f"{SITES['front']['scheme']}://{SITES['front']['domain']}/media/"
STATIC_URL = f"{SITES['front']['scheme']}://{SITES['front']['domain']}/static/"

# E-mail (opcjonalnie)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@localhost")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# (pełny wariant) RabbitMQ do realtime
if os.getenv("AMQP_URL"):
    EVENTS_PUSH_BACKEND = "taiga.events.backends.rabbitmq.EventsPushBackend"
    EVENTS_PUSH_BACKEND_OPTIONS = {"url": os.environ["AMQP_URL"]}
