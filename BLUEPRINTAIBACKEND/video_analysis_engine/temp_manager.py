from pathlib import Path
import shutil


def delete_path(path: str | Path) -> None:
    path = Path(path)
    if not path.exists():
        return

    if path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
