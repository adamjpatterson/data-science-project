"""Integration checks for the repository's three project branches."""
import contextlib
import io
import json
import os
from pathlib import Path
import pickle
import shutil
import subprocess
import sys
import tarfile
import tomllib
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


def render(sources, tmp_path, branch, custom, extra_context=None):
    context = {"project_name": "custom-project"} if custom else {}
    if custom and branch == "formal_flat_layout_cookiecutter":
        context.update({
            "package_name": "custom_package",
            "package_description": 'A "quoted" study using C:\\data',
            "author_name": 'Alice "AJ" Jones',
        })
    context.update(extra_context or {})
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
    env.pop("DATA_SCIENCE_PROJECT_ROOT", None)
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


def execute_notebook(python, env, notebook, cwd, checks=""):
    run(python, "-c", """
import nbformat, sys
from nbclient import NotebookClient
nb = nbformat.read(sys.argv[1], as_version=4)
if sys.argv[2]:
    nb.cells.append(nbformat.v4.new_code_cell(sys.argv[2]))
NotebookClient(nb, timeout=120, kernel_name='python3').execute()
""", notebook, checks, cwd=cwd, env=env)


@pytest.mark.parametrize("custom", [False, True], ids=["defaults", "custom-names"])
def test_informal_template(sources, tmp_path, custom):
    project, _ = render(sources, tmp_path, "informal_layout_cookiecutter", custom)
    for name in ("materials", "methods", "results"):
        assert (project / name / "README.md").is_file()
    python, env = environment(tmp_path)
    install_notebook_tools(python, env, tmp_path)
    execute_notebook(
        python, env, project / "methods/main.ipynb", project / "methods",
        "assert all(p.is_dir() for p in (MATERIALS_PATH, METHODS_PATH, RESULTS_PATH))",
    )


def assert_paths(python, env, cwd, package, project, code_dir):
    run(python, "-c", f"""
from pathlib import Path
import sys
import {package}
from {package}.paths import PROJECT_ROOT, MATERIALS_PATH, METHODS_PATH, RESULTS_PATH
root = Path(sys.argv[1]).resolve()
assert PROJECT_ROOT == root
assert (MATERIALS_PATH, METHODS_PATH, RESULTS_PATH) == tuple(root / name for name in ('materials', 'methods', 'results'))
assert Path({package}.__file__).resolve().parent == Path(sys.argv[2]).resolve()
""", project, code_dir, cwd=cwd, env=env)


