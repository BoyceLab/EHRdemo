# MkDocs + GitHub Pages Setup Walkthrough

A step-by-step guide to getting the ARC Clinical Browser demo site deployed with ALS TDI branding.

---

## What you'll have at the end

A live public site at `https://YOUR-USERNAME.github.io/YOUR-REPO/` with:

- A branded home page in Catalyst Purple and Foundation Navy
- An embedded live demo with synthetic patient data
- Pages explaining the pipeline, adoption guide, and privacy
- Auto-deployment whenever you push to `main`
- A separate `gh-pages` branch (auto-managed by MkDocs) that GitHub Pages serves

---

## Step 1: Understand the two branches

GitHub Pages with MkDocs uses **two branches**:

| Branch | What lives there | Who edits it |
|---|---|---|
| `main` | Source files: `mkdocs.yml`, the `docs/` folder, the dashboard files | You — manually |
| `gh-pages` | Auto-built HTML site that GitHub serves | MkDocs — never edit by hand |

**Key rule:** never edit `gh-pages` directly. The `mkdocs gh-deploy` command rebuilds it from `main` and force-pushes, overwriting any manual changes.

If you've already put files in the `gh-pages` branch, that's OK — they'll get replaced on the first auto-deployment. Move them to `main` instead.

---

## Step 2: Lay out your repository

On your `main` branch, your repo should look like this:

```
your-repo/
├── mkdocs.yml                          ← top-level config
├── README.md                            ← repo readme (separate from site content)
├── .github/
│   └── workflows/
│       └── deploy.yml                   ← GitHub Actions auto-deploy
└── docs/                                ← all site content lives here
    ├── index.md                         ← home page
    ├── demo.md                          ← live demo page
    ├── pipeline.md                      ← about the pipeline
    ├── adopt.md                         ← adoption guide
    ├── privacy.md                       ← privacy / synthetic data
    ├── dashboard_demo.html              ← the dashboard itself
    ├── demo_dashboard_data.json         ← synthetic data bundle
    ├── stylesheets/
    │   └── alstdi-brand.css             ← brand CSS overrides
    └── assets/
        ├── logo.svg                     ← header logo
        └── favicon.svg                  ← browser tab icon
```

Anything in `docs/` becomes part of the published site. The dashboard and JSON files sit alongside the Markdown so the iframe in `demo.md` can reach them via a relative URL.

---

## Step 3: Install everything locally

You need this for previewing changes before pushing.

### Install Python (skip if you already have it)

If you don't have Python 3.10+ already, download it from [python.org](https://www.python.org/downloads/). On Windows, check "Add Python to PATH" during install.

### Install MkDocs and the Material theme

In a terminal (PowerShell, Command Prompt, or VS Code terminal):

```bash
pip install mkdocs-material
```

Verify:

```bash
mkdocs --version
```

Should print something like `mkdocs, version 1.6.x`.

---

## Step 4: Drop in the files I provided

I've prepared a ready-to-go MkDocs site in the `mkdocs_site/` folder of the deliverables. Copy the contents into your repo's `main` branch:

```bash
cd path/to/your-repo

# Copy everything I provided
cp -r path/to/mkdocs_site/mkdocs.yml ./
cp -r path/to/mkdocs_site/docs ./

# Move the GitHub Actions workflow into the right place
mkdir -p .github/workflows
cp path/to/mkdocs_site/.github_workflows_deploy.yml .github/workflows/deploy.yml

# Add the dashboard files
cp path/to/dashboard_demo.html docs/
cp path/to/demo_dashboard_data.json docs/
```

