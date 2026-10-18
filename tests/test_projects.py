"""Integration checks for the repository's three project branches."""
import json
import os
from pathlib import Path
import pickle
import shutil
import subprocess
import sys
import tarfile
import venv
import zipfile

import pytest
from cookiecutter.main import cookiecutter

REPO = Path(__file__).resolve().parents[1]
BRANCHES = (
    "formal_flat_layout",
    "formal_flat_layout_cookiecutter",
    "informal_layout_cookiecutter",
)


def run(*args, cwd, env=None):
    result = subprocess.run(
        [str(arg) for arg in args], cwd=cwd, env=env,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300,
    )
    assert result.returncode == 0, result.stdout
    return result.stdout


@pytest.fixture(scope="session")
def sources(tmp_path_factory):
    """Use explicit working copies when supplied; otherwise export Git refs."""
    root = tmp_path_factory.mktemp("branches")
    override = os.environ.get("PROJECT_TEST_SOURCES")
    for branch in BRANCHES:
        target = root / branch
        if override:
            source = Path(override) / branch
            assert source.is_dir(), f"Missing branch source: {source}"
            shutil.copytree(source, target, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        else:
            ref = f"refs/remotes/origin/{branch}"
            if subprocess.run(["git", "rev-parse", "--verify", ref], cwd=REPO,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
                ref = f"refs/heads/{branch}"
            archive = root / f"{branch}.tar"
            run("git", "archive", "--output", archive, ref, cwd=REPO)
            target.mkdir()
            with tarfile.open(archive) as stream:
                stream.extractall(target, filter="data")
    return root


def render(sources, tmp_path, branch, custom):
    context = {"project_name": "custom-project"} if custom else {}
    if custom and branch == "formal_flat_layout_cookiecutter":
        context["package_name"] = "custom_package"
    project = Path(cookiecutter(
        str(sources / branch), no_input=True, extra_context=context,
        output_dir=str(tmp_path),
        default_config={"replay_dir": str(tmp_path / "replay"),
                        "cookiecutters_dir": str(tmp_path / "cookiecutters")},
    ))
    assert project.name == ("custom-project" if custom else "project")
    for path in project.rglob("*"):
        assert "{{" not in str(path.relative_to(project))
        if path.is_file():
            assert b"{{cookiecutter." not in path.read_bytes(), path
    return project, "custom_package" if custom else "package"


def environment(tmp_path):
    root = tmp_path / "venv"
    venv.EnvBuilder(with_pip=True).create(root)
    python = root / "bin/python"
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PATH"] = f"{root / 'bin'}{os.pathsep}{env.get('PATH', '')}"
    env["JUPYTER_PATH"] = str(root / "share/jupyter")
    env["JUPYTER_CONFIG_DIR"] = str(tmp_path / "jupyter-config")
    env["IPYTHONDIR"] = str(tmp_path / "ipython")
    return python, env


def install_notebook_tools(python, env, tmp_path, *packages):
    run(python, "-m", "pip", "install", "nbclient", "ipykernel", *packages,
        cwd=tmp_path, env=env)
    run(python, "-m", "ipykernel", "install", "--prefix", python.parent.parent,
        "--name", "python3", cwd=tmp_path, env=env)


def execute_notebook(python, env, notebook, cwd):
    run(python, "-c", """
import nbformat, sys
from nbclient import NotebookClient
nb = nbformat.read(sys.argv[1], as_version=4)
NotebookClient(nb, timeout=120, kernel_name='python3').execute()
""", notebook, cwd=cwd, env=env)


@pytest.mark.parametrize("custom", [False, True], ids=["defaults", "custom-names"])
def test_informal_template(sources, tmp_path, custom):
    project, _ = render(sources, tmp_path, "informal_layout_cookiecutter", custom)
    for name in ("materials", "methods", "results"):
        assert (project / name / "README.md").is_file()
    python, env = environment(tmp_path)
    install_notebook_tools(python, env, tmp_path)
    execute_notebook(python, env, project / "methods/main.ipynb", project / "methods")


@pytest.mark.parametrize("variant", ["example", "defaults", "custom-names"])
def test_formal_distribution(sources, tmp_path, variant):
    if variant == "example":
        project = tmp_path / "project"
        shutil.copytree(sources / "formal_flat_layout/project", project)
        package = "package"
        (project / package / "results/iris.data.pkl").unlink(missing_ok=True)
    else:
        project, package = render(sources, tmp_path, "formal_flat_layout_cookiecutter",
                                  variant == "custom-names")
    # build's default builds the wheel from the sdist, checking both distributions.
    run(sys.executable, "-m", "build", project, cwd=tmp_path)
    wheel, = (project / "dist").glob("*.whl")
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert f"{package}/methods/notebooks/main.ipynb" in names
        if variant == "example":
            assert f"{package}/materials/iris/iris.data" in names
            assert f"{package}/results/iris.data.pkl" not in names
    python, env = environment(tmp_path)
    install_notebook_tools(python, env, tmp_path, wheel)
    outside = tmp_path / "outside"
    outside.mkdir()
    output = run(python, "-c", f"""
import json
import {package}
from {package}.materials import MATERIALS_PATH
from {package}.methods import METHODS_PATH
from {package}.results import RESULTS_PATH
assert all(p.is_dir() for p in (MATERIALS_PATH, METHODS_PATH, RESULTS_PATH))
print(json.dumps(str(METHODS_PATH.parent)))
""", cwd=outside, env=env)
    installed = Path(json.loads(output.strip()))
    assert installed.is_relative_to(python.parent.parent)
    execute_notebook(python, env, installed / "methods/notebooks/main.ipynb", outside)
    if variant == "example":
        result = installed / "results/iris.data.pkl"
        result.unlink()  # The pipeline itself must recreate the output.
        run(python, "-m", package, cwd=outside, env=env)
        with result.open("rb") as stream:
            rows = pickle.load(stream)
        expected = [line.split(",") for line in
                    (installed / "materials/iris/iris.data").read_text().splitlines() if line]
        assert rows == expected
        assert len(rows) == 150
        assert all(len(row) == 5 for row in rows)
