# Repository Guidelines

## Project Structure & Module Organization
- `addon/`: NVDA add-on payload.
  - `addon/appModules/kakaotalk.py`: app module logic (KakaoTalk UIA list-item focus handling).
  - `addon/manifest.ini`: add-on metadata consumed by NVDA.
  - `addon/doc/`: end-user docs (HTML/Markdown per language, e.g. `addon/doc/en/`).
- Build system: `sconstruct` (SCons entrypoint), `buildVars.py` (add-on metadata), `site_scons/` (NVDA SCons tools).
- Automation: `.github/workflows/` (build + release pipeline).

## Build, Test, and Development Commands
Recommended local setup (PowerShell):
- Create venv: `python -m venv .venv` then activate `.\.venv\Scripts\Activate.ps1`
- Install tools: `pip install scons markdown pre-commit ruff pyright`
- Build add-on: `scons` (outputs `*.nvda-addon` in repo root)
- Dev build (timestamped version): `scons dev=1`
- i18n template: `scons pot` (and `scons mergePot` when updating translations)
- Clean build outputs: `scons -c`

CI runs `pre-commit run --all-files` and builds the add-on on PRs.

## Coding Style & Naming Conventions
- Indentation: tabs (Ruff formatter enforces this); max line length is 110.
- Format + lint: `ruff format .` then `ruff check .` (or `ruff check --fix .`)
- Type checking: `pyright` (strict settings in `pyproject.toml`)
- Naming: modules `snake_case.py`, classes `CamelCase`, and app modules live in `addon/appModules/`.

## Testing Guidelines
There is no unit-test suite today. Validate changes by:
1) Building (`scons`), 2) installing the generated `.nvda-addon` into NVDA, and 3) navigating KakaoTalk lists (Contacts/Chats/Messages) to confirm items are announced and focus does not freeze.
Include NVDA log excerpts when reporting or fixing regressions.

## Commit & Pull Request Guidelines
- Prefer conventional commit prefixes when practical (e.g. `feat:`, `fix:`, `chore:`) with an imperative, concise subject.
- PRs should include: summary, manual test steps (NVDA + KakaoTalk), and user-visible behavior notes. Keep generated artifacts out of commits (`*.nvda-addon`, `*.mo`, `*.pot` are ignored by `.gitignore`).
