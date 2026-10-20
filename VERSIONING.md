# Versioning

The Data Science Project versions its two Cookiecutter templates together.
Version **1.0.0** establishes the first stable release of their documented layout,
configuration fields, path helpers, and formal package entry point.

## Compatibility

- **Major**: incompatible changes to documented directory locations, imports,
  configuration fields, path resolution, or command-line behavior.
- **Minor**: backward-compatible features or optional configuration.
- **Patch**: compatible bug fixes and documentation corrections.

Published tags are permanent. Fixes receive a new version; existing release tags
are never moved. Template releases do not automatically modify existing generated
projects or freeze third-party dependencies.

## Tags and branches

| Component | Version 1.0.0 tag | Development branch |
| --- | --- | --- |
| Shared documentation and tests | `v1.0.0` | `main` |
| Formal template | `formal-cookiecutter-v1.0.0` | `formal_flat_layout_cookiecutter` |
| Informal template | `informal-cookiecutter-v1.0.0` | `informal_layout_cookiecutter` |

Use the template tag with Cookiecutter's `--checkout` option for a fixed release.
The branch names select ongoing development. Each tag identifies a separate
commit because the templates live on independent branches. They are not merged
into `main`. The GitHub release on `v1.0.0` links both template tags and records
their full commit IDs in `releases/1.0.0.json`.

GitHub's default source archive for `v1.0.0` contains the documentation and tests.
To obtain a template, use its own tag or the template archives attached to the
release.

## Generated projects

A generated formal Python package starts at **0.0.1**, defined in `__about__.py`.
Its author controls subsequent versions independently of the template version.
The informal template has no Python package version.

## Publishing a release

1. Review both templates and documentation. Run the integration suite against the
   exact template commits, using `PROJECT_TEST_SOURCES` for temporary exports.
2. Record those commits in `releases/<version>.json`; update the release commands
   and version references in the documentation.
3. Commit and push all affected branches, then confirm GitHub CI passes for the
   documentation/test commit and the intended template commits.
4. Create annotated tags for all three commits using the naming scheme above.
   Push the tags without replacing any existing tags.
5. Build template archives from the tagged commits and publish a GitHub release
   on `v<version>` with the manifest, archives, installation commands, and checks.

See `tests/README.md` for validation and instructions to reproduce a release test.
