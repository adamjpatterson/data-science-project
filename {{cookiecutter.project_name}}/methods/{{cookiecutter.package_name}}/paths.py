"""Paths to the study workspace, independent of the current directory."""
import os
from pathlib import Path

_ROOT_ENV = "DATA_SCIENCE_PROJECT_ROOT"


def _is_project(root):
    return all((root / name).is_dir() for name in ("materials", "methods", "results"))


def _resolve_project_root():
    configured = os.environ.get(_ROOT_ENV)
    if configured is not None:
        root = Path(configured).expanduser()
        if not configured or not root.is_absolute():
            raise RuntimeError(f"{_ROOT_ENV} must be an absolute project directory.")
        root = root.resolve()
        if not _is_project(root):
            raise RuntimeError(
                f"{_ROOT_ENV}={root} must contain materials, methods, and results directories."
            )
        return root

    package_dir = Path(__file__).resolve().parent
    root = package_dir.parent.parent
    if (package_dir.parent.name == "methods"
            and (root / "pyproject.toml").is_file() and _is_project(root)):
        return root
    raise RuntimeError(
        "Cannot locate the study workspace. Set DATA_SCIENCE_PROJECT_ROOT to its "
        "absolute directory before importing paths, or use --project-dir with the pipeline. "
        "Automatic discovery requires an editable install from methods/<package>."
    )


PROJECT_ROOT = _resolve_project_root()
MATERIALS_PATH = PROJECT_ROOT / "materials"
METHODS_PATH = PROJECT_ROOT / "methods"
RESULTS_PATH = PROJECT_ROOT / "results"
