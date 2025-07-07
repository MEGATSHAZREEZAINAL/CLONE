#!/bin/bash

# OpenManus System Service Installation Script
set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (use sudo)"
    exit 1
fi

echo "🚀 Installing OpenManus as a system service..."

# Create user for the service
if ! id "openmanus" &>/dev/null; then
    echo "👤 Creating openmanus user..."
    useradd --system --create-home --home-dir /opt/openmanus --shell /bin/bash openmanus
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y python3.12 python3.12-venv python3-pip git xvfb

# Clone or update repository
if [ ! -d "/opt/openmanus/OpenManus" ]; then
    echo "📥 Cloning OpenManus repository..."
    sudo -u openmanus git clone https://github.com/mannaandpoem/OpenManus.git /opt/openmanus/OpenManus
else
    echo "🔄 Updating OpenManus repository..."
    cd /opt/openmanus/OpenManus
    sudo -u openmanus git pull
fi

# Setup Python environment
cd /opt/openmanus/OpenManus
echo "🐍 Setting up Python virtual environment..."
sudo -u openmanus python3.12 -m venv /opt/openmanus/.venv
sudo -u openmanus /opt/openmanus/.venv/bin/pip install --upgrade pip
sudo -u openmanus /opt/openmanus/.venv/bin/pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
sudo -u openmanus /opt/openmanus/.venv/bin/playwright install chromium

# Setup configuration
if [ ! -f "/opt/openmanus/OpenManus/config/config.toml" ]; then
    echo "⚙️ Setting up configuration..."
    sudo -u openmanus cp /opt/openmanus/OpenManus/config/config.example.toml /opt/openmanus/OpenManus/config/config.toml
    echo "⚠️  Please edit /opt/openmanus/OpenManus/config/config.toml and add your API keys"
fi

# Copy and link files to the correct location
sudo -u openmanus cp -r /opt/openmanus/OpenManus/* /opt/openmanus/
sudo -u openmanus chmod +x /opt/openmanus/deploy.sh

# Install systemd service
echo "🔧 Installing systemd service..."
cp /opt/openmanus/systemd/openmanus.service /etc/systemd/system/
systemctl daemon-reload

# Enable and start service
echo "🚀 Enabling OpenManus service..."
systemctl enable openmanus

echo "✅ Installation complete!"
echo ""
echo "To start the service:"
echo "  sudo systemctl start openmanus"
echo ""
echo "To check service status:"
echo "  sudo systemctl status openmanus"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u openmanus -f"
echo ""
echo "To configure API keys:"
echo "  sudo nano /opt/openmanus/config/config.toml"
echo ""
echo "⚠️  Don't forget to configure your API keys before starting the service!"