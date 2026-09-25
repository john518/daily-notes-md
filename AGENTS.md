# Repository Instructions for AI Agents (`daily-notes-md`)

This document provides architectural context, constraints, and guidelines for AI coding assistants working on the `daily-notes-md` repository.

## 1. Core Philosophy & Design Principles
* **Local-First & Privacy-Centric:** All data lives locally. No telemetry, no external cloud dependencies, and zero reliance on third-party SaaS APIs.
* **Longevity & Simplicity:** Favor native web technologies, flat files, and maintainable Python code over complex frameworks or opaque database formats.
* **Git-Native:** Data changes should integrate naturally with a local Git workflow.

## 2. Tech Stack Reference
* **Frontend:** Vue.js 3, Vite, Web Awesome components, `date-fns` for calendar math.
* **Backend:** Python 3 with `pywebview` for the native OS desktop window shell.
* **Package Management:** `uv` (with `--system-site-packages` for OS-level GTK/WebKit bindings on Linux).
* **Storage Layer:** Flat Markdown files named using a 6-digit prefix (`YYMMDD.md`, e.g., `260924.md`).

## 3. Configuration & Storage Standards
* **Configuration:** The application reads its root storage directory from a user environment file located at:
  `~/.local/config/john.daily-notes-md/env`
* **Data Storage:** Journal entries reside in the root storage directory specified by the config (defaulting to an XDG-compliant path like `~/.local/share/daily-notes-md/` if unconfigured).
* **Versioning:** The backend should ensure that file writes are structured cleanly so that local Git versioning tracks changes reliably.

## 4. Coding Guidelines for Agents
* **Keep the Bridge Clean:** Communication between the Vue frontend and Python backend happens exclusively via the `window.pywebview.api` bridge. Keep API methods explicit, documented, and lightweight.
* **Avoid Bloat:** Do not introduce heavy ORMs, complex state management libraries (like Pinia/Vuex unless strictly necessary), or external CSS frameworks outside of Web Awesome.
* **Error Handling:** Gracefully handle missing files, uninitialized storage directories, or config lookup failures with clear fallback behaviors.
* **Path Management:** Always use Python's `pathlib` for file system operations to ensure cross-platform safety.
* **Test Environment:** Always use `pytest` for unit test files.
