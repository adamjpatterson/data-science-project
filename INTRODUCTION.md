# The Data Science Project

The [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like Python project templates for data science projects.

## Introduction

In the data science domain projects are sometimes shared as an informal assemblage of scripts. This repository proposes two familiar [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like layouts that can be used for organizing a data science project.

The [Formal IMRaD-like Layout](#a-formal-imrad-like-layout) offers an intuitive and familiar project layout. It organizes your project into `materials`, `methods`, and `results` directories. It adds an installable Python package within `methods`, while keeping `materials` and `results` in the project workspace.

The [Informal IMRaD-like Layout](#an-informal-imrad-like-layout) is a simple and intuitive non-installable Python project organized into `materials`, `methods`, and `results` directories.

This repository provides [Cookiecutter](https://github.com/cookiecutter/cookiecutter) templates for creating these project layouts:

- Create a [formal IMRaD-like layout](#create-a-formal-imrad-like-layout-data-science-project-using-the-cookiecutter) using the Cookiecutter
- Create an [informal IMRaD-like layout](#create-an-informal-imrad-like-layout-data-science-project-using-the-cookiecutter) using the Cookiecutter

## Table of contents

- [A formal IMRaD-like layout](#a-formal-imrad-like-layout)
- [An informal IMRaD-like layout](#an-informal-imrad-like-layout)
- [Versioning](#versioning)
- [Development checks](#development-checks)
- [Other solutions](#other-solutions)
- [Support](#support)

## A formal IMRaD-like layout

The formal layout features `materials`, `methods`, and `results` directories at the project root. Their contents are up to you; no particular data, model, or output subdirectories are specified. This approach accommodates a wide range of data science and statistical methods, while offering a project layout that is instantly recognizable to persons working in the science domains.

Use the `materials` directory for source data and intermediary datasets. Use the `results` directory for storing the products of your analysis (e.g., datasets, visualizations). The `methods` directory stores your procedures including notebooks and the installable package.

### Features

- A familiar [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like layout.
- An installable Python package.
- A preconfigured `paths` module useful for navigating the project from a notebook.

### Explore the project layout

You can [create a formal layout project using the Cookiecutter](#create-a-formal-imrad-like-layout-data-science-project-using-the-cookiecutter).

#### The directory structure looks like this.

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

The default Python package name is `package`. You can specify a different package name using the [Cookiecutter](#create-a-formal-imrad-like-layout-data-science-project-using-the-cookiecutter). Installing the package makes its utilities and workspace paths importable without modifying `sys.path` or setting `PYTHONPATH`.

### Workspace paths

The `package.paths` module exports `PROJECT_ROOT`, `MATERIALS_PATH`, `METHODS_PATH`, and `RESULTS_PATH`. Paths are resolved from the project root and returned as absolute paths, so they work independently of the notebook’s current working directory.

An editable installation automatically locates the source project above `methods/package`. Automatic discovery requires `pyproject.toml` and the three workspace directories to exist there. To select another workspace, set this before importing `package.paths` or starting a notebook kernel:

```bash
export DATA_SCIENCE_PROJECT_ROOT=/absolute/path/to/project
```

The selected directory must contain `materials`, `methods`, and `results`. An empty, relative, or invalid environment setting raises a clear error rather than selecting a different workspace. Constants are resolved on first import; restart the kernel when changing the selected workspace.

### Pipeline invocation

Run the package's `__main__.py` entry point with:

```bash
python -m package
```

This calls `main()`, which initially prints the resolved project root. Define your workflow in that function, calling reusable functions from your package. Replace `package` with your configured package name.

Notebooks are run separately; the entry point does not execute them. Notebook execution can be added to your workflow if your project needs it.

To select another project workspace for an invocation, specify:

```bash
python -m package --project-dir /path/to/project
```

This option overrides `DATA_SCIENCE_PROJECT_ROOT` and accepts relative paths. It selects the workspace used by `package.paths` without changing the working directory. Use those absolute paths when reading materials or writing results.

### Create a formal IMRaD-like layout Data Science Project using the Cookiecutter

Install the Cookiecutter package.

```bash
python -m pip install cookiecutter
```

Use the Cookiecutter to create a formal IMRaD-like layout project.

```bash
cookiecutter https://github.com/adamjpatterson/the-data-science-project.git --checkout formal-cookiecutter-v1.0.0
```

The form lets you configure the project directory, Python package, repository URL, description, and author information:

```text
project_name: project
package_name: package
repository_url: https://github.com/pypa/sampleproject
package_description: A small example package
author_name: Example Author
author_email: author@example.com
```

Project directory names may contain dashes, such as `my-study`. Use a valid Python import name for the package, such as `my_study`.

From the generated project directory, activate your environment and install your package in editable mode. Editable installation lets you change the package code without reinstalling it. Restart the notebook kernel or reload affected modules to use changes to code already imported.

```bash
python -m pip install -e .
```

Open `methods/notebooks/main.ipynb` in the same environment. Its first cell imports `PROJECT_ROOT`, `MATERIALS_PATH`, `METHODS_PATH`, and `RESULTS_PATH` from your configured package's `paths` module.

Add dependencies to `pyproject.toml` and rerun the installation command when they change. Put reusable functions in your package and import them into notebooks.

### Build and distribute the Python code

Hatchling is configured to package `methods/package` (or your chosen package name). A wheel contains the Python code, including `paths.py` and the pipeline entry point. Materials, notebooks, and generated results stay in the project workspace. They are not copied into the installed package.

After installing a wheel, select an existing workspace with `DATA_SCIENCE_PROJECT_ROOT` or `--project-dir`. A wheel cannot infer which project you intend to use. Keep or share that workspace separately when distributing the code. The [Python packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) describes how to build and publish distributions.

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

Install the Cookiecutter package.

```bash
python -m pip install cookiecutter
```

Use the Cookiecutter to create an informal IMRaD-like layout project.

```bash
cookiecutter https://github.com/adamjpatterson/the-data-science-project.git --checkout informal-cookiecutter-v1.0.0
```

Open `methods/main.ipynb` with `methods` as the working directory. Its first cell uses `pathlib` to define absolute paths to the project root and its three
directories; no package installation is needed.

## Versioning

The current template release is **1.0.0**. The commands above select its fixed
release tags. Both templates share a release number; generated projects have
independent version histories. Formal Python packages start at `0.0.1` in
`__about__.py`.

See the [versioning policy and release workflow](https://github.com/adamjpatterson/the-data-science-project/blob/v1.0.0/VERSIONING.md)
for compatibility rules, template tags, and development branches.

## Development checks

See [the integration test instructions](https://github.com/adamjpatterson/the-data-science-project/blob/main/tests/README.md) for testing both Cookiecutter templates across the project branches.

## Other solutions

Other approaches to organizing data science projects include:

- [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/): A project template from DrivenData with dedicated directories for data, models, notebooks, and reports, plus configurable development tools.

## Support

If you have a feature request or run into any issues, feel free to submit an [issue](https://github.com/adamjpatterson/the-data-science-project/issues). You’re also welcome to reach out directly to the author.

- [Adam Patterson](https://github.com/adamjpatterson)
