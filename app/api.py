from fastapi import APIRouter, Response, Request, HTTPException
from app.ics_generator import generate_calendar
from app.config import settings

router = APIRouter()

@router.get("/gym.ics", response_class=Response)
async def get_gym_feed(request: Request):
    token = request.query_params.get("token")
    if token != settings.secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    ics_data = generate_calendar()
    return Response(content=ics_data, media_type="text/calendar")
