import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.config import CORS_ALLOWED_ORIGINS
from app.database import engine
from app.exceptions import validation_exception_handler
from app.routers import authentication, gamestate, user

load_dotenv()

OPENAPI_URL_CONFIG = os.getenv("OPENAPI_URL_CONFIG")


app = FastAPI(docs_url="/docs" if OPENAPI_URL_CONFIG is not None else None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(engine)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(user.router)
app.include_router(gamestate.router)
app.include_router(authentication.router)
