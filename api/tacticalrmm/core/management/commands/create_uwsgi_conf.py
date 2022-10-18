import configparser
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate conf for uwsgi"

    def handle(self, *args, **kwargs):

        self.stdout.write("Creating uwsgi conf...")

        config = configparser.ConfigParser()

        if getattr(settings, "DOCKER_BUILD", False):
            home = str(Path(os.getenv("VIRTUAL_ENV")))  # type: ignore
            socket = "0.0.0.0:8080"
        else:
            home = str(settings.BASE_DIR.parents[0] / "env")
            socket = str(settings.BASE_DIR / "tacticalrmm.sock")

        config["uwsgi"] = {
            "chdir": str(settings.BASE_DIR),
            "module": "tacticalrmm.wsgi",
            "home": home,
            "master": str(getattr(settings, "UWSGI_MASTER", True)).lower(),
            "enable-threads": str(
                getattr(settings, "UWSGI_ENABLE_THREADS", True)
            ).lower(),
            "socket": socket,
            "harakiri": str(getattr(settings, "UWSGI_HARAKIRI", 300)),
            "chmod-socket": str(getattr(settings, "UWSGI_CHMOD_SOCKET", 660)),
            "buffer-size": str(getattr(settings, "UWSGI_BUFFER_SIZE", 65535)),
            "vacuum": str(getattr(settings, "UWSGI_VACUUM", True)).lower(),
            "die-on-term": str(getattr(settings, "UWSGI_DIE_ON_TERM", True)).lower(),
            "max-requests": str(getattr(settings, "UWSGI_MAX_REQUESTS", 500)),
            "disable-logging": str(
                getattr(settings, "UWSGI_DISABLE_LOGGING", True)
            ).lower(),
            "cheaper-algo": "busyness",
            "cheaper": str(getattr(settings, "UWSGI_CHEAPER", 4)),
            "cheaper-initial": str(getattr(settings, "UWSGI_CHEAPER_INITIAL", 4)),
            "workers": str(getattr(settings, "UWSGI_MAX_WORKERS", 40)),
            "cheaper-step": str(getattr(settings, "UWSGI_CHEAPER_STEP", 2)),
            "cheaper-overload": str(getattr(settings, "UWSGI_CHEAPER_OVERLOAD", 3)),
            "cheaper-busyness-min": str(getattr(settings, "UWSGI_BUSYNESS_MIN", 5)),
            "cheaper-busyness-max": str(getattr(settings, "UWSGI_BUSYNESS_MAX", 10)),
        }

        if getattr(settings, "UWSGI_DEBUG", False):
            config["uwsgi"]["stats"] = "/tmp/stats.socket"
            config["uwsgi"]["cheaper-busyness-verbose"] = str(True).lower()

        with open(settings.BASE_DIR / "app.ini", "w") as fp:
            config.write(fp)

        self.stdout.write("Created uwsgi conf")
