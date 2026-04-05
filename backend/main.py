from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .routes import auth_routes, notes_routes
except ImportError:
    from routes import auth_routes, notes_routes

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(auth_routes.router)
app.include_router(notes_routes.router)


@app.get("/")
def root():
    return {"message": "app running"}
