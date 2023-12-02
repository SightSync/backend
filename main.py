from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from routers import image, locate, intent, stt
from services import startup

app = FastAPI(
    title="Lauzhack 2023 - AXA's challenge",
    description="SightSync",
    docs_url="/docs",
    redoc_url="/redoc",
    version="0.1.0",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)

app.include_router(image.router)
app.include_router(locate.router)
app.include_router(intent.router)
app.include_router(stt.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

startup.load_grounding()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
