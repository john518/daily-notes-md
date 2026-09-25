# Daily Notes Markdown (`daily-notes-md`)

A lightweight, local-first daily journal and notes desktop application built for longevity and privacy. Designed to integrate natively into a Git-backed document workflow.

## Key Features

* **Local-First Desktop App:** Powered by Python and `pywebview`, leveraging native OS web rendering for high performance and low resource overhead.
* **Month-at-a-Glance Calendar:** Responsive 4-6 week calendar grid with today highlighting and clean grid styling using Web Awesome components.
* **Daily Entry Previews:** Snippets of daily entries clipped directly onto each calendar cell.
* **Frictionless Editing:** Double-click any day to instantly jump into a dedicated Markdown editor featuring live Edit and Preview tabs.
* **Timeless Storage:** One Markdown file per day (`YYMMDD.md`) stored directly inside a local Git repository.

## Tech Stack

* **Frontend:** Vue.js 3, Vite, Web Awesome, `date-fns`
* **Backend:** Python 3, `pywebview`
* **Data Layer:** Flat-file Markdown + Git version control

## Getting Started

### Prerequisites

* Python 3.10+ with `pip`
* Node.js & npm (for frontend asset building)

### Installation & Development

1. **Clone the repository:**

```bash
   git clone [https://github.com/your-username/daily-notes-md.git](https://github.com/your-username/daily-notes-md.git)
   cd daily-notes-md
```

2. **Setup Python Environment**

```bash
    uv venv --system-site-packages
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    uv pip install pywebview
```

3. **Install frontend dependencies**

```bash
    npm install
    npm run dev
```

4. **Run the app**

```bash
    python main.py
```
