from fastapi import APIRouter
import threading
from compute_modules.task_generator_module import generate_task_thread, grammar_tasks, event

router = APIRouter()


@router.on_event("startup")
async def startup_event():
    event.set()
    threading.Thread(target=generate_task_thread).start()


@router.get("/get-new-task/")
async def retrieve_task_from_queue():
    task = grammar_tasks.get(block=True)
    if task:
        event.set()
    return task
