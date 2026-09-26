# 🚀 Deploying BusPass to Render.com (Free)

## What You Need
- A **GitHub account** (free)
- A **Render.com account** (free) — sign up at https://render.com

---

## Step 1 — Push Code to GitHub

```bash
# Inside your buspass_project folder:
git init
git add .
git commit -m "Initial commit"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/buspass.git
git branch -M main
git push -u origin main
```

---

## Step 2 — Deploy on Render (Blueprint method — easiest)

1. Go to https://dashboard.render.com
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub account and select your `buspass` repo
4. Render will automatically detect the `render.yaml` file
5. It will show you two resources to create:
   - ✅ `buspass-web` (Web Service)
   - ✅ `buspass-db` (PostgreSQL)
6. Click **"Apply"**
7. Wait ~3-5 minutes for first deploy

Render will automatically:
- Install all dependencies from `requirements.txt`
- Run `python manage.py collectstatic`
- Run `python manage.py migrate`
- Run `python manage.py seed_data` (creates admin + routes)
- Start the server with `gunicorn`

---

## Step 3 — Access Your Live App

After deploy, Render gives you a URL like:
```
https://buspass-web.onrender.com
```

**Login credentials:**
| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Student | Register at `/register/` | — |

---

## Step 4 — (Optional) Set a Custom Admin Password

For security, set a stronger admin password via Render environment variables:

1. Go to your `buspass-web` service on Render
2. Click **Environment** tab
3. Add: `ADMIN_PASSWORD` = `your_strong_password_here`
4. Click **Save** — Render will redeploy automatically

---

## Free Tier Limits (What to Expect)

| Resource | Render Free Tier |
|----------|-----------------|
| Web service | ✅ Free (sleeps after 15min inactivity) |
| PostgreSQL | ✅ Free for 90 days, then $7/mo |
| Custom domain | ✅ Free `.onrender.com` subdomain |
| SSL/HTTPS | ✅ Auto-provisioned, free |
| Bandwidth | 100 GB/month |

> ⚠️ **Cold starts:** The free web service "sleeps" after 15 minutes of no traffic.
> First request after sleep takes ~30 seconds to wake up. This is normal.

---

## Manual Deploy Option (Without render.yaml)

If you prefer to set things up manually on Render:

### Create PostgreSQL Database
1. Render Dashboard → New → PostgreSQL
2. Name: `buspass-db`, Plan: Free → Create

### Create Web Service
1. Render Dashboard → New → Web Service
2. Connect GitHub repo
3. Settings:
   - **Runtime:** Python
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn buspass_project.wsgi:application`
4. Environment Variables:
   - `SECRET_KEY` → click "Generate"
   - `DEBUG` → `False`
   - `DATABASE_URL` → copy from your PostgreSQL service's "Connection String"
5. Click **Create Web Service**

---

## Local Development (unchanged)

```bash
# Still works exactly as before — uses SQLite locally
python manage.py runserver
# → http://127.0.0.1:8000/
```

No `.env` file needed locally. When `DATABASE_URL` is not set,
the app automatically uses SQLite.
