from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from database import get_all_tasks, insert_task, mark_task_completed, init_db
from contextlib import asynccontextmanager

class Task(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=2000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {'message': 'Welcome to the task tracker!'}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/about")
def about():
    return {"app": "HSE Task Tracker", "version": "0.1.0", "description": "A simple task tracking application."}

@app.get("/tasks")
def get_tasks():
    return get_all_tasks()

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    new_task = {"title": task.title, "description": task.description, "completed": False}
    return insert_task(task.title, task.description)

@app.patch("/tasks/{task_id}")
def complete_task(task_id: int):
    marked_task = mark_task_completed(task_id)
    if marked_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return marked_task
   