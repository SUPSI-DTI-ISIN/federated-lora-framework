from schemas.exceptions import ModelLoadingError


class TestModelLoadingError:
    def test_stores_model_key(self):
        assert ModelLoadingError(model_key="llama-3").model_key == "llama-3"

    def test_message_contains_model_key(self):
        assert "llama-3" in str(ModelLoadingError(model_key="llama-3"))

    def test_is_exception_subclass(self):
        assert issubclass(ModelLoadingError, Exception)


class TestSchemasExceptionsInit:
    def test_exports_model_loading_error(self):
        from schemas.exceptions import ModelLoadingError as E
        assert E is ModelLoadingError

    def test_version(self):
        import schemas.exceptions as se
        assert se.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.exceptions as se
        assert "ModelLoadingError" in se.__all__
