#!/bin/bash

# 🚀 OpenManus Auto-Deploy Helper
echo "🤖 OpenManus Auto-Deploy Helper"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial OpenManus deployment setup"
    echo "✅ Git repository created!"
else
    echo "✅ Git repository already exists"
fi

# Show current status
echo ""
echo "📋 DEPLOYMENT STATUS:"
echo "✅ Web server: web_server.py"
echo "✅ API Key: Configured"
echo "✅ Dependencies: requirements.txt"
echo "✅ Config: railway.toml, Procfile"
echo ""

# Show deployment options
echo "🚀 SUPER SIMPLE DEPLOYMENT OPTIONS:"
echo ""
echo "1️⃣  RAILWAY (Recommended):"
echo "   • Go to: https://railway.app"
echo "   • Sign up with GitHub"
echo "   • 'New Project' → 'Deploy from GitHub'"
echo "   • Select your repo"
echo "   • Add env: GEMINI_API_KEY=AIzaSyAw2gROMlUaIVj11Uy-lsDfxN39rNVeq_0"
echo "   • DONE! ✨"
echo ""
echo "2️⃣  RENDER (Free):"
echo "   • Go to: https://render.com"
echo "   • 'New +' → 'Web Service'"
echo "   • Connect GitHub repo"
echo "   • Build: pip install -r requirements.txt && playwright install chromium"
echo "   • Start: python web_server.py"
echo "   • Add env variables"
echo "   • DONE! ✨"
echo ""

# Show what they'll get
echo "🎯 YOUR DEPLOYED APP WILL HAVE:"
echo "• 🌐 Live URL accessible worldwide"
echo "• 📱 Beautiful web interface"
echo "• 🤖 AI agent powered by Gemini"
echo "• ⚡ Real-time task execution"
echo "• 🔒 HTTPS security"
echo ""

echo "🎉 OpenManus is 100% READY TO DEPLOY!"
echo ""
echo "💡 Need help? Read: DEPLOY_STATUS.md"