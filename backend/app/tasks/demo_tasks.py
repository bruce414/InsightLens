import time
from typing import cast

from celery.app.task import Task

from app.core.celery_app import celery_app


@celery_app.task(name="demo.long_running_task")
def _long_running_task(seconds: int = 5) -> dict:
    time.sleep(seconds)

    return {
        "status": "completed",
        "message": f"Task finished after {seconds} seconds.",
    }


long_running_task: Task = cast(Task, _long_running_task)