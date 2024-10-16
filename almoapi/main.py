"""Primary entrypoint that exposes an ASGI application at `app`"""

from contextlib import asynccontextmanager
import os
import pathlib
from fastapi import FastAPI
from loguru import logger

from auth import AuthManager
from common import gen_logging, model
from common.actions import branch_to_actions
from config.config import config
from endpoints.server import setup_app

from backends.exllamav2.version import check_exllama_version


async def startup():
    """Async entry function for program startup"""

    gen_logging.broadcast_status()

    # If an initial model name is specified, create a container
    # and load the model
    if config.model.model_name:
        await model.load_model(
            model=config.model,
            draft=config.draft_model,
        )

        # Load loras after loading the model
        if config.lora.loras:
            lora_dir = pathlib.Path(config.lora.lora_dir)
            # TODO: remove model_dump()
            await model.container.load_loras(
                lora_dir.resolve(), **config.lora.model_dump()
            )

    # If an initial embedding model name is specified, create a separate container
    # and load the model
    embedding_model_name = config.embeddings.embedding_model_name
    if embedding_model_name:
        embedding_model_path = pathlib.Path(config.embeddings.embedding_model_dir)
        embedding_model_path = embedding_model_path / embedding_model_name

        try:
            # TODO: remove model_dump()
            await model.load_embedding_model(
                embedding_model_path, **config.embeddings.model_dump()
            )
        except ImportError as ex:
            logger.error(ex.msg)


async def shutdown():
    if model.container:
        await model.unload_model(skip_wait=True, shutdown=True)

    if model.embeddings_container:
        await model.unload_embedding_model()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


# load config
config.load()

# setup auth
AuthManager.setup()

# branch to default paths if required
if branch_to_actions():
    exit()

# Enable CUDA malloc backend
if config.developer.cuda_malloc_backend:
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "backend:cudaMallocAsync"
    logger.warning("EXPERIMENTAL: Enabled the pytorch CUDA malloc backend.")

# Check exllamav2 version and give a descriptive error if it's too old
# Skip if launching unsafely
if config.developer.unsafe_launch:
    logger.warning(
        "UNSAFE: Skipping ExllamaV2 version check.\n"
        "If you aren't a developer, please keep this off!"
    )
else:
    check_exllama_version()

# setup auth
AuthManager.setup()

app = setup_app(lifespan=lifespan)
