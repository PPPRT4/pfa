import os
import sys
from fastapi import FastAPI

try:
    from .routes import auth_routes, notes_routes
except ImportError:
    from routes import auth_routes, notes_routes

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from ai.agent import agent_router

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(notes_routes.router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {"message": "app running"}