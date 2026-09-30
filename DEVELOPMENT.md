# Development, Environment & Git Workflow Guide

This document summarizes the technical setup, package management conventions with [`uv`](https://github.com/astral-sh/uv), and version control practices with Git and GitHub for the `pachycephalosaur-biomechanics` repository.

---

## ⚡ 1. Python Environment Management with `uv`

The project uses **[`uv`](https://github.com/astral-sh/uv)** (by Astral) for fast, deterministic, cross-platform Python virtual environment and dependency management.

### Key Configuration Files
- [`pyproject.toml`](pyproject.toml): Declares build system (`hatchling`), core dependencies (`numpy`, `scipy`, `pyvista`, `trimesh`, `pydicom`, `tetgen`, etc.), optional dev dependencies (`pytest`, `jupyterlab`), and package discovery paths (`src/stegoceras_biomechanics`).
- `uv.lock`: Fully pinned, cryptographically hashed lockfile ensuring byte-for-byte reproducible virtual environments across machines.
- `.venv/`: The local virtual environment directory created and managed by `uv` (excluded from git).

### Daily Commands

| Task | Command | Description |
| :--- | :--- | :--- |
| **Sync Environment** | `uv sync --all-extras` | Installs/updates all pinned dependencies and installs the `stegoceras_biomechanics` package in editable mode. |
| **Run Python Scripts** | `uv run python scripts/<script_name>.py` | Executes a script within the virtual environment without needing manual activation (`source .venv/bin/activate`). |
| **Run Test Suite** | `uv run pytest -v` | Runs all automated unit and regression tests in [`tests/`](tests/). |
| **Run Specific Test** | `uv run pytest tests/test_gate_b_registration.py -v` | Runs an isolated test module. |
| **Launch JupyterLab** | `uv run jupyter lab` | Starts JupyterLab with all project modules available in the Python kernel. |
| **Add Dependency** | `uv add <package>` | Adds a package to `pyproject.toml` and updates `uv.lock`. |
| **Add Dev Dependency**| `uv add --dev <package>` | Adds a tool or test dependency to the `dev` optional dependencies. |

---

## 🐙 2. Git & GitHub Workflow

### Remote & Branching
- **Primary Remote**: `origin` (`git@github-mdhornstein:mdhornstein/pachycephalosaur-biomechanics.git`)
- **Default Branch**: `main`
- All changes are synchronized with the remote via:
  ```bash
  git push origin main
  ```

### Commit Message Conventions
Commits follow semantic prefixes to distinguish the type of work:
- `feat:` New computational capability, pipeline script, or analysis module (e.g. `feat(phase5): complete Gate A DICOM volume ingestion`).
- `fix:` Bug fix or numerical correction (e.g. `fix(viz): upgrade 3D cranial rendering engine to PyVista`).
- `docs:` Documentation updates, handoffs, or state synchronization (e.g. `docs: finalize post-audit state synchronization`).
- `test:` Adding or refining regression tests (e.g. `test(phase4): add element-level manufactured displacement test`).
- `audit:` Forensic audits, review reconciliations, or provenance packages.
- `refactor:` Code reorganization without behavioral or numerical changes.
- `chore:` Maintenance tasks, environment updates, or provenance verification reruns.

### Core Repository Invariants

1. **Frozen Computational Baselines**:
   - Completed phases and gates (Phases 1–4, Phase 5 Gates A–C) are **computationally frozen**.
   - Do **NOT** rerun long-running solves or re-generate numerical artifacts in [`results/`](results/) or [`simulations/`](simulations/) unless explicitly authorized for a verified provenance check.
2. **Decoupling Execution from Documentation**:
   - Separate computational execution commits (which produce/verify code and numerical artifacts) from documentation/synthesis report commits whenever feasible.
3. **Clean Working Tree**:
   - Always verify `git status --short` before and after operations.
   - Do not leave temporary scripts, untracked files, or scratch artifacts inside the workspace.
4. **Pre-Commit Verification**:
   - Inspect diff stats before committing:
     ```bash
     git diff --stat
     git status --short
     ```
   - Ensure that raw CT files ([`data/raw/`](data/raw/)), binary meshes, or frozen solution arrays were not unintentionally modified or staged.

### Useful Git Commands
- **View last commit details & diff**:
  ```bash
  git show
  ```
- **View pure diff of most recent commit**:
  ```bash
  git diff HEAD~1 HEAD
  ```
- **View summary of changed files in last commit**:
  ```bash
  git show --stat
  ```
- **Check differences against upstream branch**:
  ```bash
  git status
  ```

---

## 🏛️ 3. Repository Architecture & Document System

The repository maintains strict separation of roles across documents to eliminate drift and confusion:

| Document / Path | Role | Function / Rule |
| :--- | :--- | :--- |
| **[`README.md`](README.md)** | Public Overview | Timeless repository introduction, scientific motivation, and layout. |
| **[`HANDOFF.md`](HANDOFF.md)** | Operational Orientation | Fast, compact living operational entry point for incoming researchers/agents; describes current HEAD reality and immediate next action. |
| **[`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)** | Living Scientific Truth | Canonical, detailed single source of truth on the active model, verified metrics, boundary conditions, and limitations. |
| **[`PLAN.md`](PLAN.md)** | Master Research Roadmap | Forward-looking phase index and gate milestones; defines where the project is going. |
| **[`docs/phase_design/`](docs/phase_design/)** | Pre-Execution Designs | Methodological blueprints specifying variables, hypotheses, and acceptance criteria *before* execution (or explicit retrospective reconstructions). |
| **[`reports/`](reports/)** | Milestone Reports | Permanent, comprehensive scientific records documenting what was actually executed, observed, and concluded. |
| **[`docs/DECISIONS.md`](docs/DECISIONS.md)** | Decision Ledger | Append-only register recording major scientific and architectural choices (`D001`–`D017`). |
| **[`docs/RESEARCH_TRACEABILITY.md`](docs/RESEARCH_TRACEABILITY.md)** | Master Traceability Map | End-to-end cryptographic and procedural linkage connecting scientific questions to code, data, tests, and reports. |

---

## 🧪 4. Testing & Quality Assurance

Automated tests in [`tests/`](tests/) guard against numerical drift, broken links, schema regressions, and coordinate inconsistencies:

```bash
# Run the complete test suite
uv run pytest -v

# Run Gate-specific suites
uv run pytest tests/test_gate_a_dicom.py -v
uv run pytest tests/test_gate_b_registration.py -v
uv run pytest tests/test_gate_c_semantics.py -v
```

Before declaring any gate or milestone complete:
1. All relevant unit and regression tests must pass cleanly.
2. Relative markdown links in created/modified documents must be validated.
3. Git state must be clean, verified, and committed with an informative message.
