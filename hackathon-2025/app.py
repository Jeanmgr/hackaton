from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers.dashboard import router as dashboard_router
from routers.monitoreo import router as monitoreo_router
from routers.api import router as api_router

app = FastAPI(title="EcoLoop API")

# Templates
templates = Jinja2Templates(directory="templates")

# Folder static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta raíz - Login
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Routers
app.include_router(api_router, prefix="/api", tags=["API"])
app.include_router(dashboard_router)
app.include_router(monitoreo_router)