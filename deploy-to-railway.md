# 🚀 Deploy OpenManus to Railway

## Step 1: Persiapan

1. **Buat account Railway**: [railway.app](https://railway.app)
2. **Connect GitHub account** 
3. **Push OpenManus ke GitHub repo anda**

## Step 2: Deploy ke Railway

### Via Website (Senang):

1. **Login ke Railway** → [railway.app](https://railway.app)
2. **Click "New Project"**
3. **Choose "Deploy from GitHub repo"**
4. **Select your OpenManus repository**
5. **Railway akan auto-detect Python project**

### Environment Variables:
Set environment variables dalam Railway dashboard:

```bash
GEMINI_API_KEY=AIzaSyAw2gROMlUaIVj11Uy-lsDfxN39rNVeq_0
PYTHONUNBUFFERED=1
DISPLAY=:99
```

## Step 3: Konfigurasi

### Railway akan automatically:
- ✅ Install dependencies dari `requirements.txt`
- ✅ Install Playwright browsers
- ✅ Run `web_server.py`
- ✅ Expose web interface

## Step 4: Access Your App

Setelah deploy selesai:
- ✅ **Railway akan beri link** (example: `your-app.railway.app`)
- ✅ **Web interface available** di browser
- ✅ **Submit tasks** via web form

## Step 5: Usage

1. **Open** your Railway URL
2. **Enter task** dalam form:
   ```
   Search Google for latest tech news and summarize top 3 articles
   ```
3. **Click Execute** dan tunggu result!

## 💡 Tips:

- **Free tier**: $5/month credit (enough untuk testing)
- **Auto-scaling**: Railway scale automatically
- **Logs**: Check Railway dashboard untuk logs
- **Custom domain**: Available in Railway settings

## 🔧 Troubleshooting:

**If deployment fails:**
1. Check Railway logs
2. Verify environment variables
3. Ensure GitHub repo is public
4. Check `requirements.txt` format

**Railway CLI (Optional):**
```bash
npm install -g @railway/cli
railway login
railway link
railway up
```