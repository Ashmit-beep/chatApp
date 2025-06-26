from fastapi import FastAPI
from .db import engine, Base
from .routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
