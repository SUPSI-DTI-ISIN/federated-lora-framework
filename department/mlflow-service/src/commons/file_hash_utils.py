import hashlib
from pathlib import Path


class FileHashUtils:
    @classmethod
    def get_file_hash(cls, file_path: Path):
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()