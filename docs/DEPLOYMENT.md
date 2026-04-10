# Echo Backend Deployment Guide

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│  Mobile App │────▶│  Render Backend │◀────│  Web Front  │
│  (Flutter)  │     │  (FastAPI)      │     │  (Next.js)  │
└─────────────┘     └────────┬────────┘     └─────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Render   │  │ Pinecone │  │  OpenAI  │
        │ PostgreSQL│  │  Vector  │  │    LLM   │
        └──────────┘  └──────────┘  └──────────┘
```

## Prerequisites

1. **GitHub Account** - Code is hosted on GitHub
2. **Render Account** - https://render.com (free tier available)
3. **Pinecone Account** - https://pinecone.io (free tier available)
4. **OpenAI API Key** - https://platform.openai.com

---

## Step 1: Create Pinecone Index

1. Go to https://pinecone.io and create a free account
2. Create a new Index:
   - **Name**: `echo-records`
   - **Dimension**: `1536`
   - **Metric**: `cosine`
   - **Cloud**: `AWS`
   - **Region**: `us-east-1`
3. Copy your **API Key** from the Pinecone dashboard

---

## Step 2: Create Render PostgreSQL

1. Go to https://render.com and create a free account
2. Create a new **PostgreSQL** instance:
   - **Name**: `echo-db`
   - **Plan**: Free
   - **Region**: Oregon (or closest to you)
3. Wait for the database to be provisioned (~2 minutes)
4. Copy the **Connection URL** (Internal Database URL)

---

## Step 3: Deploy Backend to Render

### Option A: Connect GitHub (Recommended)

1. Go to https://dashboard.render.com/blueprints
2. Click **"New Blueprint Instance"**
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml`
5. Add the following Environment Variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (Paste your PostgreSQL connection URL) |
| `PINECONE_API_KEY` | (Paste your Pinecone API key) |
| `PINECONE_ENVIRONMENT` | `us-east-1` |
| `OPENAI_API_KEY` | (Your OpenAI API key) |
| `LLM_PROVIDER` | `openai` |

6. Click **"Create Blueprint"**

### Option B: Manual Deploy

1. Create a new **Web Service** on Render
2. Connect your GitHub repo
3. Configure:
   - **Root Directory**: (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.main:app --bind 0.0.0.0:$PORT --workers 1`
4. Add Environment Variables (same as above)
5. Click **"Create Web Service"**

---

## Step 4: Get Backend URL

After deployment, Render will give you a URL like:
```
https://echo-api.onrender.com
```

Save this URL - you'll need it for:
- Mobile app configuration
- Web frontend `NEXT_PUBLIC_API_URL`

---

## Step 5: Test the Deployment

```bash
curl https://your-backend-url.onrender.com/health
# Should return: {"status": "healthy"}
```

---

## Step 6: Configure Frontends

### Mobile App (Flutter)

Edit `mobile/lib/core/constants.dart`:
```dart
static const String apiBaseUrl = 'https://your-backend-url.onrender.com';
```

### Web Frontend (Next.js)

```bash
cd frontend
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com npm run build
```

Or set environment variable before running:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com npm run dev
```

---

## Cost Summary

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Render Web Service | 750 hours/month | $7/month |
| Render PostgreSQL | 1 instance, 90 day limit | $7/month |
| Pinecone | 1M vectors | $70/month |
| OpenAI | Pay per use | $0.002/1K tokens |

**Total (Free tier)**: ~$0/month (with limitations)
**Total (Production)**: ~$15-25/month

---

## Troubleshooting

### Backend not starting
- Check Render logs for errors
- Verify all environment variables are set
- Ensure `requirements.txt` has all dependencies

### Database connection failed
- Verify `DATABASE_URL` is correct
- Check Render PostgreSQL is not sleeping (free tier sleeps after 90 days)

### Vector search not working
- Verify Pinecone index exists and API key is correct
- Check Pinecone index dimension is 1536

### LLM not generating insights
- Verify `OPENAI_API_KEY` is set correctly
- Check your OpenAI account has available credits

---

## Updating the Deployment

1. Push changes to GitHub
2. Render will auto-deploy on the next push
3. Or manually trigger a deploy from the Render dashboard
