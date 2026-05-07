class TestApiRouter:
    def test_includes_all_sub_routers(self):
        from router.api import api_router
        routes = [r.path for r in api_router.routes]
        assert any("health" in p for p in routes)
        assert any("institutes" in p for p in routes)

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

    def test_institutes_router_init_exports(self):
        from router.institutes import router as institutes_router
        assert institutes_router is not None

    def test_institutes_router_init_version(self):
        import router.institutes as ri
        assert ri.__version__ == "1.0.0"

    def test_exceptions_router_init_exports(self):
        from router.exceptions import register_exception_handlers
        assert register_exception_handlers is not None

    def test_exceptions_router_init_version(self):
        import router.exceptions as re
        assert re.__version__ == "1.0.0"
