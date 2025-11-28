from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@router.get("/usuarios", response_class=HTMLResponse)
async def usuarios(request: Request):
    return templates.TemplateResponse(
        "usuarios.html",
        {"request": request}
    )


@router.get("/historial", response_class=HTMLResponse)
async def historial(request: Request):
    return templates.TemplateResponse(
        "historial.html",
        {"request": request}
    )


@router.get("/reportes/pdf")
async def generar_pdf():
    # Aquí luego agregamos la generación real de pdf
    return {"status": "PDF generado correctamente"}


@router.get("/resumen", response_class=HTMLResponse)
async def resumen(request: Request):
    return templates.TemplateResponse(
        "resumen.html",
        {"request": request}
    )