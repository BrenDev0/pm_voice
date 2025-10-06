from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.modules.interactions import ws



app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="src/public"), name="public")

@app.get("/")
async def get():
    return FileResponse('src/public/index.html')

app.include_router(ws.router)
