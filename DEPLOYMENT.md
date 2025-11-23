# Deployment Guide - Render

This guide will help you deploy the Hedge Fund Agent application to Render.

## Prerequisites

1. A [Render account](https://render.com) (free tier available)
2. Your GitHub repository pushed to GitHub (Render deploys from Git)
3. API keys:
   - **GEMINI_API_KEY** (required) - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **NEWS_API_KEY** (optional) - Get from [NewsAPI.org](https://newsapi.org/)

## Option 1: Deploy via Blueprint (Recommended)

This deploys both backend and frontend together using the `render.yaml` file.

### Steps:

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Go to Render Dashboard**:
   - Visit https://dashboard.render.com/
   - Click "New +" → "Blueprint"

3. **Connect your repository**:
   - Connect your GitHub account if needed
   - Select the `hedge-fund-agent` repository
   - Render will automatically detect the `render.yaml` file

4. **Configure environment variables**:
   
   For **hedge-fund-agent-backend**:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `NEWS_API_KEY`: Your NewsAPI key (optional)
   
   For **hedge-fund-agent-frontend**:
   - `NEXT_PUBLIC_API_URL`: Set this to your backend URL (will be something like `https://hedge-fund-agent-backend.onrender.com`)

5. **Deploy**:
   - Click "Apply"
   - Render will build and deploy both services
   - Wait 5-10 minutes for initial deployment

6. **Update frontend with backend URL**:
   - Once backend is deployed, copy its URL
   - Go to frontend service → Environment
   - Set `NEXT_PUBLIC_API_URL` to the backend URL
   - Trigger a manual deploy

## Option 2: Deploy Services Individually

If you prefer to deploy each service separately:

### Deploy Backend:

1. Go to Render Dashboard → "New +" → "Web Service"
2. Connect your repository
3. Configure:
   - **Name**: `hedge-fund-agent-backend`
   - **Region**: Oregon (or your preference)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   - `GEMINI_API_KEY`: Your API key
   - `NEWS_API_KEY`: Your API key (optional)
   - `PYTHON_VERSION`: `3.11.0`
5. Click "Create Web Service"

### Deploy Frontend:

1. Go to Render Dashboard → "New +" → "Web Service"
2. Connect your repository (same repo)
3. Configure:
   - **Name**: `hedge-fund-agent-frontend`
   - **Region**: Oregon (or same as backend)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Node`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Start Command**: `cd frontend && npm start`
4. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend URL (e.g., `https://hedge-fund-agent-backend.onrender.com`)
   - `NODE_VERSION`: `18.17.0`
5. Click "Create Web Service"

## Post-Deployment

### Verify Backend:

Visit: `https://your-backend-url.onrender.com/health`

You should see:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "scenarios_count": 0,
  "tracked_scenarios_count": 0
}
```

### Verify Frontend:

Visit: `https://your-frontend-url.onrender.com`

You should see the Hedge Fund Agent interface.

## Important Notes

### Free Tier Limitations:

- **Spin down**: Free tier services spin down after 15 minutes of inactivity
- **Cold starts**: First request after spin down takes 30-60 seconds
- To keep services always on, upgrade to paid tier ($7/month per service)

### CORS Configuration:

The backend currently allows all origins (`allow_origins=["*"]`). For production, update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables Security:

- Never commit `.env` files to Git
- Manage all secrets through Render's dashboard
- The `sync: false` setting in `render.yaml` means you must set these manually

## Troubleshooting

### Build Failures:

**Backend fails with "No module named 'X'"**:
- Check that all dependencies are in `backend/requirements.txt`
- Verify Python version is set correctly

**Frontend fails during build**:
- Check that `NODE_VERSION` is set to `18.17.0` or higher
- Verify all dependencies are in `frontend/package.json`

### Runtime Issues:

**Backend returns 500 errors**:
- Check logs in Render dashboard
- Verify `GEMINI_API_KEY` is set correctly
- Check the "Logs" tab for detailed error messages

**Frontend can't connect to backend**:
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Must include `https://` protocol
- Check backend is running and healthy

**CORS errors**:
- Update backend CORS settings to include frontend URL
- Redeploy backend after changes

## Updating Your Deployment

Render automatically deploys when you push to your connected Git branch:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Or trigger manual deploys from the Render dashboard.

## Monitoring

- **Logs**: Available in Render dashboard under each service
- **Metrics**: View request counts, response times in Render dashboard
- **Health Checks**: Backend has `/health` endpoint for monitoring

## Cost Estimate

**Free Tier** (both services):
- Cost: $0/month
- Limitations: Spin down after inactivity, 750 hours/month

**Starter Tier** (both services):
- Cost: ~$14/month ($7 × 2 services)
- Benefits: Always on, no spin down, 512MB RAM per service

## Next Steps

1. Deploy using Option 1 above
2. Test the application thoroughly
3. Consider upgrading to paid tier if needed
4. Set up custom domain (optional)
5. Configure monitoring/alerting (optional)

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com/
