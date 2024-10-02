import asyncio
from typing import Optional
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from common.logger import UVICORN_LOG_CONFIG
from common.networking import get_global_depends
from endpoints.OAI import router as OAIRouter
from endpoints.core.router import router as CoreRouter


def setup_app(host: Optional[str] = None, port: Optional[int] = None):
    """Includes the correct routers for startup"""

    app = FastAPI(
        title="ALMoAPI",
        summary="A general purpose agentic oriented inference framework",
        description=(
            "This docs page is not meant to send requests! Please use a service "
            "like Postman or a frontend UI."
        ),
        dependencies=get_global_depends(),
    )

    # ALlow CORS requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(OAIRouter.setup())

    # Include core API request paths
    app.include_router(CoreRouter)

    return app


def export_openapi():
    """Function to return the OpenAPI JSON from the API server"""

    app = setup_app()
    return app.openapi()


async def start_api(host: str, port: int):
    """Isolated function to start the API server"""

    # TODO: Move OAI API to a separate folder
    logger.info(f"Developer documentation: http://{host}:{port}/redoc")

    # Setup app
    app = setup_app(host, port)

    # Get the current event loop
    loop = asyncio.get_running_loop()

    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_config=UVICORN_LOG_CONFIG,
        loop=loop,
    )
    server = uvicorn.Server(config)

    await server.serve()
