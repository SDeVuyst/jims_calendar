from fastapi import FastAPI
from app.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Jims Calendar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(api_router)
