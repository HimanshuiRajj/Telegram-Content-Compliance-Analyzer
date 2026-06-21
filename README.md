# Telegram Content Compliance Analyzer v1.0

A professional terminal-based application for analyzing Telegram content compliance using official Telegram APIs and OpenAI's content analysis capabilities.

## Features

### 🔐 Authentication
- **Official Telegram API** - Uses Telethon for secure, authorized access
- **Multiple Accounts** - Manage and switch between multiple Telegram accounts
- **Session Management** - Encrypted session storage for quick reconnection
- **2FA Support** - Full support for two-factor authentication

### 📊 Content Analysis
- **Smart Message Collection** - Fetch messages from channels and groups
- **Flexible Message Range Selection** - Last N messages or custom date/ID ranges
- **AI-Powered Analysis** - OpenAI integration for comprehensive content classification
- **Risk Assessment** - Automatic risk scoring and confidence evaluation

### 📋 Categories Analyzed
- Legal Content
- Suspicious Content
- Scam
- Fraud
- Phishing
- Malware Mention
- Privacy Leak
- Copyright Concern
- Harassment
- Adult Content
- Extremist Content
- Other

### 📈 Reporting & Export
- **Multiple Formats**: PDF, HTML, JSON, CSV
- **Executive Summaries** - High-level compliance overview
- **Detailed Findings** - Message-by-message analysis
- **Risk Metrics** - High/Medium/Low risk categorization
- **Category Breakdown** - Distribution of findings by type

### 🖥️ Terminal UI
- **Rich Terminal Interface** - Professional colored tables and progress bars
- **Intuitive Navigation** - Menu-driven interface
- **Real-time Progress** - Live status updates during scanning
- **Clear Formatting** - Organized data presentation

### 💾 Storage & Logging
- **Organized Storage** - Dedicated directories for sessions, evidence, exports
- **Comprehensive Logging** - Separate logs for login, scanning, analysis, exports
- **Evidence Preservation** - Raw message data stored separately
- **Audit Trails** - Track all operations

## System Requirements

- **Python 3.9+**
- **Windows, macOS, or Linux**
- **Internet connection** (for Telegram and OpenAI APIs)
- **Minimum RAM**: 2GB
- **Minimum Disk Space**: 500MB

## Quick Start

### 1. Installation

```bash
# Clone or download the project
cd telegram-compliance-analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# Required:
# - TELEGRAM_API_ID (get from https://my.telegram.org)
# - TELEGRAM_API_HASH (get from https://my.telegram.org)
# - OPENAI_API_KEY (get from https://platform.openai.com)

# Optional: Set custom encryption key (auto-generated if not provided)
```

### 3. Run Application

```bash
python -m src.main

# Or if that doesn't work:
python src/main.py
```

## Workflow

### Main Menu
```
╔════════════════════════════════════════════╗
║ Telegram Content Compliance Analyzer v1.0 ║
╚════════════════════════════════════════════╝

[1] Login Telegram Account
[2] Load Existing Session
[3] Manage Accounts
[4] Exit
```

### Login Process
1. **Enter Credentials**
   - API ID and API Hash (from my.telegram.org)
   - Phone number in format: +<country_code><number>

2. **Receive OTP**
   - Check Telegram app for authentication code
   - Enter 5-digit code

3. **Handle 2FA**
   - If enabled, enter your password

4. **Save Session**
   - Sessions are automatically saved with encryption

### Analysis Workflow
1. **Select Channels/Groups**
   - View all available dialogs
   - Select using: `1`, `1,5,8`, `1-20`, or `all`

2. **Choose Message Range**
   - Last 100/500/1000/2000/5000 messages
   - Or custom date/ID range

3. **Automatic Analysis**
   - Messages are collected
   - Analyzed with OpenAI
   - Risk scores calculated

4. **Review Results**
   - Summary statistics
   - Category breakdown
   - Detailed findings

5. **Export Report**
   - Choose format: PDF, HTML, JSON, CSV, or All
   - Reports saved to storage/exports/

## Directory Structure

