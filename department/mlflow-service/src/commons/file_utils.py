from pathlib import Path


class FileUtils:
    @classmethod
    def join_paths(cls, base_path: Path, file_name: str) -> Path:
        file_path = base_path.joinpath(file_name)
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_name} is not existing")

        return file_path