from pathlib import Path
from typing import List


def is_folder_valid(folder_path: Path) -> bool:
    if not folder_path.exists():
        print("Folder does not exist")
        return False

    if not folder_path.is_dir():
        print("Folder passed is not a directory")
        return False

    return True

def get_pdf_files_from_folder(folder_path: Path) -> List[Path]:
    return list(folder_path.glob("*.pdf"))