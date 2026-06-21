# Configuration Guide

Complete reference for all configuration options in the Telegram Content Compliance Analyzer.

## Environment Variables (.env)

### Telegram Configuration

```bash
# Required: Get from https://my.telegram.org
TELEGRAM_API_ID=123456789
TELEGRAM_API_HASH=abcdefg0123456789abcdefg0123456

# Telegram API settings
# Default connection timeout (seconds)
TELEGRAM_TIMEOUT=30
```

### OpenAI Configuration

```bash
# Required: Get from https://platform.openai.com/api/keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx

# Model selection
# Options: gpt-4-turbo-preview, gpt-3.5-turbo, gpt-4
# Default: gpt-4-turbo-preview
OPENAI_MODEL=gpt-4-turbo-preview

# Analysis timeout in seconds
# Increase if you get timeout errors
ANALYSIS_TIMEOUT=30
```

### Application Settings

```bash
# Application metadata
APP_NAME=Telegram Content Compliance Analyzer
APP_VERSION=1.0.0

# Application timezone (optional)
APP_TIMEZONE=UTC
```

### Storage Configuration

```bash
# Base storage directory
STORAGE_PATH=./storage

# Subdirectories (relative to STORAGE_PATH)
LOG_PATH=./storage/logs
SESSION_PATH=./storage/sessions
EVIDENCE_PATH=./storage/evidence
EXPORT_PATH=./storage/exports
CACHE_PATH=./storage/cache

# These are created automatically if they don't exist
```

### Logging Configuration

```bash
# Log level
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log format
# Python logging format string
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Log to console as well (optional)
LOG_TO_CONSOLE=false
```

### Session & Encryption

```bash
# Encryption key for session files
# If not provided, a key will be auto-generated
# Format: Fernet key (base64 encoded)
SESSION_ENCRYPTION_KEY=

# To generate a new key:
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Enable/disable encryption
ENABLE_ENCRYPTION=true
```

### Performance Configuration

```bash
# Maximum messages to collect per scan
MAX_MESSAGES_PER_SCAN=5000

# Batch size for processing messages
# Increase for faster processing (uses more memory)
# Decrease if you get memory errors
BATCH_SIZE=100

# Number of worker threads for parallel processing
WORKER_THREADS=4
```

### Security Configuration

```bash
# Enable audit logging
ENABLE_AUDIT_LOG=true

# Session timeout (minutes)
# How long until session expires if inactive
SESSION_TIMEOUT=60

# Max login attempts before lockout
MAX_LOGIN_ATTEMPTS=5

# Lockout duration (minutes)
LOCKOUT_DURATION=30
```

### Debug Configuration

```bash
# Enable debug mode
# Provides more verbose logging
DEBUG=false

# Enable development mode
# Skips some security checks (NEVER use in production)
DEVELOPMENT_MODE=false
```

## Advanced Configuration

### Custom Analysis Categories

To add or modify analysis categories, edit `src/analyzer/__init__.py`:

```python
CATEGORIES = [
    "Legal Content",
    "Suspicious Content",
    # Add your custom categories here
    "Custom Category 1",
    "Custom Category 2",
]
```

### Custom Export Templates

Edit HTML template in `src/export/__init__.py` to customize report format.

### Custom UI Colors

Edit colors in `src/ui/components.py`:

```python
# Change color scheme
color="cyan"  # cyan, magenta, yellow, red, green, blue, etc.
```

## Performance Tuning

### For Large-Scale Scans

```bash
# Increase batch size
BATCH_SIZE=500

# Increase workers
WORKER_THREADS=8

# Increase message limit
MAX_MESSAGES_PER_SCAN=10000

# Use faster (but less accurate) model
OPENAI_MODEL=gpt-3.5-turbo

# Increase timeout for large batches
ANALYSIS_TIMEOUT=60
```

### For Cost Optimization

```bash
# Use cheaper model
OPENAI_MODEL=gpt-3.5-turbo

# Reduce messages per scan
MAX_MESSAGES_PER_SCAN=1000

# Reduce batch size (fewer parallel requests)
BATCH_SIZE=50
```

### For Production Servers

```bash
# High performance setup
BATCH_SIZE=250
WORKER_THREADS=8
MAX_MESSAGES_PER_SCAN=5000
ANALYSIS_TIMEOUT=45
OPENAI_MODEL=gpt-3.5-turbo

# Optimize storage
LOG_LEVEL=WARNING
CACHE_PATH=/tmp/compliance_cache
```

