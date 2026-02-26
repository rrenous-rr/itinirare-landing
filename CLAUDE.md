# CLAUDE.md — Itinirare Landing Page

## Project Overview

Static HTML/CSS landing page for the **Itinirare** travel planning app. Hosted on Vercel with one Node.js serverless function for the contact form. Auto-deploys from GitHub (`master` branch).

---

## Key Links

| What | Where |
|------|-------|
| GitHub repo | https://github.com/rrenous-rr/itinirare-landing |
| Vercel project | https://vercel.com/rrenous-rr/itinirare-landing |
| Live site | https://itinirare-landing.vercel.app |

---

## Project Structure

```
itinirare-landing/
├── index.html          # Main landing page
├── contact.html        # Contact form → POSTs to /api/contact
├── support.html        # FAQ / Support page
├── privacy.html        # Privacy policy
├── terms.html          # Terms of service
├── favicon.png / icon.png
├── vercel.json         # cleanUrls: true, trailingSlash: false
├── package.json        # nodemailer dep for serverless function
├── DEPLOYMENT.md       # Full deployment reference
├── images/             # App screenshots (7 PNG files)
└── api/
    └── contact.js      # Serverless function — sends email via SMTP
```

---

## Tech Stack

- **No build step** — plain HTML/CSS/JS, open `index.html` directly in browser
- **Vercel** — static hosting + serverless functions (Node.js)
- **GitHub** — push to `master` triggers auto-deploy (~30s)
- **nodemailer** — used in `api/contact.js` to send contact form emails via SMTP

---

## What Was Built (Session History)

### Initial build
- Created landing page (`index.html`) with app screenshots, feature sections, store links
- Light theme design with split layouts showcasing real app screenshots

### Pages added
- `contact.html` — contact form with JS validation and success/error UI
- `support.html` — FAQ page
- `privacy.html` and `terms.html` — legal pages

### Infrastructure
- `api/contact.js` — Vercel serverless function that reads SMTP credentials from env vars and sends emails via nodemailer
- `vercel.json` — clean URL config (no `.html` extensions in URLs)
- `package.json` — declares nodemailer dependency
- `DEPLOYMENT.md` — full reference guide for deployment, env vars, and onboarding new machines

### Fixes & polish
- Fixed all internal links to use relative paths (works both locally and on Vercel)
- Updated email addresses to `raphir@itinirare.com` / `info@itinirare.com`
- Added Google Play store link
- Fixed footer Contact link to point to `contact.html`

---

## Current State (February 2026)

- **All pages complete and deployed** on Vercel
- **Contact form** is wired up end-to-end; requires SMTP env vars set in Vercel dashboard to send mail
- **No custom domain** yet — live at the `.vercel.app` subdomain
- **Git repo is clean** — no uncommitted changes

### SMTP env vars required in Vercel (Settings → Environment Variables)

| Variable | Value |
|----------|-------|
| `SMTP_HOST` | `mail.spacemail.com` |
| `SMTP_PORT` | `465` |
| `SMTP_USER` | `raphir@itinirare.com` |
| `SMTP_PASS` | *(secret — never commit)* |
| `SMTP_TO` | `info@itinirare.com` |

---

## Workflow

```bash
# Make changes, then:
git add <files>
git commit -m "describe change"
git push origin master
# Vercel auto-deploys in ~30 seconds
```

For full details, see `DEPLOYMENT.md`.
