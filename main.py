from fastapi import FastAPI

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

