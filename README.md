# Mark2PDF

A split-pane Markdown editor with live preview and one-click PDF export. Built with Flask and WeasyPrint.

![Design inspired by Mermaid Studio](https://img.shields.io/badge/design-Obsidian%20Terminal-A6FF00?style=flat&labelColor=0e0e0e)
![Python](https://img.shields.io/badge/python-3.8+-A6FF00?style=flat&labelColor=0e0e0e)
![Flask](https://img.shields.io/badge/flask-latest-A6FF00?style=flat&labelColor=0e0e0e)

## Features

- **Live preview** — rendered as you type via `marked.js`
- **Bidirectional scroll sync** — editor and preview stay in lockstep
- **PDF export** — server-side via WeasyPrint; tables stay together across pages
- **Auto filename** — PDF named after the first `# H1` heading
- **3 themes** — Obsidian (dark), Monochrom, GitHub
- **Persistent editor** — content saved to `localStorage`

## Stack

| Layer | Tech |
|-------|------|
| Server | Flask |
| Markdown → HTML (PDF) | Python `markdown` lib |
| Markdown → HTML (preview) | `marked.js` |
| PDF rendering | WeasyPrint |
| Fonts | Space Grotesk, Manrope, JetBrains Mono |

## Getting Started

**Requirements:** Python 3.8+, and WeasyPrint's native deps (Pango, Cairo, GDK-PixBuf).

```bash
# Install system deps (Fedora/RHEL)
sudo dnf install pango cairo gobject-introspection

# Install system deps (Debian/Ubuntu)
sudo apt install libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0

# Set up and run
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## Architecture

Two independent Markdown rendering stages — browser preview and server PDF are not shared:

```
Browser                          Server
──────                           ──────
marked.js → HTML preview         markdown lib → HTML → WeasyPrint → PDF
localStorage ← editor content
```

Editing PDF appearance → `app.py` inline `<style>` block  
Editing preview appearance → `static/style.css`