```
telegram-compliance-analyzer/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration
│   ├── telegram_client/
│   │   ├── __init__.py
│   │   ├── client.py           # Telegram API wrapper
│   │   └── session_manager.py  # Session management
│   ├── analyzer/
│   │   └── __init__.py         # OpenAI integration
│   ├── export/
│   │   └── __init__.py         # Report generation
│   ├── storage/
│   │   └── __init__.py         # Storage management
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── components.py       # UI components
│   │   ├── main_menu.py
│   │   ├── login.py
│   │   ├── dialogs.py
│   │   ├── scanner.py
│   │   └── results.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging setup
│       └── encryption.py       # Encryption utilities
├── storage/
│   ├── sessions/               # Encrypted sessions
│   ├── evidence/               # Raw message data
│   ├── exports/                # Generated reports
│   ├── logs/                   # Application logs
│   └── cache/                  # Cached data
├── requirements.txt            # Dependencies
├── .env.example               # Example environment
├── README.md                  # This file
└── INSTALL.md                 # Installation guide
```

## Configuration Options

Edit `.env` file:

```bash
# Telegram API
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

# OpenAI
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4-turbo-preview

# Storage
STORAGE_PATH=./storage
LOG_PATH=./storage/logs
SESSION_PATH=./storage/sessions
EVIDENCE_PATH=./storage/evidence
EXPORT_PATH=./storage/exports

# Performance
MAX_MESSAGES_PER_SCAN=5000
BATCH_SIZE=100
WORKER_THREADS=4

# Security
ENABLE_ENCRYPTION=true
ENABLE_AUDIT_LOG=true
```

## Security Features

- ✅ **Official APIs Only** - No unauthorized access methods
- ✅ **Encrypted Sessions** - Session data encrypted with Fernet
- ✅ **User-Authorized Content** - Only access to content user has permission to see
- ✅ **Audit Logging** - All operations logged for compliance
- ✅ **No Data Sharing** - No third-party data sharing
- ✅ **Resume Support** - Can pause and resume scans
- ✅ **Queue Management** - Batch processing for stability

## Logging

Logs are stored in `storage/logs/`:

- `login.log` - Authentication events
- `scan.log` - Message collection events
- `analysis.log` - AI analysis events
- `export.log` - Report generation events
- `error.log` - Error tracking
- `audit.log` - Compliance audit trail

## Performance Targets

- **Messages per Scan**: Up to 5,000
- **Batch Processing**: 100 messages per batch (configurable)
- **Analysis Time**: ~0.5-2 seconds per message (depending on OpenAI)
- **Memory Usage**: ~100-500MB depending on message volume
- **Session Persistence**: Encrypted storage for quick reconnection

## Troubleshooting

### Connection Issues
- Check internet connection
- Verify API credentials
- Check Telegram service status

### Authentication Failures
- Verify phone number format (+country_code)
- Check OTP code is correct
- Ensure 2FA password if enabled

### Analysis Issues
- Check OpenAI API key is valid
- Verify API rate limits not exceeded
- Check message content is not empty

### Export Problems
- Ensure storage/exports directory exists
- Check available disk space
- Verify write permissions

## Performance Optimization

### For Large Scans
1. Reduce `BATCH_SIZE` if memory is limited
2. Increase `WORKER_THREADS` for faster processing
3. Use custom date ranges instead of large message counts

### For Faster Analysis
1. Use `gpt-3.5-turbo` instead of `gpt-4` (less accurate but faster)
2. Increase `BATCH_SIZE` for parallel processing
3. Reduce `ANALYSIS_TIMEOUT` if needed

## API Costs

### Telegram API
- **Free** - Official Telegram API is free with API ID/Hash

### OpenAI API
- **gpt-4-turbo-preview**: ~$0.01-0.03 per message
- **gpt-3.5-turbo**: ~$0.001-0.002 per message
- Batch of 100 messages: $1-3 (approximately)

Use `gpt-3.5-turbo` for cost-effective analysis.

## Support & Documentation

For detailed information:
- See [INSTALL.md](INSTALL.md) for installation troubleshooting
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment

## License

This project uses official APIs and respects all terms of service:
- Telegram Bot API Terms: https://core.telegram.org/bots/api-terms
- OpenAI Terms: https://openai.com/policies/terms-of-use

## Disclaimer

This tool is designed for:
- Compliance analysis of your own content
- Content moderation of authorized channels
- Research and analysis with proper authorization

NOT for:
- Unauthorized data collection
- Privacy violations
- Harassment or surveillance
- Terms of service violations

Users are responsible for compliance with:
- Telegram Terms of Service
- OpenAI Terms of Use
- Local data protection laws
- Any relevant compliance regulations

## Version History

### v1.0.0 (Current)
- Initial release
- Multi-account support
- OpenAI integration
- PDF/HTML/JSON/CSV export
- Terminal UI with Rich
- Encrypted session management

---

**Made with ❤️ for Compliance Teams**
