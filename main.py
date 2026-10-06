from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class Task(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=2000)

app = FastAPI()

@app.get("/")
async def read_root():
    return {'message': 'Welcome to the task tracker!'}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/about")
def about():
    return {"app": "HSE Task Tracker", "version": "0.1.0", "description": "A simple task tracking application."}

tasks = [
    {"id": 1, "title": "Task 1", "description": "This is the first task.", "completed": False},
    {"id": 2, "title": "Task 2", "description": "This is the second task.", "completed": False},
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    new_id = max((item["id"] for item in tasks), default=0) + 1
    new_task = {"id": new_id, "title": task.title, "description": task.description, "completed": False}
    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def complete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")