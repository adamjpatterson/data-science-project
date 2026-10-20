# Data Science Project Cookiecutter

This template creates a study with `materials`, `methods`, and `results` at the
project root. Organize their contents to suit your study. Reusable Python code
lives in `methods/package` by default; `package_name` is configurable.

Install the generated project with `python -m pip install -e .`. Import workspace
paths from `<package_name>.paths`, and run its `__main__.py` entry point with
`python -m <package_name>`. The starter workflow prints the project root; add
your own steps in `main()`. Notebooks are run separately. An editable install
discovers the study automatically;
installed wheels use `DATA_SCIENCE_PROJECT_ROOT` or `--project-dir` to select it.

See the generated README and the
[project introduction](https://github.com/adamjpatterson/the-data-science-project/blob/main/INTRODUCTION.md)
for details.
