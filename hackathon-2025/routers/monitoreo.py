from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/monitoreo", response_class=HTMLResponse)
async def monitoreo(request: Request):
    return templates.TemplateResponse(
        "monitoreo.html",
        {"request": request}
    )
