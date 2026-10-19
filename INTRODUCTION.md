# The Data Science Project

The [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like Python project templates for data science projects.

## Introduction

In the data science domain projects are sometimes shared as an informal assemblage of scripts. This repository proposes two [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like layouts that can be used for organizing a data science project.

The "[Formal IMRaD-like Layout](#a-formal-imrad-like-layout)" offers an intuitive project layout. It organizes your project into `materials`, `methods`, and `results` directories. It adds an installable Python package within `methods`, while keeping materials and results in the project workspace.

The "[Informal IMRaD-like Layout](#an-informal-imrad-like-layout)" is a simple and intuitive non-installable Python project organized into `materials`, `methods`, and `results` directories.

## Table of contents

- [A formal IMRaD-like layout](#a-formal-imrad-like-layout)
- [An informal IMRaD-like layout](#an-informal-imrad-like-layout)
- [Support](#support)

## A formal IMRaD-like layout

The formal layout features `materials`, `methods`, and `results` directories at the project root. Their contents are up to you; no particular data, model, or output subdirectories are specified. This approach accommodates a wide range of data science and statistical methods. Reusable Python code lives in an installable package inside `methods`, alongside notebooks and any other methods.

```text
├── project ⬅ This is the project directory. Choose a name for your project.
    │
    ├── __about__.py
    │
    ├── materials ⬅ Put inputs and supporting materials here; organize them for your study.
    │   │
    │   └── README.md
    │
    ├── methods ⬅ Put your notebooks, reusable Python code, and other methods here.
    │   │
    │   ├── README.md
    │   │
    │   ├── notebooks
    │   │   │
    │   │   └── main.ipynb
    │   │
    │   └── package ⬅ This is the Python package. Cookiecutter lets you choose its name.
    │       │
    │       ├── __init__.py
    │       │
    │       ├── __main__.py ⬅ Define your package's pipeline here.
    │       │
    │       ├── paths.py ⬅ Import the paths to your materials, methods, and results from this module.
    │       │
    │       └── utils.py ⬅ Put reusable Python functions here.
    │
    ├── results ⬅ Put your study's outputs here; organize them for your study.
    │   │
    │   └── README.md
    │
    ├── pyproject.toml ⬅ Configure your package and its dependencies here.
    │
    └── README.md ⬅ Put your Introduction and Discussion here.
```

`package` is the default Python package name. Cookiecutter lets you choose another
name. Installing the package makes its utilities and workspace paths importable
without modifying `sys.path` or setting `PYTHONPATH`.

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
The notebook runs with the selected project as its working directory. The formal
template provides this entry point using Papermill.

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

Open `methods/notebooks/main.ipynb` in the same environment. Its first cell imports
`PROJECT_ROOT`, `MATERIALS_PATH`, `METHODS_PATH`, and `RESULTS_PATH` from your
configured package's `paths` module.

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

## An informal IMRaD-like layout

The Informal [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like Layout is a useful and intuitive project layout. It also serves as an introduction to the IMRaD-like layouts for data science projects. It isn't installable; however, its IMRaD-like naming convention makes its organization immediately recognizable to persons working in the science domains.

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

Open `methods/main.ipynb` with `methods` as the working directory. Its first cell
uses `pathlib` to define absolute paths to the project root and its three
directories; no package installation is needed.

## Support

If you have a feature request or run into any issues, feel free to submit an [issue](https://github.com/adamjpatterson/data-science-project/issues). You’re also welcome to reach out directly to one of the authors.

- [Adam Patterson](https://github.com/adamjpatterson)

## Development checks

See [the integration test instructions](https://github.com/adamjpatterson/data-science-project/blob/main/tests/README.md) for testing both Cookiecutter templates across the project branches.
