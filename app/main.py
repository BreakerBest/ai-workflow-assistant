from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="AI Workflow Assistant")

app.include_router(router)