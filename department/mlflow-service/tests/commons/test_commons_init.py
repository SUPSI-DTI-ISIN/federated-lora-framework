class TestCommonsInit:
    def test_all_exports_are_importable(self):
        from commons import (
            ModelPathUtils,
            FileHashUtils,
            ManifestUtils,
            FileUtils,
            AdapterUtils,
            ModelUtils,
        )
        assert ModelPathUtils is not None
        assert FileHashUtils is not None
        assert ManifestUtils is not None
        assert FileUtils is not None
        assert AdapterUtils is not None
        assert ModelUtils is not None

    def test_version(self):
        import commons
        assert commons.__version__ == "1.0.0"

    def test_all_list(self):
        import commons
        assert set(commons.__all__) == {
            "ModelPathUtils",
            "FileHashUtils",
            "ManifestUtils",
            "FileUtils",
            "AdapterUtils",
            "ModelUtils",
        }
