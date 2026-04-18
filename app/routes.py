from fastapi import APIRouter
from app.models import WorkflowRequest
from pathlib import Path
from datetime import datetime
import json
import uuid

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
@router.get("/plans/{plan_id}")
def get_plan(plan_id: str):
    if not DATA_FILE.exists():
        return {"error": "No plans found"}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            plans = json.load(file)
        except json.JSONDecodeError:
            return {"error": "Invalid plans data"}

    for plan in plans:
        if plan.get("id") == plan_id:
            return plan

    return {"error": "Plan not found"}

def generate_steps(goal: str, task_type: str):
    task_type = task_type.lower()

    if task_type == "planning":
        return [
            f"Define the goal clearly: {goal}",
            "Break the goal into smaller milestones",
            "Put the tasks in the best order",
            "Choose the most important first step",
            "Review progress and adjust the plan",
        ]
    elif task_type == "studying":
        return [
            f"Identify the topic you need to study: {goal}",
            "Gather notes, class materials, and practice problems",
            "Break the topic into smaller sections",
            "Study one section at a time and test yourself",
            "Review weak areas and repeat",
        ]
    elif task_type == "fitness":
        return [
            f"Set the fitness target clearly: {goal}",
            "Choose a workout schedule you can follow weekly",
            "Plan meals that support the goal",
            "Track workouts and body progress each week",
            "Adjust based on results and consistency",
        ]
    elif task_type == "business":
        return [
            f"Define the business goal clearly: {goal}",
            "Research the target customer or market",
            "List the key tasks needed to launch",
            "Take action on the most important revenue-driving step",
            "Review results and improve the process",
        ]
    elif task_type == "coding":
        return [
            f"Understand the coding goal: {goal}",
            "Break the feature into smaller parts",
            "Build the simplest version first",
            "Test each part as you go",
            "Fix bugs and clean up the code",
        ]
    else:
        return [
            f"Understand the goal: {goal}",
            f"Choose the best approach for task type: {task_type}",
            "Break the work into small tasks",
            "Complete the highest-priority task first",
            "Review and improve the result",
        ]


@router.post("/plan")
def create_plan(request: WorkflowRequest):
    goal = request.goal
    task_type = request.task_type

    plan = {
    "id": str(uuid.uuid4()),
    "goal": goal,
    "task_type": task_type,
    "steps": generate_steps(goal, task_type),
    "created_at": datetime.now().isoformat(),
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