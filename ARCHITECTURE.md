# Project Summary & Architecture

## Overview

The **Telegram Content Compliance Analyzer** is a professional-grade, terminal-based Python application designed for analyzing Telegram content compliance using official APIs and AI-powered content analysis.

## Project Statistics

- **Total Lines of Code**: ~2,500+
- **Python Version**: 3.9+
- **Main Dependencies**: 24
- **Modules**: 8 core modules
- **UI Components**: 5 specialized interfaces
- **Export Formats**: 4 (PDF, HTML, JSON, CSV)
- **Supported Categories**: 12 content categories

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│         Telegram Content Compliance Analyzer v1.0       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │          Rich Terminal User Interface             │  │
│  │  (Main Menu, Login, Dialogs, Scanner, Results)   │  │
│  └────────────────┬────────────────────────────────┘  │
│                   │                                    │
│  ┌────────────────▼────────────────────────────────┐  │
│  │       Application Core Logic (main.py)          │  │
│  │  - Workflow orchestration                       │  │
│  │  - Session management                           │  │
│  │  - Analysis pipeline                            │  │
│  └────┬────────────────────────────────────────┬──┘  │
│       │                                        │      │
│  ┌────▼──────────────┐  ┌──────────────────────▼────┐ │
│  │ Telegram Client   │  │ AI Analyzer (OpenAI)      │ │
│  │ (Telethon)        │  │ (AsyncOpenAI)             │ │
│  │ - Login           │  │ - Risk Scoring            │ │
│  │ - Dialogs         │  │ - Categorization          │ │
│  │ - Messages        │  │ - Batch Processing        │ │
│  │ - Sessions        │  │ - Confidence Scores       │ │
│  └────┬──────────────┘  └──────────────┬─────────────┘ │
│       │                                │               │
│  ┌────▼──────────────────────────────▼────┐           │
│  │         Storage & Logging               │           │
│  │ - Sessions (encrypted)                  │           │
│  │ - Evidence (raw data)                   │           │
│  │ - Logs (audit trail)                    │           │
│  │ - Cache                                 │           │
│  └────┬────────────────────────────────────┘           │
│       │                                                │
│  ┌────▼────────────────────────────────────┐          │
│  │     Export & Reporting                  │          │
│  │ - PDF Generation                        │          │
│  │ - HTML Reports                          │          │
│  │ - JSON Export                           │          │
│  │ - CSV Export                            │          │
│  └─────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

## Module Structure

### Core Modules

```
src/
├── main.py                          # Application entry point & orchestration
│   └── TelegramComplianceApp       # Main application class
│
├── config/
│   └── settings.py                 # Configuration management (Pydantic)
│       └── Settings class          # All configuration options
│
├── telegram_client/
│   ├── client.py                   # Telethon wrapper
│   │   └── TelegramClient          # Telegram API operations
│   └── session_manager.py          # Session persistence
│       └── SessionManager          # Multi-account support
│
├── analyzer/
│   └── __init__.py                 # OpenAI integration
│       ├── MessageAnalyzer         # Content analysis
│       └── AnalysisResult          # Results aggregation
│
├── export/
│   └── __init__.py                 # Report generation
│       └── ReportExporter          # Multi-format export
│
├── storage/
│   └── __init__.py                 # Data persistence
│       └── StorageManager          # Evidence & cache
│
├── ui/                             # Terminal user interface
│   ├── components.py               # Rich UI elements
│   ├── main_menu.py               # Main menu interface
│   ├── login.py                    # Login workflow UI
│   ├── dialogs.py                  # Dialog selection UI
│   ├── scanner.py                  # Progress display
│   └── results.py                  # Results display
│
└── utils/
    ├── logger.py                   # Logging configuration
    └── encryption.py               # Session encryption
```

## Data Flow Diagram

