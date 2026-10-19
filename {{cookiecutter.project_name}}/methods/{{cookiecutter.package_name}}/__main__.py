"""Execute the study's main notebook."""
import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, help="Study directory (overrides DATA_SCIENCE_PROJECT_ROOT).")
    args = parser.parse_args()
    if args.project_dir is not None:
        os.environ["DATA_SCIENCE_PROJECT_ROOT"] = str(args.project_dir.expanduser().resolve())

    from .paths import PROJECT_ROOT, METHODS_PATH, RESULTS_PATH
    import papermill as pm

    pm.execute_notebook(
        METHODS_PATH / "notebooks" / "main.ipynb",
        None,
        cwd=str(PROJECT_ROOT),
    )


if __name__ == "__main__":
    main()
