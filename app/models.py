from pydantic import BaseModel

class WorkflowRequest(BaseModel):
    goal: str
    task_type: str