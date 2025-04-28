"""
Main entry point for the FastAPI application.
Initializes the app, includes routes, and starts the server.
"""

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from app.config import Config
from app.routes import router_spa, router_api_v1
from app.https import cert_file, key_file
from app.logger import logger
from pathlib import Path
import logging
import asyncio

# Configs
host = Config.get("app.host")
port = Config.get("app.port")
debug = Config.get("app.debug")
log_level = logging.DEBUG if debug else logging.INFO
logger.setLevel(log_level)

# Initialize FastAPI app
app = FastAPI()

# Include routes
app.include_router(router_spa, tags=["SPA"])
app.include_router(router_api_v1, tags=["API"])

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/partials", StaticFiles(directory="app/templates/partials"), name="partials")


if debug:
    @app.middleware("http")
    async def add_delay_middleware(request: Request, call_next):
        # Apply delay only to routes starting with "/api"
        if request.url.path.startswith(("/api", "/api/v1/files", "/api/v1/server")):
            await asyncio.sleep(1)
        return await call_next(request)

if __name__ == "__main__":
    # Start web server
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=debug,
        access_log=log_level == logging.DEBUG,
        ssl_keyfile=key_file,
        ssl_certfile=cert_file,
    )