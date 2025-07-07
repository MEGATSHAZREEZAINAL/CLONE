# OpenManus Deployment Guide

This guide provides multiple deployment options for OpenManus, an AI agent framework.

## Prerequisites

- Python 3.12+
- Docker (for containerized deployment)
- Git
- API keys for LLM services (OpenAI, Claude, etc.)

## Deployment Options

### 1. Local Development Deployment

#### Quick Setup

```bash
# Clone the repository
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Setup configuration
cp config/config.example.toml config/config.toml
# Edit config/config.toml to add your API keys

# Run the application
python main.py
```

#### Using UV (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Setup configuration
cp config/config.example.toml config/config.toml
# Edit config/config.toml to add your API keys

# Run the application
python main.py
```

### 2. Docker Deployment (Recommended for Production)

#### Quick Docker Deployment

```bash
# Run the deployment script
./deploy.sh

# Or manually:
docker-compose build
docker-compose run --rm openmanus
```

#### Docker Commands

```bash
# Build the image
docker-compose build

# Run interactively (recommended)
docker-compose run --rm openmanus

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Clean up
docker-compose down --volumes --rmi all
```

### 3. Cloud Deployment

#### AWS EC2 Deployment

```bash
# Connect to your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-instance

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and deploy
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
./deploy.sh

# Configure API keys
nano config/config.toml
```

#### Google Cloud Platform

```bash
# Create a new Compute Engine instance
gcloud compute instances create openmanus-instance \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=e2-medium \
    --zone=us-central1-a

# SSH into the instance
gcloud compute ssh openmanus-instance --zone=us-central1-a

# Follow the same Docker installation steps as AWS EC2
```

#### Azure Virtual Machine

```bash
# Create a new VM
az vm create \
    --resource-group myResourceGroup \
    --name openmanusVM \
    --image Ubuntu2204 \
    --admin-username azureuser \
    --generate-ssh-keys

# SSH into the VM
ssh azureuser@<public-ip-address>

# Follow the same Docker installation steps as AWS EC2
```

## Configuration

### Required Configuration

1. **API Keys**: Edit `config/config.toml` to add your LLM API keys:

```toml
[llm]
model = "claude-3-5-sonnet"  # or "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "your-api-key-here"
max_tokens = 4096
temperature = 0.0

[llm.vision]
model = "claude-3-5-sonnet"
base_url = "https://api.openai.com/v1"
api_key = "your-api-key-here"
```

2. **Browser Configuration** (optional):

```toml
[browser]
headless = true  # Set to false for debugging
disable_security = true
```

3. **Proxy Configuration** (optional):

```toml
[browser.proxy]
server = "http://proxy-server:port"
username = "proxy-username"
password = "proxy-password"
```

## Environment Variables

You can also use environment variables instead of config files:

```bash
export OPENAI_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## Troubleshooting

### Common Issues

1. **Browser automation fails**:
   - Ensure Playwright browsers are installed: `playwright install chromium`
   - For Docker: Make sure the container has proper display setup

2. **API key errors**:
   - Verify your API keys in `config/config.toml`
   - Check that you have sufficient API credits

3. **Permission errors**:
   - Ensure proper file permissions: `chmod +x deploy.sh`
   - For Docker: Make sure Docker daemon is running

4. **Memory issues**:
   - Increase Docker container memory: modify `shm_size` in docker-compose.yml
   - For local deployment: ensure sufficient RAM (4GB+ recommended)

### Logs

- Local deployment: Check terminal output
- Docker deployment: `docker-compose logs -f`
- Application logs: Check `logs/` directory if created

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Browser Security**: The application disables some browser security features for automation
3. **Network**: Consider running behind a firewall or VPN
4. **Updates**: Regularly update dependencies for security patches

## Performance Optimization

1. **Resource Allocation**:
   - Minimum 4GB RAM recommended
   - SSD storage for better performance
   - Stable internet connection for API calls

2. **Docker Optimization**:
   - Use multi-stage builds for smaller images
   - Configure resource limits in docker-compose.yml

3. **Scaling**:
   - For multiple concurrent users, consider container orchestration
   - Use load balancers for high availability

## Monitoring and Maintenance

1. **Health Checks**: Monitor application logs for errors
2. **Resource Monitoring**: Check CPU, memory, and disk usage
3. **API Usage**: Monitor API call quotas and costs
4. **Updates**: Regularly pull latest changes from the repository

## Support

For deployment issues:
1. Check the troubleshooting section above
2. Review application logs
3. Check the [GitHub Issues](https://github.com/mannaandpoem/OpenManus/issues)
4. Contact the maintainers via email: mannaandpoem@gmail.com