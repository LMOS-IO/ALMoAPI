"""alternate entrypoint that bundles an ASGI web server"""

import uvicorn
from loguru import logger

from main import app
from config.config import config
from common.logger import UVICORN_LOG_CONFIG


host = config.network.host
port = config.network.port

# TODO: Move OAI API to a separate folder
display_host = host if host != "0.0.0.0" else "localhost"
logger.info(f"Developer documentation: http://{display_host}:{port}/redoc")

# Setup app

uvicornConfig = uvicorn.Config(app, host=host, port=port, log_config=UVICORN_LOG_CONFIG)
server = uvicorn.Server(uvicornConfig)

try:
    server.run()
except KeyboardInterrupt:
    logger.info("received KeyboardInterrupt")
finally:
    server.shutdown()
