# Project

## Introduction

Describe the question or purpose of this study.

## Organization

- `materials/`: inputs and supporting materials for this study.
- `methods/`: notebooks, reusable Python code, and other methods.
- `results/`: outputs from the study.

Organize the contents of these directories to suit your study. No particular data,
model, or output categories are required.

The installable Python package is in `methods/{{cookiecutter.package_name}}/`. Install it from this
project directory with `python -m pip install -e .`, then use:

```python
from {{cookiecutter.package_name}}.paths import PROJECT_ROOT, MATERIALS_PATH, METHODS_PATH, RESULTS_PATH
```

Editable installs locate this workspace automatically, independently of the
notebook's current directory. Set `DATA_SCIENCE_PROJECT_ROOT` to an absolute
workspace directory before importing paths to select a different study. That
directory must contain `materials`, `methods`, and `results`. Invalid settings
raise an error; they never silently select another directory.

Run `python -m {{cookiecutter.package_name}}` to call `main()` in your package's
`__main__.py`. The starter workflow prints the resolved project root. Add your
workflow there, calling reusable package functions. Notebooks run separately;
the entry point does not execute them or change the working directory.

To select another workspace, use
`python -m {{cookiecutter.package_name}} --project-dir /path/to/study`. The command-line option
takes precedence over the environment setting and accepts relative paths too.
Path constants are resolved when `{{cookiecutter.package_name}}.paths` is first imported; restart
the kernel before switching workspaces.

Wheels contain only Python code. Data, notebooks, and results remain in the study
workspace. After installing a wheel, select that workspace using the environment
setting or command-line option above.

## Discussion

Describe and interpret the results here.
