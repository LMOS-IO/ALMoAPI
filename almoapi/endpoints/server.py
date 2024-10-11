from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.networking import get_global_depends
from endpoints.OAI import router as OAIRouter
from endpoints.core.router import router as CoreRouter


def setup_app(lifespan):
    """Includes the correct routers for startup"""

    app = FastAPI(
        title="ALMoAPI",
        summary="A general purpose agentic oriented inference framework",
        description=(
            "This docs page is not meant to send requests! Please use a service "
            "like Postman or a frontend UI."
        ),
        dependencies=get_global_depends(),
        lifespan=lifespan,
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
