class TestModelSchemaInit:
    def test_all_exports_are_importable(self):
        from schemas.model import FileDTO, ManifestDTO, ModelAdaptersVersionDTO, FederatedDataDTO
        assert FileDTO is not None
        assert ManifestDTO is not None
        assert ModelAdaptersVersionDTO is not None
        assert FederatedDataDTO is not None

    def test_version(self):
        import schemas.model as m
        assert m.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.model as m
        assert set(m.__all__) == {"FileDTO", "ManifestDTO", "ModelAdaptersVersionDTO", "FederatedDataDTO"}
