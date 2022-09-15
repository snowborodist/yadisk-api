import uvicorn

from src.yadisk_api.settings import settings

uvicorn.run(
    "yadisk_api.app:app",
    host=settings.server_host,
    port=settings.server_port,
    reload=True
)
