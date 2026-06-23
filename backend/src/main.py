from fastapi import FastAPI
import os
from dotenv import load_dotenv
from routes.login_router import login_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

load_dotenv()

app.include_router(login_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000","http://localhost:5173"],  # link do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)