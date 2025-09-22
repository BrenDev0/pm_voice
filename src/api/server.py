from fastapi import FastAPI, Body
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.dependencies.configure_container import configure_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_container()  
    yield

app = FastAPI(lifespan=lifespan)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/", status_code=202)
def testing(
    data = Body(...)
):
    print(data)


