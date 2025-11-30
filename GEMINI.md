# Project Context: KakaoTalk Accessible NVDA Add-on

## Overview
This project is an **NVDA (NonVisual Desktop Access) add-on** designed to improve the accessibility of the KakaoTalk desktop application. It functions by customizing how NVDA interacts with KakaoTalk's window controls, specifically forcing the use of MSAA (Microsoft Active Accessibility) over UIA (User Interface Automation) for certain list controls to prevent freezing and accessibility issues.

## Architecture & Key Files
*   **Core Logic:** `addon/appModules/kakaotalk.py`
    *   Inherits from `appModuleHandler.AppModule`.
    *   `isGoodUIAWindow`: Determines whether to use UIA or MSAA for specific window classes (e.g., `EVA_Menu`, `EVA_VH_ListControl_Dblclk`).
    *   `script_dumpFocus`: A debug tool to log focus ancestry and children (bound to `Control+Shift+K`).
*   **Build Configuration:**
    *   `sconstruct`: The main build script using SCons. Handles compilation of translations, documentation, and packaging into `.nvda-addon`.
    *   `buildVars.py`: Central configuration for add-on metadata (version, name, author, excluded files, etc.).
*   **Configuration:**
    *   `pyproject.toml`: Configures development tools like **Ruff** (linter/formatter) and **Pyright** (type checker).
    *   `.github/workflows/build_addon.yml`: CI pipeline definition for building and releasing the add-on.

## Development Setup
1.  **Prerequisites:**
    *   Python 3.11+ (3.13 recommended).
    *   SCons (`pip install scons`).
    *   Markdown (`pip install markdown`).
    *   GNU Gettext tools (for translations).
2.  **Dependencies:**
    *   Install Python dependencies: `pip install -r requirements.txt` (Note: create this file based on tools if needed, or just install manually).
    *   Standard tools: `ruff`, `pyright`.

## Building and Running
*   **Build Add-on:**
    ```powershell
    scons
    ```
    This generates a `.nvda-addon` file in the root directory.
*   **Generate Translation Template (.pot):**
    ```powershell
    scons pot
    ```
*   **Clean Build:**
    ```powershell
    scons -c
    ```
*   **Development Build (Dev Version):**
    ```powershell
    scons dev
    ```

## Code Style & Conventions
*   **Linting:** The project uses **Ruff**.
    *   Run checks: `ruff check .`
    *   Format code: `ruff format .`
*   **Type Checking:** The project uses **Pyright**.
    *   Run checks: `pyright`
*   **Indentation:** **Tabs** are used for indentation (enforced by Ruff config).
*   **Line Length:** 110 characters.
*   **Strings:** Double quotes prefered.
*   **Imports:** Sorted standard library, then third party, then local.

## Workflow
1.  Modify code in `addon/`.
2.  Update `buildVars.py` if changing metadata or version.
3.  Run `scons` to build the package.
4.  Test the `.nvda-addon` file by installing it into a local NVDA instance.

## Agent Instructions
*   **Auto-Build:** You must automatically run `scons` to rebuild the add-on after any modification to the source code.
*   **Documentation:** Always record changes, experiments, and lessons learned in the "Notes" section of this file (`GEMINI.md`) to ensure context is preserved across sessions.

## Notes
*   **2025-11-30**: Attempted to fix list reading by returning `False` in `isGoodUIAWindow` for `EVA_VH_ListControl_Dblclk`.
    *   **Result**: FAILURE. The window lost NVDA focus entirely.
    *   **Lesson**: Do not disable UIA for `EVA_VH_ListControl_Dblclk` via `isGoodUIAWindow`. It breaks focus.
    *   **Current State**: `isGoodUIAWindow` logic reverted to return `True`. Need to find an alternative way to make lists accessible (likely by inspecting the UIA tree or using an overlay).
*   **2025-11-30 (Attempt 2)**: Analyzed UIA tree. Items are present (Role 15, `EVA_VH_ListControl_Dblclk`) but only get `SELECTED` state, not `FOCUSED`. Parent container keeps `FOCUSED` state.
    *   **Action**: Implemented `KakaoListItem` overlay class. Overrode `event_UIA_elementSelected` to call `api.setFocusObject(self)` when `SELECTED` state is present.
    *   **Goal**: Force NVDA to treat the selected item as the focus, bypassing the parent's focus retention.