```
User Input
    ↓
┌─────────────────────────────┐
│   Authentication Phase      │
│ - Get Telegram credentials  │
│ - Request OTP               │
│ - Verify 2FA (if needed)    │
│ - Get user info             │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│   Dialog Selection Phase    │
│ - Fetch available dialogs   │
│ - Display in table          │
│ - Get user selection        │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│   Message Collection Phase  │
│ - Fetch messages from API   │
│ - Store raw data            │
│ - Prepare for analysis      │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│   AI Analysis Phase         │
│ - Batch processing          │
│ - OpenAI API calls          │
│ - Risk scoring              │
│ - Categorization            │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│   Results Processing Phase  │
│ - Aggregate findings        │
│ - Calculate statistics      │
│ - Display summary           │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│   Export Phase              │
│ - Generate reports          │
│ - Save to disk              │
│ - Display locations         │
└──────────────┬──────────────┘
               ↓
            Complete
```

## Key Components Explained

### 1. Telegram Client (Telethon)
- **Purpose**: Official Telegram API wrapper
- **Features**: 
  - Async communication
  - Session persistence
  - Multi-account support
- **Security**: API-only, user-authorized access

### 2. AI Analyzer (OpenAI)
- **Purpose**: Content classification and risk assessment
- **Features**:
  - Real-time analysis
  - Risk scoring (0.0-1.0)
  - Confidence scores
  - Batch processing
- **Categories**: 12 predefined compliance categories

### 3. Session Manager
- **Purpose**: Account session persistence
- **Features**:
  - Encrypted storage
  - Multiple accounts
  - Metadata tracking
  - Automatic timestamps

### 4. Report Exporter
- **Purpose**: Multi-format report generation
- **Formats**:
  - PDF (via ReportLab)
  - HTML (via Jinja2)
  - JSON (native)
  - CSV (tabular data)

### 5. Terminal UI (Rich)
- **Purpose**: Professional terminal interface
- **Components**:
  - Colored tables
  - Progress bars
  - Panels & boxes
  - Live updates

## Technology Stack

### Core Framework
- **Telethon** (1.35.0) - Telegram API
- **OpenAI** (1.12.0) - AI Analysis
- **Rich** (13.7.0) - Terminal UI
- **Pydantic** (2.5.2) - Config validation

### Data Processing
- **Asyncio** - Async operations
- **Aiofiles** (23.2.1) - Async file I/O
- **Pandas** (2.1.3) - Data analysis (optional)

### Security
- **Cryptography** (41.0.7) - Session encryption
- **Python-dotenv** (1.0.0) - Config management

### Reporting
- **ReportLab** (4.0.9) - PDF generation
- **Jinja2** (3.1.2) - HTML templating

### Logging
- **Python Logging** - Built-in logging
- **Rotating Handlers** - Log rotation

## Performance Characteristics

### Processing Speed
- **Message Collection**: 50-100 msg/sec
- **Analysis Speed**: 0.5-2 sec/msg (varies by model)
- **Report Generation**: 1-5 sec

### Memory Usage
- **Base Application**: 100-150 MB
- **Per 100 Messages**: +50-100 MB
- **Peak Usage**: Depends on batch size

### API Costs (Approximate)
- **Telegram**: Free
- **OpenAI gpt-4-turbo**: $0.01-0.03 per message
- **OpenAI gpt-3.5-turbo**: $0.001-0.002 per message

### Scalability
- **Max Messages/Scan**: 10,000 (configurable)
- **Max Channels**: 200+ (Telegram limit)
- **Concurrent Analyses**: Sequential (can be parallelized)

## Security Architecture

### Authentication
```
User Phone
    ↓
Telegram OTP
    ↓
2FA Password (optional)
    ↓
Session Token
    ↓
Encrypted Session File
```

### Data Protection
- **Session Files**: Fernet encryption
- **Evidence Storage**: Plaintext (encrypted filesystem recommended)
- **API Keys**: Environment variables only
- **Logs**: Plain text (apply filesystem permissions)

### Access Control
- **Session Persistence**: Per-user encrypted files
- **Multi-Account**: Separate encrypted sessions
- **File Permissions**: Strict (600 for .env, 700 for dirs)

## Workflow Sequences

### Login Workflow
```
1. Display credentials prompt
2. Connect to Telegram
3. Send code request
4. Get OTP from user
5. Verify code
6. Handle 2FA if needed
7. Get user info
8. Save encrypted session
9. Display success
```