def assert_path_error(python, env, cwd, package, message):
    result = subprocess.run([str(python), "-c", f"from {package}.paths import PROJECT_ROOT"],
                            cwd=cwd, env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode != 0
    assert message in result.stderr, result.stderr


@pytest.mark.parametrize("variant", ["example", "defaults", "custom-names"])
def test_formal_distribution(sources, tmp_path, variant):
    if variant == "example":
        project = tmp_path / "project"
        shutil.copytree(sources / "formal_flat_layout/project", project)
        package = "package"
        stale_wheel = project / "dist/previous-0.0.0-py3-none-any.whl"
        stale_wheel.parent.mkdir(exist_ok=True)
        stale_wheel.write_bytes(b"previous build artifact")
    else:
        project, package = render(sources, tmp_path, "formal_flat_layout_cookiecutter",
                                  variant == "custom-names")
    for name in ("materials", "methods", "results"):
        assert (project / name / "README.md").is_file()
        assert not (project / name / "__init__.py").exists()
    assert (project / "methods" / package / "paths.py").is_file()
    # Build the wheel from the sdist, in a clean output directory.
    distributions = tmp_path / "distributions"
    run(sys.executable, "-m", "build", "--outdir", distributions, project, cwd=tmp_path)
    wheel, = distributions.glob("*.whl")
    if variant == "example":
        assert stale_wheel.read_bytes() == b"previous build artifact"
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert f"{package}/paths.py" in names
        assert f"{package}/__main__.py" in names
        assert all(name.startswith((package + "/",)) or ".dist-info/" in name for name in names)
        assert not any(name.endswith((".ipynb", ".pkl", ".data")) for name in names)
        assert not any(name.startswith(f"{package}/{section}/") for name in names
                       for section in ("materials", "methods", "results"))
    python, env = environment(tmp_path)
    install_notebook_tools(python, env, tmp_path, wheel)
    outside = tmp_path / "outside"
    outside.mkdir()
    code_dir = Path(run(python, "-c", f"import {package}; from pathlib import Path; print(Path({package}.__file__).parent)",
                        cwd=outside, env=env).strip())
    assert code_dir.is_relative_to(python.parent.parent)
    # A wheel must not guess a workspace from cwd, even when cwd is a project.
    assert_path_error(python, env, project, package, "DATA_SCIENCE_PROJECT_ROOT")
    run(python, "-m", package, "--help", cwd=outside, env=env)
    for configured, message in [("", "absolute"), ("relative", "absolute"),
                                 (str(tmp_path / "missing"), "must contain")]:
        assert_path_error(python, dict(env, DATA_SCIENCE_PROJECT_ROOT=configured),
                          outside, package, message)

    workspace = tmp_path / "separate-study"
    for name in ("materials", "methods", "results"):
        shutil.copytree(project / name, workspace / name)
    # This workspace contains no source package or pyproject: only study assets.
    shutil.rmtree(workspace / "methods" / package)
    configured = dict(env, DATA_SCIENCE_PROJECT_ROOT=str(workspace))
    assert_paths(python, configured, outside, package, workspace, code_dir)
    checks = "assert all(p.is_dir() for p in (MATERIALS_PATH, METHODS_PATH, RESULTS_PATH))"
    if variant == "example":
        checks += "\nassert iris == data and len(iris) == 150"
    execute_notebook(python, configured, workspace / "methods/notebooks/main.ipynb", outside, checks)
    # The CLI overrides even an invalid environment setting before importing paths.
    run(python, "-m", package, "--project-dir", "../separate-study", cwd=outside,
        env=dict(env, DATA_SCIENCE_PROJECT_ROOT=str(tmp_path / "invalid")))
    if variant == "example":
        result = workspace / "results/iris.data.pkl"
        expected = [line.strip().split(",") for line in
                    (workspace / "materials/iris/iris.data").read_text().splitlines() if line.strip()]
        with result.open("rb") as stream:
            assert pickle.load(stream) == expected
        assert not (project / "results/iris.data.pkl").exists()
        for damaged in (False, True):
            if damaged:
                result.write_bytes(b"incomplete previous output")
            else:
                result.unlink()
            run(python, "-m", package, cwd=outside, env=configured)
            with result.open("rb") as stream:
                assert pickle.load(stream) == expected

    # Editable installs discover their source workspace from any current directory.
    run(python, "-m", "pip", "install", "--no-deps", "--editable", project, cwd=outside, env=env)
    source_code = project / "methods" / package
    assert_paths(python, env, outside, package, project, source_code)
    assert_paths(python, configured, outside, package, workspace, source_code)
    assert_path_error(python, dict(env, DATA_SCIENCE_PROJECT_ROOT=str(tmp_path / "invalid")),
                      outside, package, "must contain")
    execute_notebook(python, env, project / "methods/notebooks/main.ipynb", outside, checks)
    run(python, "-m", package, cwd=outside, env=env)


@pytest.mark.parametrize("value", [
    'A "quoted" value',
    r"C:\new\trials",
    "First line\nSecond line\tRésumé 🧪",
], ids=["quotes", "backslashes", "multiline-unicode"])
def test_template_metadata_round_trip(sources, tmp_path, value):
    context = dict.fromkeys(
        ("author_name", "author_email", "package_description", "repository_url"), value,
    )
    project, _ = render(sources, tmp_path, "formal_flat_layout_cookiecutter", False, context)
    metadata = tomllib.loads((project / "pyproject.toml").read_text())["project"]
    assert metadata["authors"] == [{"name": value, "email": value}]
    assert metadata["description"] == value
    assert metadata["urls"] == {"Homepage": value, "Issues": value + "/issues"}


@pytest.mark.parametrize("ending", ["\n\n", "\n", ""],
                         ids=["blank-line", "newline", "no-newline"])
def test_iris_input_line_endings(sources, tmp_path, ending):
    package = sources / "formal_flat_layout/project"
    original = (package / "materials/iris/iris.data").read_text()
    expected = [line.strip().split(",") for line in original.splitlines() if line.strip()]
    materials = tmp_path / "materials"
    (materials / "iris").mkdir(parents=True)
    results = tmp_path / "results"
    results.mkdir()
    (materials / "iris/iris.data").write_text(original.rstrip("\n") + ending)
    notebook = json.loads((package / "methods/notebooks/main.ipynb").read_text())
    # Exercise the real data-processing cell without starting another kernel.
    cell, = ["".join(cell["source"]) for cell in notebook["cells"]
             if "pickle.dump" in "".join(cell["source"])]
    namespace = {"MATERIALS_PATH": materials, "RESULTS_PATH": results}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(cell, "Iris data-processing cell", "exec"), namespace)
    assert namespace["data"] == expected
    assert len(namespace["data"]) == 150
    with (results / "iris.data.pkl").open("rb") as stream:
        assert pickle.load(stream) == expected
