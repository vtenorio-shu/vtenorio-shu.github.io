# Viviane Martins Tenório — Academic Website

Personal academic website built with Jekyll and hosted on GitHub Pages.
Auto-updates publications weekly via GitHub Actions + Semantic Scholar API.

## 🚀 Quick setup (5 steps)

### 1. Create the GitHub repository

```bash
# On GitHub, create a repo named exactly:
tenorio-vivianesgm.github.io

# Then push this folder:
git init
git add .
git commit -m "Initial site"
git remote add origin https://github.com/tenorio-vivianesgm/tenorio-vivianesgm.github.io.git
git push -u origin main
```

### 2. Enable GitHub Pages

- Go to your repo → **Settings** → **Pages**
- Source: **Deploy from a branch**
- Branch: `main` / `/ (root)`
- Save — your site will be live at `https://tenorio-vivianesgm.github.io`

### 3. Find your Semantic Scholar author ID

Visit: https://www.semanticscholar.org/
Search your name → click your profile → copy the ID from the URL
(e.g. `https://www.semanticscholar.org/author/V.-Tenório/12345678` → ID is `12345678`)

Then edit `scripts/fetch_publications.py` and set:
```python
AUTHOR_ID = "12345678"  # your actual ID
```

### 4. Enable the auto-update workflow

- Go to your repo → **Actions** tab
- Click "I understand my workflows, go ahead and enable them"
- The workflow runs every Monday at 08:00 UTC
- To trigger manually: Actions → "Update Publications" → "Run workflow"

### 5. Run locally (optional)

```bash
gem install bundler
bundle install
bundle exec jekyll serve
# Visit http://localhost:4000
```

## 📁 Structure

```
.
├── _config.yml              # Site settings
├── _data/
│   └── publications.yml     # Auto-updated publication list
├── _layouts/
│   └── default.html         # Page template
├── assets/
│   ├── css/main.css         # All styles
│   └── js/main.js           # Interactions
├── index.html               # Homepage
├── scripts/
│   └── fetch_publications.py  # Publication fetcher
└── .github/
    └── workflows/
        └── update-publications.yml  # Auto-update schedule
```

## ✏️ Updating content

**To add a talk or update bio:** edit `index.html` directly.

**To add a publication manually:** edit `_data/publications.yml`:
```yaml
- title: "Your paper title"
  authors: "Tenório, V.S.G.M., Collaborator, A."
  venue: "Journal or Conference Name"
  year: 2026
  doi: "10.xxxx/xxxxx"   # optional
  type: journal           # or: conference
  tags: [motor control, neural dynamics]
```

**Publication types:** `journal`, `conference`, `thesis`, `preprint`

## 🎨 Customisation

All colours are CSS variables in `assets/css/main.css`:
- `--accent`: warm terracotta (`#c17d5a`) — change to any colour
- `--teal`: secondary accent
- `--cream` / `--warm-white`: backgrounds

## 📬 Contact

tenorio.vivianesgm@gmail.com
