from fastapi import APIRouter
from app.models import WorkflowRequest
from pathlib import Path
import json

router = APIRouter()

DATA_FILE = Path("data/plans.json")

@router.get("/")
def root():
    return {"message": "AI Workflow Assistant is running"}

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/plans")
def get_plans():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

@router.post("/plan")
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

    save_plan(plan)

    return plan

def save_plan(plan: dict):
    DATA_FILE.parent.mkdir(exist_ok=True)

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                plans = json.load(file)
            except json.JSONDecodeError:
                plans = []
    else:
        plans = []

    plans.append(plan)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(plans, file, indent=2)