# Creating a release

Releases are built from a verified Git tag. The HACS archive contains the
integration directly at its root and is published together with a SHA-256
checksum file.

## 0.8.1 maintenance release

I prepared this release from the v0.8.0 tag, commit
`eea30744b9cb86c618a55125658d7bd36e75f5da`. It backports the timezone correction
merged in PR #65, without the startup recovery or season-switching beta work.
The maintenance PR targets a separate branch rooted at v0.8.0 so its diff and
CI checks cover precisely the code intended for stable users.

I verified 1,024 tests with 96.05% combined statement and branch coverage using
Python 3.14.2, HA 2026.9.4 and the development versions pinned by v0.8.0.
Ruff 0.16.9 formatting/lint and strict Mypy 2.3.1 passed. There were no physical
appliance writes. The release workflow must pass before publication, and the
published archive and checksum must match the locally built Linux package.

The development branch also contains the fix through PR #65. Its separate
HA 2026.10.0b4 test environment passed 1,146 cases with 96.35% combined
coverage. This is development-branch evidence, not a claim that the maintenance
archive was tested with that environment.

## Local release checks

Run the following commands from the repository root:

```bash
ruff format --check .
ruff check .
mypy
pytest
python -m venv .audit-venv
.audit-venv/bin/python -m pip install -e ".[security]"
.audit-venv/bin/python -m pip freeze --exclude-editable > .audit-venv/requirements.txt
.audit-venv/bin/python -m pip_audit --strict --requirement .audit-venv/requirements.txt
python scripts/build_release.py --expected-version <version>
```

Use `.audit-venv\Scripts\python.exe` instead on Windows. Keeping the audit in a
clean environment prevents Home Assistant's test-only dependency set from
being mistaken for the integration's runtime dependencies.

The official HACS and hassfest validation requires Docker. If Docker is not
available locally, publication remains gated: the tag-triggered GitHub
workflow runs both checks before creating a release.

After the build, `dist/bosch_buderus_heating.zip` and
`dist/bosch_buderus_heating.zip.sha256` must exist. For an additional check,
extract the ZIP into an empty directory. `manifest.json` must be located at the
archive root.

## Publication

1. Ensure that the version in `manifest.json`, `pyproject.toml`, and the
   heading in `CHANGELOG.md` match.
2. Require a clean working tree and successful local checks.
3. Push the verified state to GitHub only after explicit release approval.
4. Create and push the signed or annotated version tag.

The tag starts the release workflow. It repeats tests, type checks, formatting,
linting, dependency auditing, hassfest, and HACS validation. Only then does it
create the GitHub release with the ZIP and checksum.

## Field validation

I am releasing 0.8.0 as stable after an initial local check in which beta.3
appeared to work. Apart from the version number, the integration code and
packaged assets match beta.3. The release includes all changes from the
three 0.8.0 betas, including the maintenance updates.

My initial check does not establish that every affected scenario has been
tested. A 48-hour connection test, preservation of the expected solar
entities after restart and reload on the affected installation, and the
retained fault details and timestamps still need specific confirmation.
The original cause of the connection loss in #49 has not been established.
Issues #36, #48 and #49 remain open for that feedback.

I tested beta.1 on my installation: notifications appeared when faults
occurred and changed to resolved when they cleared. Retained details are
kept only for the visible message and are cleared on dismissal, disabling
notifications, unloading or restart. Solar entities belong to the gateway
device. These checks do not require appliance writes or deliberately
triggering a fault.

Existing field feedback includes a Buderus installation
with a K40 gateway and an installation with two heating circuits whose reporter
confirmed the expected controls and changes appearing in MyBuderus. That report
does not enumerate every tested control or confirm restoration of every value.
Bosch systems, additional gateway and multi-source configurations, and long-term
operation still need broader field evidence. A stable release does not imply
that every supported function has been tested on every installation.
The holiday-input corrections in 0.7.2 still need confirmation on a physical
installation after an update and restart.
