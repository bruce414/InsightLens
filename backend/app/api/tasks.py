from celery.result import AsyncResult
from fastapi import APIRouter

from app.core.celery_app import celery_app
from app.tasks.demo_tasks import long_running_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/demo")
def create_demo_task(seconds: int = 5):
    task = long_running_task.delay(seconds)

    return {
        "task_id": task.id,
        "status": "queued",
    }


@router.get("/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }