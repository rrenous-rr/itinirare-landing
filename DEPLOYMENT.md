# Itinirare Landing Page — Deployment Guide

## Overview

The landing page is a static HTML/CSS site with one serverless function for the contact form.
It is hosted on **Vercel**, deployed automatically from **GitHub** on every push to `master`.

---

## Repositories & Services

| What | Where |
|------|-------|
| GitHub repo | https://github.com/rrenous-rr/itinirare-landing |
| Vercel project | https://vercel.com/rrenous-rr/itinirare-landing |
| Live site | https://itinirare-landing.vercel.app (or your custom domain) |
| GitHub account | `rrenous-rr` |

---

## How the Pipeline Works

```
You edit files locally
       ↓
git push origin master
       ↓
GitHub receives the push
       ↓
Vercel detects the push (via GitHub integration)
       ↓
Vercel builds & deploys automatically (~30 seconds)
       ↓
Live site is updated
```

No manual build step. No CI/CD config needed. Push = deploy.

---

## Local Development

### Prerequisites
- Git
- GitHub CLI (`gh`) — installed via `winget install --id GitHub.cli`
- A browser (open HTML files directly — no build step needed)

### First-time setup on a new machine
```bash
gh auth login
git clone https://github.com/rrenous-rr/itinirare-landing.git
cd itinirare-landing
```

### Preview locally
Just open `index.html` in a browser. All paths are **relative** so images and links work from `file://`.

> ⚠️ The contact form (`/api/contact`) will NOT work locally — it needs Vercel's serverless runtime.
> To test the form locally you'd need the Vercel CLI (`npx vercel dev`).

### Making changes
```bash
# Edit files, then:
git add <files>
git commit -m "describe your change"
git push origin master
# Vercel auto-deploys in ~30 seconds
```

---

## Project Structure

```
itinirare-landing/
├── index.html          # Main landing page
├── contact.html        # Contact page (form → /api/contact)
├── support.html        # FAQ / Support page
├── privacy.html        # Privacy policy
├── terms.html          # Terms of service
├── favicon.png         # App icon (32×32, used in browser tab + header)
├── icon.png            # Larger app icon
├── vercel.json         # Vercel config (cleanUrls, no trailing slashes)
├── package.json        # Node deps for serverless function (nodemailer)
├── .gitignore
├── images/             # App screenshots used in the landing page
│   ├── screenshot-firsttrip.png
│   ├── screenshot-multitrip.png
│   ├── screenshot-triplist.png
│   ├── screenshot-sharing.png
│   ├── screenshot-multiusers.png
│   ├── screenshot-triptips.png
│   └── screenshot-suggestions.png
└── api/
    └── contact.js      # Vercel serverless function — sends contact form emails
```

---

## Vercel Configuration

### vercel.json
```json
{
  "cleanUrls": true,
  "trailingSlash": false
}
```

- **cleanUrls**: lets you link to `/privacy` instead of `/privacy.html`
- **trailingSlash: false**: `itinirare.com/privacy` not `itinirare.com/privacy/`

### Build settings (in Vercel dashboard)
These should already be set, but for reference:

| Setting | Value |
|---------|-------|
| Framework preset | Other |
| Build command | *(leave empty)* |
| Output directory | *(leave empty / `.`)* |
| Install command | `npm install` (Vercel detects package.json automatically) |

Vercel installs `nodemailer` from `package.json` so the serverless function can use it.

---

## Environment Variables

The contact form serverless function reads all SMTP credentials from environment variables.
**Never put the password in code.**

### Where to set them
1. Go to https://vercel.com → `itinirare-landing` project
2. **Settings** → **Environment Variables**
3. Add each variable below, selecting **Production + Preview + Development**

### Required variables

| Variable | Value | Notes |
|----------|-------|-------|
| `SMTP_HOST` | `mail.spacemail.com` | SMTP server hostname |
| `SMTP_PORT` | `465` | Implicit TLS port |
| `SMTP_USER` | `raphir@itinirare.com` | SMTP login / sender address |
| `SMTP_PASS` | *(your password)* | ⚠️ Keep secret — never commit to git |
| `SMTP_TO` | `info@itinirare.com` | Where contact form emails are delivered |

### After changing env vars
Environment variable changes require a **redeploy** to take effect:
- Go to **Deployments** tab → click the three dots on the latest deployment → **Redeploy**

---

## Contact Form — How It Works

```
User fills form on contact.html
       ↓
JavaScript fetch() POSTs JSON to /api/contact
       ↓
Vercel routes /api/contact → api/contact.js (Node.js serverless function)
       ↓
Function reads SMTP_* env vars, connects to mail.spacemail.com:465 (TLS)
       ↓
Sends formatted HTML email to info@itinirare.com
Reply-To is set to the visitor's email address
       ↓
Returns { ok: true } → form shows success screen
```

### Error handling
- Network error or 5xx → red error banner appears on the form, user can retry
- All fields validated client-side (required) before sending

---

## Custom Domain (optional — when ready)

1. In Vercel dashboard → **Settings** → **Domains**
2. Add your domain (e.g. `itinirare.com` or `www.itinirare.com`)
3. Vercel gives you DNS records to add in your domain registrar
4. Vercel provisions an SSL certificate automatically

---

## Connecting a New Machine to This Repo

```bash
# 1. Install GitHub CLI if not already installed
winget install --id GitHub.cli

# 2. Authenticate
gh auth login
# → choose GitHub.com → HTTPS → authenticate via browser

# 3. Clone the repo
git clone https://github.com/rrenous-rr/itinirare-landing.git
cd itinirare-landing

# 4. Make changes, commit, push
git add .
git commit -m "your change"
git push origin master
```

---

## Useful Links

- Vercel dashboard: https://vercel.com/dashboard
- GitHub repo: https://github.com/rrenous-rr/itinirare-landing
- Vercel docs (serverless functions): https://vercel.com/docs/functions
- nodemailer docs: https://nodemailer.com

---

*Last updated: February 2026*
