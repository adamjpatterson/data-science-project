# The Data Science Project

The [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like Python project templates for data science projects.

## Introduction

In the data science domain projects are sometimes shared as an informal assemblage of scripts. This repository proposes two [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like layouts that can be used for organizing a data science project.  The "[Informal IMRaD-like Layout](#an-informal-imrad-like-layout)" is a Python project organized into `materials`, `methods`, and `results` directories.  The "[Formal IMRaD-like Layout](#a-formal-imrad-like-layout)" adds an installable Python package within `methods`, while keeping materials and results in the study workspace.

## Table of contents

- [An informal IMRaD-like layout](#an-informal-imrad-like-layout)
- [A formal IMRaD-like layout](#a-formal-imrad-like-layout)
- [Support](#support)

## An informal IMRaD-like layout

The Informal [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like Layout is a useful and intuitive project layout.  It also serves as an introduction to the IMRaD-like layouts for data science projects.  It isn't installable; however, its IMRaD-like naming convention makes its organization immediately recognizable to persons working in the science domains.

### Features

- A simple [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like layout.

### Explore the project layout

You can [create an informal layout project using the Cookiecutter](#create-an-informal-imrad-like-layout-data-science-project-using-the-cookiecutter).

#### The directory structure looks like this.

```
├── project ⬅ This is the project directory.
    │
    ├── materials ⬅ Put inputs and supporting materials here; organize them for your study.
    │   │
    │   └── README.md
    │
    ├── methods ⬅ You can put your utility functions and notebooks in the methods directory.
    │   │
    │   ├── main.ipynb
    │   │
    │   └── README.md
    │
    ├── results ⬅ You can put the outputs of your scripts (e.g., tables and visualizations) in the results directory.
    │   │
    │   └── README.md
    │
    ├── requirements.txt ⬅ You can specify your project requirements in this file.
    │
    ├── README.md ⬅ You can put your Introduction and Discussion in the README.md file.
    │
    └── .gitignore
```

### Create an informal IMRaD-like layout Data Science Project using the Cookiecutter

#### Install the Cookiecutter package.

```bash
pip install cookiecutter
```

#### Use the Cookiecutter to create an informal IMRaD-like layout project.

```bash
cookiecutter https://github.com/adamjpatterson/data-science-project.git --checkout informal_layout_cookiecutter
```

## A formal IMRaD-like layout

The formal layout keeps `materials`, `methods`, and `results` at the project root.
Their contents are up to the study: no particular data, model, or output categories
are required. Reusable Python code lives in an installable package inside
`methods`, alongside notebooks and any other methods.

```text
project/
├── README.md
├── pyproject.toml
├── __about__.py
├── materials/
│   └── README.md
├── methods/
│   ├── README.md
│   ├── notebooks/
│   │   └── main.ipynb
│   └── package/
│       ├── __init__.py
│       ├── __main__.py
│       ├── paths.py
│       └── utils.py
└── results/
    └── README.md
```

`package` is the default Python package name. Cookiecutter lets you choose another
name. Installing the package makes its utilities and workspace paths importable
without modifying `sys.path` or setting `PYTHONPATH`.

### Explore the example project

The `formal_flat_layout` branch contains a small Iris example using this layout.
The example adds an `iris/` directory under `materials`; that is specific to this
example, not a required category for other studies.

```bash
git clone --branch formal_flat_layout https://github.com/adamjpatterson/data-science-project.git
cd data-science-project/project
```

Activate your Python environment, then install the package in editable mode:

```bash
python -m pip install -e .
```

Open `methods/notebooks/main.ipynb` in that environment. Import paths and utilities
using the installed package name:

```python
from package.paths import MATERIALS_PATH, METHODS_PATH, RESULTS_PATH
from package.utils import say_hello

print(say_hello())
```

The example reads its inputs and saves its outputs through those paths:

```python
import pickle

rows = [
    line.strip().split(",")
    for line in (MATERIALS_PATH / "iris/iris.data").read_text().splitlines()
    if line.strip()
]
with (RESULTS_PATH / "iris.data.pkl").open("wb") as stream:
    pickle.dump(rows, stream)
```

Run the example pipeline with:

```bash
python -m package
```

It executes `methods/notebooks/main.ipynb` and prints the first ten Iris rows.

### Workspace paths

`package.paths` exports `PROJECT_ROOT`, `MATERIALS_PATH`, `METHODS_PATH`, and
`RESULTS_PATH`. Paths are absolute and do not depend on the notebook's current
directory.

An editable installation automatically locates the source project above
`methods/package`. Automatic discovery requires `pyproject.toml` and the three
workspace directories to exist there. To select another workspace, set this
before importing `package.paths` or starting a notebook kernel:

```bash
export DATA_SCIENCE_PROJECT_ROOT=/absolute/path/to/project
```

The selected directory must contain `materials`, `methods`, and `results`.
An empty, relative, or invalid environment setting raises a clear error rather
than selecting a different workspace. Constants are resolved on first import;
restart the kernel when changing the selected workspace.

For a pipeline invocation, you can instead specify:

```bash
python -m package --project-dir /path/to/project
```

This option overrides the environment setting and accepts relative paths as well.
The notebook runs with the selected project as its working directory. The example
and generated template both provide this entry point using Papermill.

### Create a formal IMRaD-like layout Data Science Project using the Cookiecutter

```bash
python -m pip install cookiecutter
cookiecutter https://github.com/adamjpatterson/data-science-project.git --checkout formal_flat_layout_cookiecutter
```

The form lets you configure the project directory, Python package, repository URL,
description, and author information:

```text
project_name: project
package_name: package
repository_url: https://github.com/pypa/sampleproject
package_description: A small example package
author_name: Example Author
author_email: author@example.com
```

Project directory names may contain dashes, such as `my-study`. Use a valid Python
import name for the package, such as `my_study`. With that choice, Cookiecutter
creates `methods/my_study/` and notebook imports use `from my_study.paths import …`.
No fixed subdirectories are created within `materials` or `results`.

From the generated project directory, activate your environment and run:

```bash
python -m pip install -e .
```

Add dependencies to `pyproject.toml` and rerun the installation command when they
change. Put reusable functions in your package and import them into notebooks;
notebooks themselves are outside the package and do not need a `__package__`
assignment.

### Build and distribute the Python code

Hatchling is configured to package `methods/package` (or your chosen package name).
A wheel contains the Python code, including `paths.py` and the pipeline entry
point. Materials, notebooks, and generated results stay in the study workspace.
They are not copied into the installed package.

After installing a wheel, select an existing workspace with
`DATA_SCIENCE_PROJECT_ROOT` or `--project-dir`. A wheel cannot infer which study
you intend to use. Keep or share that workspace separately when distributing the
code. The [Python packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
describes how to build and publish distributions.

### Updating from the previous formal layout

Move `package/materials` and `package/results` to the project root. Move notebooks
to `methods/notebooks`, reusable code to `methods/package`, and utilities formerly
in `package.methods` into the package itself. The workspace directories are no
longer Python subpackages; remove their old `__init__.py` files.

Replace the old path imports from `package.materials`, `package.methods`, and
`package.results` with imports from `package.paths`. Replace
`from package.methods.utils import …` with `from package.utils import …`.
Update the build configuration to use `packages = ["methods/package"]` under
`[tool.hatch.build.targets.wheel]`, add the new `paths.py` module and pipeline entry
point, and reinstall with `python -m pip install -e .`.

The example implementation is available in
[`methods/package`](https://github.com/adamjpatterson/data-science-project/tree/formal_flat_layout/project/methods/package).
The existing branch names are retained for the example and both templates.

## Support

If you have a feature request or run into any issues, feel free to submit an [issue](https://github.com/adamjpatterson/data-science-project/issues). You’re also welcome to reach out directly to one of the authors.

- [Adam Patterson](https://github.com/adamjpatterson)

## Development checks

See [the integration test instructions](https://github.com/adamjpatterson/data-science-project/blob/main/tests/README.md) for testing both Cookiecutter templates and the formal example across the project branches.
