# The Data Science Project

The [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like Python project templates for data science projects.

## Introduction

In the data science domain projects are sometimes shared as an informal assemblage of scripts. This repository proposes two [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like layouts that can be used for organizing a data science project.  The "[Informal IMRaD-like Layout](#an-informal-imrad-like-layout)" is a Python project organized into `materials`, `methods`, and `results` directories.  The "[Formal IMRaD-like Flat Layout](#a-formal-imrad-like-flat-layout)" is a conventional installable Python [flat-layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) project that can be built and distributed as a package and published to PyPI.

## Table of contents

- [An informal IMRaD-like layout](#an-informal-imrad-like-layout)
- [A formal IMRaD-like flat layout](#a-formal-imrad-like-flat-layout)
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
    ├── materials ⬅ You can put your datasets and models in the materials directory.
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

## A formal IMRaD-like flat layout

The Formal [IMRaD](https://en.wikipedia.org/wiki/IMRAD)-like Flat Layout project template describes an approach for organizing your data science project using a conventional Python "[flat-layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)" project layout. It follows formal conventions for packaging a Python project. You install it into your environment just like an ordinary Python package. It consists of a single package with an IMRaD-like layout; it contains `materials`, `methods`, and `results` sub-packages. Project dependencies are specified in the `pyproject.toml` file.

One important advantage of this approach is that utility functions can be conveniently imported into notebooks from anywhere in the package. It makes imports seamless without having to modify `sys.path` or setting the `PYTHONPATH` environment variable.

### Features

- An easily recognizable formal Python package layout
- Define your dependencies using formal packing conventions
- Seamless imports from anywhere in your package
- Relative package imports from within notebooks
- Pipeline definitions

### Explore the project layout

You can clone this repository and follow this short tutorial in order to explore the project layout.  If you want to start a new project, you can [create a project using the Cookiecutter](#create-a-formal-imrad-like-flat-layout-data-science-project-using-the-cookiecutter).

### Instructions

In this example you will clone the repository, explore its layout, install it, and run an example notebook.

#### Clone the repository.

```bash
git clone https://github.com/adamjpatterson/data-science-project.git
```

#### Checkout the branch.

```bash
git checkout formal_flat_layout
```

#### Change directory into the repository's project directory.

This is the top-level directory of a conventional Python package.
```bash
cd data-science-project/project
```

#### The directory structure looks like this.

This is a conventional [flat-layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) Python project.  The project follows all the conventions of a formal Python project.

```
├── project ⬅ This is the project directory.  Optionally chose a name for your project.
    |
    ├── __about__.py
    |
    ├── LICENSE
    |
    ├── package ⬅ This is the package directory.  Optionally give the package a unique name.
    |   |
    │   ├── __init__.py
    |   |
    |   ├── __main__.py ⬅ You can define your package's pipeline in the __main__.py module.
    |   |
    │   ├── materials ⬅ You can put your datasets and models in the materials directory.
    |   |   |
    │   │   ├── __init__.py
    |   |   |
    │   │   └── README.md
    |   |
    │   ├── methods ⬅ You can put your utility functions and notebooks in the methods directory.
    |   |   |
    │   │   ├── __init__.py
    |   |   |
    │   │   ├── notebooks
    |   |   |   |
    │   │   │   └── main.ipynb
    |   |   |
    │   │   ├── README.md
    |   |   |
    │   │   └── utils.py
    |   |
    │   └── results ⬅ You can put the outputs of your scripts (e.g., tables and visualizations) in the results directory.
    |       |
    │       ├── __init__.py
    |       |
    │       └── README.md
    |   
    ├── pyproject.toml ⬅ The project is configured to use the Hatch project manager.
    |
    └── README.md
```

#### Activate your environment if you are using a package manager (e.g., conda).

```bash
conda activate <your-environment>
```

#### Install the package in editable mode.  

An editable install, also known as a development install, will make changes to your package modules immediately available when you restart your kernel.
```bash
pip install -e .
```
You have installed a Python package named `package`.  Once you complete the tutorial, you can uninstall it using pip.
```bash
pip uninstall package
```

#### Open the `package/methods/notebooks/main.ipynb` notebook and run the cells.

##### Import the path of each sub-package.

```python
from package.materials import MATERIALS_PATH
from package.methods import METHODS_PATH
from package.results import RESULTS_PATH
```

##### Set the `__package__` attribute and use a relative import to import a utility function from the `methods` sub-package.

```python
__package__ = "package.methods.notebooks"

from ..utils import say_hello

print(say_hello())
```

##### Import a utility function from the `methods` sub-package.

```python
from package.methods.utils import say_hello

print(say_hello())
```

##### Read data from the `MATERIALS_PATH`, transform it into a list of lists, and write the data to the `RESULTS_PATH` and print it to the notebook output cell.

```python
from pprint import pprint
import pickle

# Read `iris.data` from the MATERIALS_PATH.
data = [
    line.strip().split(",")
    for line in open(MATERIALS_PATH.joinpath("iris/iris.data")).readlines()[:-1]
]

# Write the `iris.data.pkl` table to RESULTS_PATH.
pickle.dump(data, open(RESULTS_PATH.joinpath("iris.data.pkl"), "wb"))

pprint(data)
```

#### Run the pipeline module named `package`.

The example project contains a pipeline defined in `__main__.py`.  You can run the pipeline by running the installed `package` module.  It uses the [papermill](https://papermill.readthedocs.io/en/latest/index.html) package to run the contents of `/project/package/methods/notebooks/main.ipynb`.  It prints the first 10 lines of the iris dataset to the console.
```bash
python -m package
```

### Create a formal IMRaD-like flat layout Data Science Project using the Cookiecutter

You can use the Cookiecutter package to create a customized instance of The Data Science Project.

#### Install the Cookiecutter package.

```bash
pip install cookiecutter
```

#### Use the Cookiecutter to create a Data Science Project from the cookiecutter branch.

```bash
cookiecutter https://github.com/adamjpatterson/data-science-project.git --checkout formal_flat_layout_cookiecutter
```

#### Complete the Cookiecutter form.

```bash
  [1/6] project_name (project): project
  [2/6] package_name (package): package
  [3/6] repository_url (https://github.com/pypa/sampleproject): https://github.com/pypa/sampleproject
  [4/6] package_description (A small example package): A small example package
  [5/6] author_name (Example Author): Example Author
  [6/6] author_email (author@example.com): author@example.com
```
You can give your project and package the same name.

#### Change directory into the repository's project directory.

This is the top-level directory of a conventional Python package.
```bash
cd <my_project_name>
```

#### Activate your environment if you are using a package manager (e.g., conda).

```bash
conda activate <your-environment>
```

#### Install the package in editable mode.  

An editable install, also known as a development install, will make changes to your package modules immediately available when you restart your kernel.
```bash
pip install -e .
```

### Specify dependencies

You can add dependencies to your project by modifying the `dependencies` section of the `pyproject.toml`.  

#### Add a package dependency to your project.

##### Include the Pandas package.

You can include the `pandas` package, for example, by adding it to the list of `dependencies`.

`pyproject.toml`
```python
...
dependencies = [
    "hatch", 
    "ipykernel", 
    "pandas>=2, <3"
    ]
...
```

#### Reinstall your environment after specifying a new dependency.

```bash
pip install -e .
```

### Create a pipeline

You can use `__main__.py` in order to define your project's pipeline.  Once your package is installed and your pipeline is defined in your `__main__.py` module, you can run your package's pipeline using the `-m` option.
```bash
python -m <your-package-name>
```

### Example

The [`__main__.py`](https://github.com/adamjpatterson/data-science-project/blob/main/project/package/__main__.py) module in this repository shows how you can use [papermill](https://papermill.readthedocs.io/en/latest/index.html) to easily construct a notebook pipeline.

### Publish your package

You can publish your package by following the instructions in the [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/).  Alternatively, you can use the [Hatch](https://hatch.pypa.io/latest/) CLI tool in order to build and publish your project.

## Support

If you have a feature request or run into any issues, feel free to submit an [issue](https://github.com/adamjpatterson/data-science-project/issues) or start a [discussion](https://github.com/adamjpatterson/data-science-project/discussions). You’re also welcome to reach out directly to one of the authors.

- [Adam Patterson](https://github.com/adamjpatterson)

## Development checks

See [the integration test instructions](tests/README.md) for testing both Cookiecutter templates and the formal example across the project branches.
