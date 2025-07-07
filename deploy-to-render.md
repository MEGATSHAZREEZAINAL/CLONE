# 🚀 Deploy OpenManus to Render

## Step 1: Persiapan

1. **Buat account Render**: [render.com](https://render.com)
2. **Connect GitHub account**
3. **Push OpenManus ke GitHub repo anda**

## Step 2: Deploy ke Render

### Via Render Dashboard:

1. **Login ke Render** → [render.com](https://render.com)
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure deployment:**

```yaml
Name: openmanus-ai-agent
Environment: Python 3
Build Command: pip install -r requirements.txt && playwright install chromium
Start Command: python web_server.py
```

## Step 3: Environment Variables

Add dalam Render dashboard:

```bash
GEMINI_API_KEY=AIzaSyAw2gROMlUaIVj11Uy-lsDfxN39rNVeq_0
PYTHONUNBUFFERED=1
DISPLAY=:99
PORT=10000
```

## Step 4: Advanced Settings

```yaml
Auto-Deploy: Yes
Branch: main
Runtime: Python 3.12
Health Check Path: /health
```

## Step 5: Deploy!

- ✅ Click **"Create Web Service"**
- ✅ Render akan build dan deploy automatically
- ✅ Check logs untuk progress

## Step 6: Access Your App

Selepas deploy:
- ✅ **URL**: `https://your-app.onrender.com`
- ✅ **Web interface** ready
- ✅ **Test dengan task** simple

## 💡 Render Benefits:

- ✅ **Free tier** available
- ✅ **SSL certificates** automatic
- ✅ **GitHub integration** seamless
- ✅ **Build logs** detailed
- ✅ **Auto-deploy** on git push

## ⚠️ Render Limitations (Free):

- 📝 **Spin down** after 15 minutes inactive
- 📝 **Cold starts** may take 30-60 seconds
- 📝 **Build time** limits
- 📝 **Monthly hours** limited

## 🔧 Alternative: render.yaml

Create `render.yaml` untuk deployment automation:

```yaml
services:
  - type: web
    name: openmanus-ai-agent
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt && playwright install chromium
    startCommand: python web_server.py
    envVars:
      - key: PYTHONUNBUFFERED
        value: 1
      - key: DISPLAY
        value: :99
      - key: GEMINI_API_KEY
        sync: false  # Set manually in dashboard
```

## 🚀 Quick Deploy Commands:

```bash
# Update API key dalam config
echo "api_key = 'AIzaSyAw2gROMlUaIVj11Uy-lsDfxN39rNVeq_0'" >> config/config.toml

# Commit dan push
git add .
git commit -m "Deploy to Render"
git push origin main

# Deploy akan trigger automatically
```