### Analysis Workflow
```
1. Fetch available dialogs
2. Display dialog list
3. Get user selection
4. Get message range
5. Collect messages
6. Analyze with OpenAI
7. Calculate statistics
8. Display results
9. Offer export options
10. Generate reports
```

### Export Workflow
```
1. Get export format choice
2. Prepare data structures
3. Generate report
4. Save to file
5. Return file path
6. Display completion
```

## Configuration Hierarchy

```
Defaults (hard-coded)
    ↓
.env.example (template)
    ↓
.env (user configuration)
    ↓
Environment Variables
    ↓
Runtime Configuration
```

## Storage Organization

```
storage/
├── sessions/
│   ├── default.session (encrypted)
│   ├── account1.session (encrypted)
│   └── sessions_metadata.json
│
├── evidence/
│   ├── messages_account1_20240101.json
│   ├── findings_account1_20240101.json
│   └── ...
│
├── exports/
│   ├── compliance_report_20240101_120000.pdf
│   ├── compliance_report_20240101_120000.html
│   ├── compliance_report_20240101_120000.json
│   └── compliance_report_20240101_120000.csv
│
├── logs/
│   ├── login.log
│   ├── scan.log
│   ├── analysis.log
│   ├── export.log
│   ├── error.log
│   └── audit.log
│
└── cache/
    ├── dialogs_default.json
    └── ...
```

## Error Handling Strategy

```
User Error
    ↓
Validate Input
    ↓
   Pass ✓ → Continue
    ↓
   Fail ✗ → Log Error
         ↓
         Display Message
         ↓
         Retry or Cancel
```

## Logging Strategy

```
Operation → Logger → Handler → File
                ↓
           File Handler
           (rotating 10MB, 5 backups)
                ↓
           Log Files in storage/logs/
```

## Testing Recommendations

### Unit Tests
```python
# Test configuration validation
# Test encryption/decryption
# Test message parsing
# Test analysis categorization
```

### Integration Tests
```python
# Test Telegram connection
# Test OpenAI integration
# Test export formats
# Test session persistence
```

### E2E Tests
```python
# Full login workflow
# Full analysis workflow
# Multi-account handling
# Export verification
```

## Future Enhancement Opportunities

1. **Web Interface** - Flask/FastAPI backend
2. **Database Backend** - PostgreSQL/MongoDB
3. **Real-time Monitoring** - WebSocket updates
4. **Advanced Filtering** - Complex query support
5. **Machine Learning** - Custom model training
6. **Multi-language** - Internationalization
7. **Mobile App** - React Native client
8. **Distributed Processing** - Celery worker pool

## Maintenance Guidelines

### Regular Tasks
- Monitor API usage
- Review logs for errors
- Update dependencies quarterly
- Test disaster recovery
- Review security settings

### Performance Monitoring
- Track analysis speed
- Monitor memory usage
- Check API costs
- Analyze bottlenecks

### Documentation
- Keep .env.example updated
- Update README for new features
- Document custom configurations
- Maintain change log

## Compliance & Standards

### Follows
- ✅ Telegram Bot API Terms
- ✅ OpenAI Terms of Use
- ✅ GDPR principles (with user consent)
- ✅ Python best practices
- ✅ Async/await patterns

### Respects
- ✅ User privacy
- ✅ API rate limits
- ✅ Terms of service
- ✅ Data protection laws

---

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Language** | Python 3.9+ |
| **Main Framework** | Telethon + OpenAI + Rich |
| **Architecture** | Modular, async, layered |
| **Performance** | 50-100 msg/sec collection |
| **Security** | Encrypted sessions, API-only |
| **Scalability** | Up to 10k messages/scan |
| **Export Formats** | PDF, HTML, JSON, CSV |
| **Deployment** | Single server or cloud |

For more details, see:
- [README.md](README.md) - Complete usage guide
- [INSTALL.md](INSTALL.md) - Installation instructions
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production setup
- [CONFIG.md](CONFIG.md) - Configuration reference
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
