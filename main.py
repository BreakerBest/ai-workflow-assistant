from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Workflow Assistant")

class WorkflowRequest(BaseModel):
    goal: str
    task_type: str

@app.get("/")
def root():
    return {"message": "AI Workflow Assistant is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/plan")
def create_plan(request: WorkflowRequest):
    goal = request.goal
    task_type = request.task_type

    plan = {
        "goal": goal,
        "task_type": task_type,
        "steps": [
            f"Understand the goal: {goal}",
            f"Choose the best approach for task type: {task_type}",
            "Break the work into small tasks",
            "Complete the highest-priority task first",
            "Review and improve the result"
        ]
    }

    return plan