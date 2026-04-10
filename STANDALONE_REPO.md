# Moving `retrodocs` to its own Git repository

The docs site repo is **[github.com/omiq/retrodocs](https://github.com/omiq/retrodocs)** (public). CI runs on every push via [`.github/workflows/ci.yml`](https://github.com/omiq/retrodocs/actions/workflows/ci.yml).

The TRSE compiler stays in **[github.com/omiq/trse](https://github.com/omiq/trse)** (or upstream [leuat/TRSE](https://github.com/leuat/TRSE)); that is a different repository from the documentation site.

## First push from the TRSE monorepo

If `retrodocs/` still lives under a full TRSE clone and GitHub already has the empty `omiq/retrodocs` placeholder:

```bash
cd /path/to/TRSE
git fetch origin
git subtree split -P retrodocs -b retrodocs-only
git push https://github.com/omiq/retrodocs.git retrodocs-only:main
```

Use `--force` on the push only if you must replace what is on `main` (e.g. the initial README/LICENSE commit) and you accept overwriting it.

Alternatively, copy the folder into a fresh clone of `omiq/retrodocs`, commit, and push — no subtree history.

## Why a second repo?

- Clear issues/PRs for documentation only  
- Independent permissions and releases  
- Smaller clone for contributors who only edit docs  

## Splitting history from the monorepo (optional)

From the **TRSE** repository root (with full history):

```bash
# Create a branch that contains only retrodocs/ history (Git 2.22+)
git subtree split -P retrodocs -b retrodocs-only
```

Create an empty repo on GitHub (e.g. `omiq/retrodocs`), then:

```bash
git remote add retrodocs https://github.com/omiq/retrodocs.git
git push retrodocs retrodocs-only:main
```

Alternatively, **copy** the `retrodocs/` tree into a fresh repo without history (`git init`, add, commit, push). That is simpler if you do not need subtree history.

## TRSE sources for auto-generated pages

`deploy.sh` and the import scripts read **TRSE’s** `resources/text/` and `units/` to regenerate:

- `docs/trse/reference/methods/` (from `syntax.txt` + help RTFs)  
- `docs/trse/reference/units/` (from `units/**/*.tru`)  

In the **monorepo**, those paths are found by walking up from `retrodocs/scripts/` to the TRSE root.

In a **standalone** `retrodocs` clone, that walk fails unless you point at a TRSE checkout.

### Option A — sibling directories (local / CI)

```bash
git clone https://github.com/omiq/trse.git ../trse
git clone git@github.com:omiq/retrodocs.git
cd retrodocs
export TRSE_REPO_ROOT="$(cd ../trse && pwd)"
source .venv/bin/activate
python3 scripts/import_trse_reference.py --skip-init
python3 scripts/import_trse_units.py
mkdocs build
```

### Option B — explicit `TRSE_REPO_ROOT`

Same as above; `deploy.sh` picks it up automatically:

```bash
export TRSE_REPO_ROOT=/path/to/TRSE
./deploy.sh
```

### Option C — `--repo-root`

```bash
python3 scripts/import_trse_reference.py --skip-init --repo-root /path/to/TRSE
python3 scripts/import_trse_units.py --repo-root /path/to/TRSE
```

### Skip regeneration

If you only change Markdown/CSS and not TRSE upstream:

```bash
SKIP_TRSE_IMPORT=1 ./deploy.sh
```

(Or use committed `docs/trse/reference/` as-is.)

## What changed in the scripts for standalone use

- **`import_trse_units.py`** always writes under **this repo’s** `docs/` (next to `scripts/`), never under `TRSE/retrodocs/docs`.  
- Both imports accept **`TRSE_REPO_ROOT`** as well as **`--repo-root`**.

## After the move

1. Remove or adjust any **CI** in the TRSE repo that assumed `retrodocs` lived inside it.  
2. Add CI to the **new** docs repo (e.g. `mkdocs build` on push).  
3. Optionally add **`trse`** as a **submodule** or checkout step in CI so `TRSE_REPO_ROOT` is deterministic.
