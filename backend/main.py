from fastapi import FastAPI

try:
    from .database import Base, engine
    from .routes import auth_routes, notes_routes
except ImportError:
    from database import Base, engine
    from routes import auth_routes, notes_routes

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(auth_routes.router)
app.include_router(notes_routes.router)


@app.get("/")
def root():
    return {"message": "app running"}
