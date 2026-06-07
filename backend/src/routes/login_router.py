from fastapi import APIRouter


login_router = APIRouter()

@login_router.post("/")
def loginrouter():
    ...