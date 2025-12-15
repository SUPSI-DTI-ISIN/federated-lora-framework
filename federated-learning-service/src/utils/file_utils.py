from pathlib import Path
from typing import List, Optional


class FileUtils:
    @staticmethod
    def is_folder_valid(folder_path: Path) -> bool:
        if not folder_path.exists():
            print("Folder does not exist")
            return False

        if not folder_path.is_dir():
            print("Folder passed is not a directory")
            return False

        return True

    @classmethod
    def get_files_from_folder(cls, folder_path: Path, pattern: str) -> Optional[List[Path]]:
        if not cls.is_folder_valid(folder_path=folder_path):
            return None
        return list(folder_path.glob(pattern=pattern))