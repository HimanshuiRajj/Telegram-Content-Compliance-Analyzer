# Quick Start Guide

Get the Telegram Content Compliance Analyzer up and running in 5 minutes.

## Step 1: Prerequisites (2 minutes)

### Create Required Accounts
1. **Telegram**: https://web.telegram.org/ - your personal account
2. **OpenAI**: https://platform.openai.com/signup - for API access

### Install Python
- **Windows/macOS/Linux**: https://www.python.org/downloads/ (Python 3.9+)

### Verify Installation
```bash
python --version  # Should show Python 3.9 or higher
```

## Step 2: Download & Setup (1 minute)

```bash
# Download the project
git clone <repository-url>
cd telegram-compliance-analyzer

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure (1 minute)

### Get Telegram API Credentials
1. Go to https://my.telegram.org
2. Click "API development tools"
3. Create an app and copy:
   - **API ID**
   - **API Hash**

### Get OpenAI API Key
1. Go to https://platform.openai.com/api/keys
2. Create new secret key
3. Copy the key (save it - you can't see it again!)

### Create .env File
```bash
# Copy example
cp .env.example .env

# Edit .env with your values
# Windows: notepad .env
# macOS/Linux: nano .env
```

Add your values:
```bash
TELEGRAM_API_ID=123456789
TELEGRAM_API_HASH=abcdefg123456789
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
```

## Step 4: Run (1 minute)

```bash
# Make sure virtual environment is activated
python src/main.py
```

You should see:
```
╔════════════════════════════════════════════╗
║ Telegram Content Compliance Analyzer v1.0 ║
╚════════════════════════════════════════════╝

[1] Login Telegram Account
[2] Load Existing Session
[3] Manage Accounts
[4] Exit
```

## Your First Analysis

### 1. Login to Telegram
- Select **[1] Login Telegram Account**
- Enter your API ID and Hash (from Step 3)
- Enter your phone: `+1234567890` (with country code)
- Check Telegram app for OTP code
- Enter the 5-digit code

### 2. Select Channels/Groups
- Choose which channels/groups to scan
- Example: `1,3,5` (scan channels 1, 3, and 5)

### 3. Choose Message Range
- Last 100 messages (fast, quick test)
- Or Last 1000 messages (full analysis)

### 4. Wait for Analysis
- Application analyzes each message
- Shows progress in real-time

### 5. View & Export Results
- See findings summary
- Export as PDF, HTML, JSON, or CSV

## Common Commands

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run the application
python src/main.py

# View logs
tail storage/logs/analysis.log

# View reports
# Windows: explorer storage\exports
# macOS/Linux: ls -la storage/exports
```

## What Gets Analyzed?

The analyzer checks for:
- ✅ Scams & Fraud
- ✅ Phishing attempts
- ✅ Malware mentions
- ✅ Privacy leaks
- ✅ Copyright concerns
- ✅ Harassment
- ✅ Adult content
- ✅ Extremist content

Each message gets:
- 📊 Risk Score (0.0-1.0)
- 🎯 Category classification
- 💡 Explanation
- 📝 Evidence references

## Costs

### Telegram API
- **Free** - Official API is free

### OpenAI API
- **Per message**: $0.001-$0.003 (varies by model)
- **100 messages**: ~$0.10-$0.30
- **1000 messages**: ~$1-$3

## Troubleshooting

### "Module not found" error
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### "Invalid API ID"
- Check https://my.telegram.org for correct values
- Verify no typos in .env file
- No spaces around `=` in .env

### "Connection failed"
- Check internet connection
- Verify API credentials
- Check Telegram service status

### "API rate limit exceeded"
- Wait a minute
- Or reduce batch size in .env:
  ```bash
  BATCH_SIZE=50
  ```

## Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Installation Help**: See [INSTALL.md](INSTALL.md)
3. **Production Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## Example Output

```
╔════════════════════════════════════════════╗
║ Logged In Successfully                     ║
╠════════════════════════════════════════════╣
║ Name     : John Doe                        ║
║ Username : @johndoe                        ║
║ Phone    : +1 XXXXXXX890                   ║
╚════════════════════════════════════════════╝

Available Channels & Groups
┌─────┬──────────────────────┬─────────┬─────────┐
│ ID  │ Name                 │ Members │ Unread  │
├─────┼──────────────────────┼─────────┼─────────┤
│ 1   │ General Updates      │ 1,250   │ 42      │
│ 2   │ Tech News            │ 3,421   │ 18      │
│ 3   │ My Group             │ 32      │ 5       │
└─────┴──────────────────────┴─────────┴─────────┘

✓ Selected 3 dialog(s)

Scanning Channel...
████████████████████░░░░░░░░░ 65.4%
3287 / 5000 Messages

Findings Summary
┌──────────────┬───────┐
│ Metric       │ Count │
├──────────────┼───────┤
│ Total Find.  │  47   │
│ High Risk    │   8   │
│ Medium Risk  │  15   │
│ Low Risk     │  24   │
└──────────────┴───────┘
```

## Performance Tips

### For Faster Analysis
- Use smaller message ranges (100-500)
- Use `gpt-3.5-turbo` instead of `gpt-4` (cheaper & faster)
- Increase `BATCH_SIZE` in .env

### For Lower Costs
- Use `gpt-3.5-turbo` model (~10x cheaper)
- Analyze fewer messages
- Analyze during off-peak hours

### For Production
- See [DEPLOYMENT.md](DEPLOYMENT.md) for full setup

## Key Features at a Glance

| Feature | Details |
|---------|---------|
| **Login** | Phone number + OTP, 2FA support |
| **Accounts** | Multiple accounts, encrypted sessions |
| **Analysis** | OpenAI integration, real-time processing |
| **Export** | PDF, HTML, JSON, CSV formats |
| **Logging** | Comprehensive audit trails |
| **Security** | Encrypted sessions, API-only access |

---

**Ready to start?** Run `python src/main.py` and follow the prompts!

For help: See [README.md](README.md) or [INSTALL.md](INSTALL.md)
