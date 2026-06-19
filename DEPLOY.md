# Deployment Guide — ShinyApps.io

This guide walks you through deploying the HPV Cancer Prediction Tool online using **ShinyApps.io** (free tier available).

---

## Prerequisites

- Python 3.9+ installed on your machine
- A GitHub account (for hosting the code)
- A ShinyApps.io account — sign up free at https://www.shinyapps.io

---

## Step 1 — Push to GitHub

> Do this once to host your code publicly (or privately).

```bash
# Inside your project folder
git init
git add .
git commit -m "Initial commit: HPV prediction app"

# On GitHub: create a new repo called hpv-cancer-prediction
# Then connect and push:
git remote add origin https://github.com/<your-username>/hpv-cancer-prediction.git
git branch -M main
git push -u origin main
```

---

## Step 2 — Install rsconnect-python

This is Posit's official tool for deploying Python Shiny apps to ShinyApps.io.

```bash
pip install rsconnect-python
```

---

## Step 3 — Connect your ShinyApps.io account

1. Go to https://www.shinyapps.io → Log in → Click your name (top right) → **Tokens**
2. Click **Show** → copy the token and secret
3. Run this command (replace with your actual values):

```bash
rsconnect add \
  --account <your-shinyapps-username> \
  --name shinyapps \
  --token <YOUR_TOKEN> \
  --secret <YOUR_SECRET>
```

---

## Step 4 — Deploy the App

From inside the project folder, run:

```bash
rsconnect deploy shiny . \
  --account <your-shinyapps-username> \
  --name hpv-cancer-prediction \
  --title "HPV Cancer Prediction Tool"
```

- This uploads all files and starts the app on ShinyApps.io.
- Deployment takes 2–5 minutes (first time).
- Once done, your app will be live at:
  `https://<your-shinyapps-username>.shinyapps.io/hpv-cancer-prediction/`

---

## Step 5 — Verify the App

Open the URL in your browser and test:
1. Download the sample CSV from the sidebar
2. Upload it in **Batch Prediction** mode
3. Click **Run Prediction** — results should appear

---

## Updating the App

After making changes to `app.py` or any files:

```bash
# Push changes to GitHub
git add .
git commit -m "Update: describe your change"
git push

# Re-deploy to ShinyApps.io
rsconnect deploy shiny . \
  --account <your-shinyapps-username> \
  --name hpv-cancer-prediction \
  --title "HPV Cancer Prediction Tool"
```

---

## ShinyApps.io Free Tier Limits

| Resource | Free Plan |
|----------|-----------|
| Active hours / month | 25 hrs |
| Apps | 5 |
| RAM | 1 GB |
| Instances | 1 |

For research use, the free tier is typically sufficient. Upgrade to a paid plan if you need more uptime.

---

## Troubleshooting

**App fails to start — module not found:**
Make sure all packages in `requirements.txt` are installed and listed correctly.

**Pickle file errors:**
Ensure `hpv_paper.pkl` and `training_genes.pkl` are included in the deployment folder (they must not be in `.gitignore`).

**Gene mismatch errors:**
Check that uploaded CSV column names match the 20 expected gene names (case-insensitive).
