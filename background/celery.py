from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready

from core.config import settings

app = Celery(__name__, broker=settings.celery.broker, backend=settings.celery.backend)
app.autodiscover_tasks(['background.tasks'])


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    from background.tasks import update_menus

    sender.add_periodic_task(
        crontab(minute='*/1'), update_menus.s(), name='update_menus'
    )


@worker_ready.connect
def at_start(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task('update_menus', connection=conn)