(On Windows, use Explorer to copy files instead of `cp` if that's easier.)

---

## Step 5: Edit `mkdocs.yml` for your repo

Open `mkdocs.yml` and replace the placeholders with your actual GitHub username and repo name:

```yaml
site_url: https://YOUR-USERNAME.github.io/YOUR-REPO/
repo_name: YOUR-USERNAME/YOUR-REPO
repo_url: https://github.com/YOUR-USERNAME/YOUR-REPO
```

If your repo is at `https://github.com/alstdi/arc-clinical-browser`, that becomes:

```yaml
site_url: https://alstdi.github.io/arc-clinical-browser/
repo_name: alstdi/arc-clinical-browser
repo_url: https://github.com/alstdi/arc-clinical-browser
```

Same for the social links section near the bottom of `mkdocs.yml`.

Optional: if your repo is at the root of `username.github.io` (i.e. you registered a personal site), then `site_url` is just `https://YOUR-USERNAME.github.io/`.

---

## Step 6: Edit page content for ALS TDI specifics

Open the five Markdown files in `docs/` and replace the bracketed placeholders:

- `[ARC data team contact]` — replace with the real email or contact form URL
- Any other `[bracketed]` text

Search across all five files for `[` to catch them all.

---

## Step 7: Replace the placeholder logo and favicon

The `docs/assets/logo.svg` and `docs/assets/favicon.svg` I included are simple placeholders. To use ALS TDI's actual logo:

1. Get the official logo SVG (or PNG) from the ALS TDI brand team
2. Replace `docs/assets/logo.svg` with it
3. For favicon, a square version works best — a 32×32 PNG also works (rename and update `mkdocs.yml`)

If you stick with the placeholder for now, that's fine — it just shows a generic "A" in the header.

---

## Step 8: Preview locally

In your terminal:

```bash
cd path/to/your-repo
mkdocs serve
```

Open `http://localhost:8000` in your browser. You should see:

- The home page with the purple-to-navy hero gradient
- "ARC Clinical Browser" in serif type
- Tab navigation across the top: Home, Live Demo, About the Pipeline, For Other Registries, Privacy & Synthetic Data
- The brand colors throughout

Click **Live Demo** in the nav. The embedded dashboard should appear in an iframe. Click around inside it — patient list, tabs, export buttons should all work.

If the dashboard shows "Auto-load failed", check that `dashboard_demo.html` and `demo_dashboard_data.json` are both in `docs/` (not inside a subfolder).

Press **Ctrl+C** in the terminal to stop the preview when you're done.

---

## Step 9: Commit and push to `main`

```bash
git add .
git commit -m "Add MkDocs site with ALS TDI branding"
git push origin main
```

---

## Step 10: Configure GitHub Pages

Go to your repo on GitHub:

1. Click **Settings** → **Pages**
2. Under **Build and deployment**:
   - **Source:** "Deploy from a branch"
   - **Branch:** `gh-pages` / `(root)`
3. Click **Save**

GitHub will say "Your site is being built" and after a minute show "Your site is published at https://YOUR-USERNAME.github.io/YOUR-REPO/".

---

## Step 11: Verify auto-deployment

The first push to `main` should trigger the GitHub Action you copied into `.github/workflows/deploy.yml`. Check:

1. Click the **Actions** tab in your repo
2. You should see "Deploy MkDocs to GitHub Pages" running
3. Wait ~1-2 minutes for it to finish
4. Visit `https://YOUR-USERNAME.github.io/YOUR-REPO/`

If the Action shows as **success** but the site doesn't appear, give it another 1-2 minutes — GitHub's CDN takes a moment to propagate.

---

## Step 12: Make changes going forward

Anytime you want to update the site:

```bash
# Edit any file in docs/ or mkdocs.yml
git add .
git commit -m "Update home page copy"
git push origin main
```

The GitHub Action will rebuild and redeploy automatically. No manual `mkdocs gh-deploy` needed.

---

## Troubleshooting

### "404 - File not found" at the GitHub Pages URL

- Wait 2-3 minutes after first publish; GitHub Pages takes time to propagate.
- Verify the **Actions** tab shows a successful run.
- Verify `gh-pages` branch exists in your repo (it gets created automatically on first deploy).
- Check **Settings → Pages** is set to deploy from `gh-pages`, not `main`.

### The dashboard iframe shows nothing

- Check `dashboard_demo.html` and `demo_dashboard_data.json` are in `docs/`, not in a subfolder.
- Open browser dev tools (F12) → Console and look for fetch errors.
- Make sure `mkdocs.yml` doesn't have any plugins that strip `.html` files from the build.

### The colors don't look like ALS TDI brand colors

- Check `docs/stylesheets/alstdi-brand.css` is present.
- Verify `mkdocs.yml` has `extra_css: - stylesheets/alstdi-brand.css` near the middle of the file.
- Hard-refresh your browser (Ctrl+Shift+R on Windows, Cmd+Shift+R on Mac) — your browser may have cached the unstyled version.

### The Action fails with a "permission denied" error

- Go to **Settings** → **Actions** → **General** → scroll to **Workflow permissions**
- Set to "**Read and write permissions**" → Save
- Re-run the failed Action

### "Plugins removed" warnings during local `mkdocs serve`

- Ignore. These are advisories about a future MkDocs major version. They do not affect your build.

---

## A note on the two-branch model

When the GitHub Action runs `mkdocs gh-deploy`, it:

1. Builds the static HTML/CSS site from `main` into a temporary directory
2. Switches to the `gh-pages` branch
3. Replaces everything there with the new build
4. Force-pushes to `gh-pages`

This means anything you previously committed manually to `gh-pages` is gone. Always edit on `main`. The `gh-pages` branch is purely a deployment artifact, not a workspace.

If you ever need to clear `gh-pages` and start fresh, the simplest path is to delete the branch on GitHub and run a fresh deploy from local:

```bash
mkdocs gh-deploy --force --clean
```

---

## Maintenance

- Push to `main` → site updates automatically (~1-2 min)
- Update `dashboard_demo.html` or `demo_dashboard_data.json` in `docs/` to refresh the demo
- Re-run `python generate_synthetic_data.py` to produce a fresh demo dataset; copy the output into `docs/`
- The Material theme updates regularly; bump it occasionally with `pip install --upgrade mkdocs-material`

---

*Dedicated to curing ALS.*
