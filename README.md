# Daily Notes Markdown (`daily-notes-md`)

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![pywebview](https://img.shields.io/badge/pywebview-GUI-4B8BBE?style=flat&logo=python&logoColor=white)](https://pywebview.flowehip.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=flat&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-Frontend-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)

A lightweight, local-first daily journal and notes desktop application built for longevity and privacy. Designed to integrate natively into a Git-backed document workflow. It is intended for developers who are comfortable building the app using npm and running from python. It has only been used on linux (Ubuntu) systems, and might need some tweaking for other OS platforms.

<img src="./docs/images/DailyNotesMarkdown.png" width="1076" alt="Screenshot">

## Key Features

* **Local-First Desktop App:** Powered by Python and `pywebview`, leveraging native OS web rendering for high performance and low resource overhead.
* **Month-at-a-Glance Calendar:** Responsive 4-6 week calendar grid with today highlighting and clean grid styling using Web Awesome components.
* **Daily Entry Previews:** Snippets of daily entries clipped directly onto each calendar cell.
* **Frictionless Editing:** Double-click any day to instantly jump into a dedicated Markdown editor featuring live Edit and Preview tabs.
* **Timeless Storage:** One Markdown file per day (`YYMMDD.md`) stored directly inside a local Git repository.

## Tech Stack

* **Frontend:** Vue.js 3, Vite
* **Backend:** Python 3, `pywebview`
* **Data Layer:** Flat-file Markdown + Git version control

## Storage

No databases were used in the development of this app :)

Instead, journal entries are organized in a hierarchical YY/MM/YYMMDD.md structure beneath a configurable DATA_DIR. The root data directory is resolved from the environment configuration file at `~/.config/john.daily-notes/env`, supporting environment variable expansion like ${HOME}, with a fallback default for development testing.

## Getting Started

### Prerequisites

* Python 3.14+ with `uv`
* Node.js & npm (for frontend asset building)

### Installation & Development

1. **Clone the repository:**

```bash
   git clone [https://github.com/your-username/daily-notes-md.git](https://github.com/your-username/daily-notes-md.git)
   cd daily-notes-md
```

2. **Setup Python Environment**

Be sure to use system python and site packages. These are needed for pywebview to access system graphics (GTK).

```bash
    uv venv --python /usr/bin/python3 --system-site-packages --clear
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    uv pip install pywebview
```

3. **Build frontend in client subdirectory**

```bash
    cd client
    npm install
    npm run build
    cd ..
```

4. **Run the app**

You can run without activating the venv or installing the app by calling python explicitly and setting PYTHONPATH to the root directory:

```bash
    PYTHONPATH=. ./.venv/bin/python -u -m daily_notes.main
```

Here is the complete **Linux Desktop Setup** section formatted as a single, ready-to-copy markdown block:

## Linux Desktop Setup

This project is configured for a native Linux desktop experience (tested on Wayland/GNOME). To integrate the app launcher and titlebar icons cleanly, follow the steps below.

### 1. Icon Asset Generation

* **Source:** Downloaded the "Calendar Month" icon as an SVG from [Google Fonts - Material Symbols](https://fonts.google.com/icons).
* **Customization:** Opened `calendar_month.svg` and changed the path `fill` attribute to a high-contrast color (e.g., `fill="#2563eb"`) since default Google assets are optimized for dark-mode web contexts. The modified svg file is included in this repository at `client/src/assets/calendar_month.svg`.
* **Conversion:** Rendered at a high density (`300` DPI) using ImageMagick to prevent pixelation when scaling:
```bash
  convert -density 300 calendar_month.svg -background none -resize 256x256 -gravity center -extent 256x256 icon.png
```

### 2. Icon Placement

Move the generated PNG into the local user icon theme hierarchy so GTK and the desktop environment can reference it by name:

```bash
mkdir -p ~/.local/share/icons/hicolor/256x256/apps
cp assets/icon.png ~/.local/share/icons/hicolor/256x256/apps/daily-notes.png
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor
```

### 3. Desktop Application Entry

Create the desktop entry file to register the app in your system launcher and map the window class correctly:

* **Path:** `~/.local/share/applications/daily-notes.desktop`
* **Contents:**
```ini
[Desktop Entry]
Type=Application
Name=Daily Notes
Comment=Local-first daily journal
Exec=daily-notes
Icon=daily-notes
Terminal=false
Categories=Utility;Office;
StartupWMClass=daily-notes.py
```

We can don't need paths for `Exec` and `Icon` because they are in standard locations:

  - `$HOME/.local/bin/daily-notes`
  - `$HOME/.local/share/icons/hicolor/256x256/apps/daily-notes.png`


*(Note: `StartupWMClass` is mapped to match the active window process identifier).*
* **Update Database:**

```bash
update-desktop-database ~/.local/share/applications/
```

### 4. Executable Wrapper Script & Project Structure

* **Naming Convention:** The main script file is named explicitly (`daily-notes.py`) rather than a generic `main.py` to prevent Wayland window class collisions across local projects.
* **Wrapper Path:** `~/.local/bin/daily-notes`

```bash
#!/bin/bash
python3 /home/john/projects/05-lab/git/daily-notes-md/daily-notes.py "$@"

```
