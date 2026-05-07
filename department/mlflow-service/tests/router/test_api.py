class TestApiRouter:
    def test_includes_all_sub_routers(self):
        from router.api import api_router
        routes = [r.path for r in api_router.routes]
        assert any("health" in p for p in routes)
        assert any("manifest" in p or "file_name" in p for p in routes)
        assert any("adapters" in p for p in routes)
        assert any("federated" in p for p in routes)

    def test_is_importable(self):
        from router.api import api_router
        assert api_router is not None

    def test_router_init_exports(self):
        from router import api_router, lifespan
        assert api_router is not None
        assert lifespan is not None

    def test_router_init_version(self):
        import router
        assert router.__version__ == "1.0.0"

    def test_model_router_init_exports(self):
        from router.model import adapter_router, base_router
        assert adapter_router is not None
        assert base_router is not None

    def test_model_router_init_version(self):
        import router.model as rm
        assert rm.__version__ == "1.0.0"
