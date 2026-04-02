from fastapi import FastAPI

try:
    from .routes import auth_routes, notes_routes
except ImportError:
    from routes import auth_routes, notes_routes

app=FastAPI()

app.include_router(auth_routes.router)
app.include_router(notes_routes.router)


@app.get("/")
def root():
    return {"message": "app running"}