### For Low-Resource Environments

```bash
# Conservative setup
BATCH_SIZE=25
WORKER_THREADS=2
MAX_MESSAGES_PER_SCAN=500
ANALYSIS_TIMEOUT=60

# Use slower but cheaper model
OPENAI_MODEL=gpt-3.5-turbo

# Reduce log verbosity
LOG_LEVEL=ERROR
```

## .env Example Files

### Minimal Setup

```bash
TELEGRAM_API_ID=123456789
TELEGRAM_API_HASH=abcdef0123456789
OPENAI_API_KEY=sk-proj-xxxx
```

### Development Setup

```bash
TELEGRAM_API_ID=123456789
TELEGRAM_API_HASH=abcdef0123456789
OPENAI_API_KEY=sk-proj-xxxx

LOG_LEVEL=DEBUG
DEBUG=true
MAX_MESSAGES_PER_SCAN=100
BATCH_SIZE=10
```

### Production Setup

```bash
TELEGRAM_API_ID=123456789
TELEGRAM_API_HASH=abcdef0123456789
OPENAI_API_KEY=sk-proj-xxxx

LOG_LEVEL=INFO
STORAGE_PATH=/var/lib/compliance/storage
SESSION_ENCRYPTION_KEY=<generated-key>

MAX_MESSAGES_PER_SCAN=5000
BATCH_SIZE=250
WORKER_THREADS=8
OPENAI_MODEL=gpt-3.5-turbo

ENABLE_AUDIT_LOG=true
ENABLE_ENCRYPTION=true
```

## Troubleshooting Configuration Issues

### Issue: "Settings validation error"

**Solution**: Check .env file for:
- Missing required values
- Syntax errors (spaces around =)
- Invalid data types (API_ID should be number)

### Issue: "Cannot find storage directories"

**Solution**: 
- Ensure write permissions to current directory
- Manually create: `mkdir -p storage/{sessions,evidence,exports,logs,cache}`

### Issue: "Memory usage too high"

**Solution**:
- Reduce `BATCH_SIZE` (default 100, try 50)
- Reduce `WORKER_THREADS` (default 4, try 2)
- Reduce `MAX_MESSAGES_PER_SCAN`

### Issue: "API rate limits exceeded"

**Solution**:
- Reduce `BATCH_SIZE`
- Increase `ANALYSIS_TIMEOUT`
- Switch to `gpt-3.5-turbo` model

### Issue: "Encryption key errors"

**Solution**: Generate new key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Add to .env:
```bash
SESSION_ENCRYPTION_KEY=<paste-generated-key>
```

## Environment Validation

Validate your configuration:

```bash
# Check configuration
python -c "from src.config import Settings; s = Settings(); print('✓ Configuration valid')"

# Check API connectivity
python -c "from telethon import TelegramClient; print('✓ Telethon OK')"

# Check OpenAI connectivity
python -c "from openai import AsyncOpenAI; print('✓ OpenAI OK')"
```

## Dynamic Configuration

You can change configuration at runtime:

```python
from src.config import Settings

settings = Settings()

# Modify settings
settings.batch_size = 200
settings.log_level = "DEBUG"
```

## Configuration Best Practices

1. **Security**
   - Never commit .env to version control
   - Use strong encryption keys
   - Rotate API keys periodically

2. **Performance**
   - Monitor memory usage
   - Adjust batch size based on available RAM
   - Use appropriate model for accuracy/cost tradeoff

3. **Reliability**
   - Enable audit logging in production
   - Set reasonable timeouts
   - Monitor API usage and costs

4. **Maintainability**
   - Document custom configurations
   - Use version control for code, not secrets
   - Keep configuration files consistent

## Environment-Specific Configuration

Create multiple .env files:

```bash
# .env.local (development)
# .env.staging (staging)
# .env.production (production)

# Load appropriate file based on environment
python -m src.main --env=production
```

## Configuration Validation Schema

Configuration is validated against:

```python
{
    "telegram_api_id": int,
    "telegram_api_hash": str,
    "openai_api_key": str,
    "storage_path": str,
    "max_messages_per_scan": int (0-10000),
    "batch_size": int (1-1000),
    "worker_threads": int (1-16),
    "analysis_timeout": int (5-300),
    "log_level": str ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    "enable_encryption": bool,
    "enable_audit_log": bool,
}
```

---

For quick setup, see [QUICKSTART.md](QUICKSTART.md)  
For installation help, see [INSTALL.md](INSTALL.md)  
For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)
