# Integration tests

Run on Linux or macOS with Python 3.11 or newer:

```bash
python -m venv /tmp/data-science-project-tests
/tmp/data-science-project-tests/bin/python -m pip install -r requirements-test.txt
/tmp/data-science-project-tests/bin/python -m pytest -v tests
```

The suite renders both Cookiecutter templates with default and custom names,
executes their notebooks, and builds and installs the formal packages in separate
virtual environments. Builds use a separate temporary output directory so existing
`dist` artifacts cannot interfere. Wheels are built from source distributions,
then replaced with editable installs to check the documented development workflow. Notebook
checks verify the resulting data and workspace paths as well as successful execution.
Wheel checks confirm that study assets are excluded, require an explicit workspace,
and execute notebooks in a separate study without a source package. Editable
installs must discover their own workspace from an unrelated current directory.
Tests also cover invalid and overriding environment settings, CLI precedence,
and configurable package names.
The formal example pipeline must regenerate its Iris output from the bundled
data when the output is missing or damaged. Source branches and their existing
notebook outputs are never modified. Regression checks also cover quoted,
backslash-containing, and multiline Unicode metadata, plus dataset files with
or without a final newline or blank line.

By default, tests export the three template/example branches from local
`origin/*` refs (falling back to local branches when a remote ref is absent).
Fetch first when you want to test the latest remote commits. To test uncommitted
worktrees instead, set `PROJECT_TEST_SOURCES` to a directory containing one
subdirectory or symlink per branch, named exactly like the branch. All sources
are copied into temporary test directories before use.

CI runs on main-branch pushes and pull requests, manually, and weekly. Each run
checks all three project branches. Changes made only on a template branch are
covered by the next scheduled or manual run. Network access is required to install
build tools and dependencies. These checks validate Python 3.11 in CI; they do not
establish compatibility with every Python version advertised by the templates.

The three project branches are independent, long-lived layouts and templates.
They are not feature branches to merge into `main`; `main` holds the shared
documentation and tests.
