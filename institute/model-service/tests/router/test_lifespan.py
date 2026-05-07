import pytest
from unittest.mock import MagicMock, patch


class TestLifespan:
    async def test_calls_download_base_model_on_startup(self):
        from router.lifespan import lifespan
        from fastapi import FastAPI

        app = FastAPI()
        mock_downloader = MagicMock()

        with patch("router.lifespan.build_init_model_downloader_service",
                   return_value=mock_downloader), \
             patch("router.lifespan.settings") as mock_settings:
            mock_settings.model_key = "llama-3"

            async with lifespan(app):
                pass

        mock_downloader.download_base_model.assert_called_once_with(model_key="llama-3")
