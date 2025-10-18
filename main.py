from fastapi import FastAPI
from api import weather, traffic, incident, summary, visuals, system
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield
    # Shutdown logic (if needed)

app = FastAPI(
    title="Urban Traffic Intelligence System",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.weather_router)
app.include_router(traffic.traffic_router)
app.include_router(incident.incident_router)
app.include_router(summary.summary_router)
app.include_router(visuals.visuals_router)
app.include_router(system.system_router)
    
@app.get("/")
async def root():
    return {
        "message": "Hello, you are not lost. We just don't like keeping here empty"
    }