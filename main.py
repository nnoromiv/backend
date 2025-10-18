import os
from fastapi import FastAPI, HTTPException, Query
from api import weather, traffic, incident, summary, visuals, system
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pipeline import run_pipeline
import asyncio

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
    allow_origins=["*"],
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
async def root(destination: str | None = Query(None, description="Optional destination")):
    """
    Run the pipeline. If 'destination' is provided, it takes priority over environment variable.
    """
    try:
        # Pass the destination to run_pipeline
        await asyncio.to_thread(run_pipeline, destination)
        return {"success": True, "destination_used": destination or os.getenv("DESTINATION", "Reading")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
