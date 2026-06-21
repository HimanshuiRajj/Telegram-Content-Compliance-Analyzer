# Installation Guide

Complete step-by-step guide to install and configure the Telegram Content Compliance Analyzer.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [System Setup](#system-setup)
3. [Telegram Configuration](#telegram-configuration)
4. [OpenAI Configuration](#openai-configuration)
5. [Application Setup](#application-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Minimum Requirements
- **Python 3.9** or higher
- **pip** (Python package manager)
- **Git** (optional, for cloning)
- **2GB RAM minimum**
- **500MB disk space**

### Accounts Needed
- **Telegram Account** - Personal or organization account
- **OpenAI Account** - For API access

### Check Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should show Python 3.9 or higher
```

If not installed:
- **Windows**: https://www.python.org/downloads/
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3`

## System Setup

### Windows

#### 1. Download Project
```bash
# Option A: Using Git
git clone <repository-url>
cd telegram-compliance-analyzer

# Option B: Download and extract ZIP file
# Extract to desired location
cd telegram-compliance-analyzer
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal
```

#### 3. Upgrade pip
```bash
python -m pip install --upgrade pip
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### macOS

#### 1. Download Project
```bash
# Using Git
git clone <repository-url>
cd telegram-compliance-analyzer

# Or download and extract ZIP
cd telegram-compliance-analyzer
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal
```

#### 3. Upgrade pip
```bash
pip install --upgrade pip
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)

#### 1. Install Dependencies
```bash
# Update package list
sudo apt-get update

# Install Python and development tools
sudo apt-get install python3 python3-pip python3-venv build-essential

# Install system libraries for cryptography
sudo apt-get install libssl-dev libffi-dev
```

#### 2. Download Project
```bash
# Using Git
git clone <repository-url>
cd telegram-compliance-analyzer

# Or download and extract
unzip telegram-compliance-analyzer.zip
cd telegram-compliance-analyzer
```

#### 3. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Telegram Configuration

### Step 1: Get API Credentials

1. Visit https://my.telegram.org
2. Log in with your Telegram account
3. Click "API development tools"
4. Create a new application:
   - **App title**: Enter any name (e.g., "Compliance Analyzer")
   - **Short name**: Enter a short identifier
   - Accept terms
   - Click "Create my app!"

5. You'll see:
   - **App api_id**
   - **App api_hash**
   
Save these values - you'll need them next.

### Step 2: Configure .env File

```bash
# Copy the example file
cp .env.example .env

# Edit .env file with your favorite editor
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

Add your Telegram credentials:
```bash
TELEGRAM_API_ID=123456789
TELEGRAM_API_HASH=abcdef0123456789abcdef0123456789
```

**Important**: Keep these credentials secret!

## OpenAI Configuration

### Step 1: Create OpenAI Account

1. Visit https://platform.openai.com/signup
2. Create account or sign in
3. Verify email

### Step 2: Get API Key

1. Go to https://platform.openai.com/api/keys
2. Click "Create new secret key"
3. Copy the key (you won't be able to see it again!)
4. Save in .env file

### Step 3: Set Up Billing

1. Go to https://platform.openai.com/account/billing/overview
2. Add payment method
3. Set usage limits (recommended: $10-20/month for testing)

### Step 4: Update .env File

```bash
# Edit .env file
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx

# Optional: Choose model (default is gpt-4-turbo-preview)
OPENAI_MODEL=gpt-3.5-turbo  # For cost savings
```

**Model Comparison**:
- `gpt-4-turbo-preview` - Most accurate, ~$0.01-0.03 per message
- `gpt-3.5-turbo` - Good accuracy, ~$0.001-0.002 per message

## Application Setup

### Step 1: Create Storage Directories

```bash
# Directories are auto-created, but you can manually create:
mkdir -p storage/sessions
mkdir -p storage/evidence
mkdir -p storage/exports
mkdir -p storage/logs
mkdir -p storage/cache
```

### Step 2: Complete .env Configuration

```bash
# Optional: Generate encryption key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Add to .env:
SESSION_ENCRYPTION_KEY=<generated_key>
```

Or keep it empty for auto-generation.

### Step 3: Verify Installation

```bash
# Test imports
python -c "import telethon; print('Telethon OK')"
python -c "import openai; print('OpenAI OK')"
python -c "from rich import print; print('[green]Rich OK[/green]')"

# All should print "OK"
```

## Verification

### Test the Application

```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run the application
python src/main.py

# You should see the main menu
```

### First-Time Login Test

1. Select "[1] Login Telegram Account"
2. Enter your API ID and API Hash
3. Enter your phone number (+country_code format)
4. Check Telegram app for OTP code
5. Enter the 5-digit code
6. You should see "Logged In Successfully"

### Troubleshooting Tests

```bash
# Check Python version
python --version

# Check pip packages
pip list

# Check specific packages
pip show telethon
pip show openai
pip show rich

# Test imports individually
python -c "from telethon import TelegramClient; print('✓ Telethon')"
python -c "from openai import AsyncOpenAI; print('✓ OpenAI')"
python -c "from rich import print; print('✓ Rich')"
```

## Troubleshooting

### Issue: "Python not found" or "python: command not found"

**Solution**: 
- Ensure Python is installed and in PATH
- Try `python3` instead of `python`
- On Windows, reinstall Python with "Add Python to PATH" checked

### Issue: "No module named 'telethon'"

**Solution**:
```bash
# Ensure virtual environment is activated
# Then reinstall:
pip install --upgrade telethon
```

### Issue: "Cannot find venv"

**Solution**:
```bash
# Recreate virtual environment
python -m venv venv

# Activate and reinstall
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Invalid API ID or API Hash"

**Solution**:
- Verify credentials from https://my.telegram.org
- Check for typos in .env file
- Ensure no extra spaces or quotes

### Issue: "Permission denied" on Linux

**Solution**:
```bash
# Check file permissions
ls -la venv/

# If needed, fix permissions
chmod -R u+x venv/bin/
```

### Issue: "ModuleNotFoundError" for cryptography

**Solution (Linux)**:
```bash
# Install development headers
sudo apt-get install libssl-dev libffi-dev python3-dev

# Reinstall requirements
pip install --upgrade --force-reinstall -r requirements.txt
```

### Issue: Out of memory during installation

**Solution**:
```bash
# Install one at a time
pip install telethon
pip install openai
pip install rich
# ... etc
```

### Issue: .env file not loading

**Solution**:
- Ensure .env file is in project root
- Check file name exactly: `.env` (not `.env.txt`)
- Ensure proper formatting (no spaces around =)

## Getting Help

If you encounter issues:

1. **Check logs**:
   ```bash
   tail storage/logs/error.log
   ```

2. **Verify configuration**:
   ```bash
   # Check .env file exists
   cat .env
   ```

3. **Test connectivity**:
   ```bash
   # Test Telegram API
   python -c "import telethon; print('Telethon working')"
   
   # Test OpenAI API
   python -c "from openai import AsyncOpenAI; print('OpenAI working')"
   ```

4. **Enable debug logging**:
   ```bash
   # In .env, set:
   LOG_LEVEL=DEBUG
   ```

## Next Steps

Once installation is complete:

1. See [README.md](README.md) for usage guide
2. See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
3. Review [.env.example](.env.example) for all configuration options

---

**Installation Complete!** 🎉

You're ready to start using the Telegram Content Compliance Analyzer.
