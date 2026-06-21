# Deployment Guide

Production deployment guide for the Telegram Content Compliance Analyzer.

## Table of Contents
1. [Production Checklist](#production-checklist)
2. [Server Setup](#server-setup)
3. [Security Hardening](#security-hardening)
4. [Performance Optimization](#performance-optimization)
5. [Monitoring & Logging](#monitoring--logging)
6. [Backup & Recovery](#backup--recovery)
7. [Scaling](#scaling)

## Production Checklist

Before deploying to production:

- [ ] All dependencies installed and tested
- [ ] .env file configured with production values
- [ ] API keys and credentials secured
- [ ] Firewall rules configured
- [ ] SSL/TLS certificates obtained (if needed)
- [ ] Backup strategy implemented
- [ ] Monitoring tools set up
- [ ] Logging configured
- [ ] User documentation prepared
- [ ] Incident response plan created

## Server Setup

### Option 1: Linux Server (Recommended)

#### 1. Server Requirements
- **OS**: Ubuntu 20.04 LTS or higher
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 50GB (for logs and evidence storage)
- **Network**: 100 Mbps minimum

#### 2. Initial Setup

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    python3.9 python3-pip python3-venv \
    build-essential libssl-dev libffi-dev \
    git curl wget \
    supervisor \
    fail2ban \
    certbot

# Create application user
sudo useradd -m -s /bin/bash compliance
sudo su - compliance
```

#### 3. Deploy Application

```bash
# Clone repository
git clone <repository-url> /home/compliance/app
cd /home/compliance/app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set permissions
chmod -R 755 storage/
chmod 600 .env
```

#### 4. Configure systemd Service

Create `/etc/systemd/system/compliance-analyzer.service`:

```ini
[Unit]
Description=Telegram Content Compliance Analyzer
After=network.target

[Service]
Type=simple
User=compliance
WorkingDirectory=/home/compliance/app
Environment="PATH=/home/compliance/app/venv/bin"
ExecStart=/home/compliance/app/venv/bin/python src/main.py
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=compliance-analyzer

[Install]
WantedBy=multi-user.target
```

Enable the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable compliance-analyzer
sudo systemctl start compliance-analyzer

# Check status
sudo systemctl status compliance-analyzer
```

### Option 2: Windows Server

#### 1. Requirements
- Windows Server 2019 or higher
- Python 3.9+
- 4GB+ RAM
- Administrative privileges

#### 2. Setup

```powershell
# Install Python if not present
# Download from https://www.python.org/downloads/

# Create application directory
New-Item -ItemType Directory -Path "C:\ComplianceAnalyzer"
cd C:\ComplianceAnalyzer

# Clone repository
git clone <repository-url> .

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Create Windows Service

Using NSSM (Non-Sucking Service Manager):

```powershell
# Download NSSM
# https://nssm.cc/download

# Install service
nssm install ComplianceAnalyzer "C:\ComplianceAnalyzer\venv\Scripts\python.exe" "C:\ComplianceAnalyzer\src\main.py"

# Set working directory
nssm set ComplianceAnalyzer AppDirectory "C:\ComplianceAnalyzer"

# Start service
nssm start ComplianceAnalyzer

# Verify
nssm status ComplianceAnalyzer
```

## Security Hardening

### 1. Environment Variables

Never commit `.env` file:

```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "storage/evidence/*" >> .gitignore
echo "storage/exports/*" >> .gitignore
```

### 2. File Permissions

```bash
# Restrict .env file
chmod 600 .env

# Restrict storage directories
chmod 700 storage/
chmod 700 storage/sessions/
chmod 700 storage/evidence/
chmod 700 storage/exports/

# Ensure only application user can read logs
chmod 750 storage/logs/
```

### 3. API Key Management

Use environment variable rotation:

```bash
# Rotate OpenAI API key periodically
# Set new key in .env
sudo systemctl restart compliance-analyzer

# Monitor for unusual API usage
# Check OpenAI dashboard for rate limit alerts
```

### 4. Network Security

```bash
# UFW Firewall (Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp    # SSH only
sudo ufw allow 443/tcp   # HTTPS if applicable
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### 5. Fail2Ban Configuration

Create `/etc/fail2ban/jail.local`:

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
```

```bash
sudo systemctl restart fail2ban
```

### 6. SSL/TLS (if exposing API)

```bash
# Using Let's Encrypt
sudo certbot certonly --standalone -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Performance Optimization

### 1. Batch Processing

Optimize in `.env`:

```bash
# Increase batch size for faster processing
BATCH_SIZE=500

# Increase worker threads for parallel analysis
WORKER_THREADS=8

# Set max messages for scanning
MAX_MESSAGES_PER_SCAN=10000
```

### 2. Memory Management

```python
# Monitor memory usage
free -h

# Adjust batch size if memory is limited
# Smaller batches = less memory but slower processing
```

### 3. API Rate Limiting

```bash
# Configure in code for production
# src/analyzer/__init__.py
# Implement exponential backoff for rate limits
```

### 4. Caching

Enable dialog caching:

```python
# Sessions and dialog info are cached
# Cache valid for session duration
# Clear cache if needed: rm -rf storage/cache/*
```

## Monitoring & Logging

### 1. Centralized Logging

Using rsyslog:

```bash
# On production server:
# Edit /etc/rsyslog.d/30-compliance.conf

*.* @@logs.example.com:514
```

### 2. Log Rotation

Logrotate configuration at `/etc/logrotate.d/compliance-analyzer`:

```bash
/home/compliance/app/storage/logs/* {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 compliance compliance
    sharedscripts
    postrotate
        systemctl reload compliance-analyzer > /dev/null 2>&1 || true
    endscript
}
```

### 3. Monitoring Tools

```bash
# Install monitoring
sudo apt-get install -y prometheus node-exporter grafana

# Configure alerts for:
# - High API usage
# - Failed authentications
# - Analysis errors
# - Disk space
```

### 4. Health Checks

```bash
# Create health check script
#!/bin/bash
systemctl is-active compliance-analyzer > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Service down!" | mail -s "Alert" admin@example.com
fi
```

## Backup & Recovery

### 1. Backup Strategy

```bash
# Daily backups of sensitive data
0 2 * * * /home/compliance/backup.sh

# Backup script:
#!/bin/bash
BACKUP_DIR="/mnt/backups"
SOURCE_DIR="/home/compliance/app/storage"
DATE=$(date +%Y%m%d_%H%M%S)

# Exclude raw evidence, keep metadata
rsync -av --exclude='evidence/*.json' \
    $SOURCE_DIR $BACKUP_DIR/backup_$DATE/

# Keep 30 days of backups
find $BACKUP_DIR -name "backup_*" -mtime +30 -exec rm -rf {} \;
```

### 2. Disaster Recovery

```bash
# Keep .env file in secure backup
# Keep API credentials encrypted

# Recovery procedure:
1. Restore application from version control
2. Restore .env from secure backup
3. Restore storage directories
4. Restart service
5. Verify functionality
```

### 3. Database Backups

```bash
# If using database for findings:
mysqldump -u user -p database > backup_$(date +%Y%m%d).sql
gzip backup_$(date +%Y%m%d).sql
```

## Scaling

### 1. Multi-Instance Setup

```nginx
# Load balancer configuration
upstream compliance_backends {
    server instance1.example.com:5000;
    server instance2.example.com:5000;
    server instance3.example.com:5000;
}

server {
    listen 80;
    server_name compliance.example.com;
    
    location / {
        proxy_pass http://compliance_backends;
    }
}
```

### 2. Database Backend (Optional)

For multiple instances, use shared database:

```bash
# Add to requirements.txt
SQLAlchemy==2.0.0
psycopg2-binary==2.9.0

# Configure in .env
DATABASE_URL=postgresql://user:pass@db.example.com/compliance
```

### 3. Message Queue (Optional)

For async processing:

```bash
# Add to requirements.txt
celery==5.3.0
redis==5.0.0

# Use Redis for task queue
```

## Automated Monitoring Script

Create `monitor.sh`:

```bash
#!/bin/bash

LOGFILE="/var/log/compliance-monitor.log"
EMAIL="admin@example.com"

check_service() {
    if ! systemctl is-active compliance-analyzer > /dev/null; then
        echo "$(date): Service down" >> $LOGFILE
        systemctl start compliance-analyzer
        echo "Service restarted" | mail -s "Compliance Alert" $EMAIL
    fi
}

check_disk() {
    USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ $USAGE -gt 90 ]; then
        echo "$(date): Disk usage $USAGE%" >> $LOGFILE
        echo "Disk usage high" | mail -s "Alert" $EMAIL
    fi
}

check_api() {
    API_USAGE=$(curl -s https://api.openai.com/dashboard/billing/usage \
        -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.total_usage')
    
    if [ $API_USAGE -gt 1000 ]; then
        echo "$(date): High API usage: $API_USAGE" >> $LOGFILE
    fi
}

check_service
check_disk
check_api
```

Schedule with cron:

```bash
# Run every 15 minutes
*/15 * * * * /home/compliance/monitor.sh
```

## Performance Metrics

Monitor these KPIs:

```bash
# Messages per minute
grep "Collected" storage/logs/scan.log | tail -100 | \
    awk '{print $NF}' | sort | uniq -c

# Average analysis time
grep "risk_score" storage/logs/analysis.log | \
    awk '{sum+=$2} END {print sum/NR " seconds average"}'

# API cost tracking
# Check OpenAI dashboard regularly
```

## Troubleshooting Production Issues

### Issue: High Memory Usage

```bash
# Check memory
free -h
ps aux | grep python

# Solution:
# 1. Reduce BATCH_SIZE in .env
# 2. Restart service
# 3. Monitor memory after changes
```

### Issue: API Rate Limiting

```bash
# Check logs
grep "rate_limit" storage/logs/analysis.log

# Solution:
# 1. Reduce batch size
# 2. Add delays between requests
# 3. Upgrade OpenAI plan
```

### Issue: Session Timeouts

```bash
# Check logs
grep "timeout" storage/logs/login.log

# Solution:
# 1. Increase ANALYSIS_TIMEOUT in .env
# 2. Check network connectivity
# 3. Verify API credentials
```

## Compliance & Auditing

### 1. Audit Logging

```bash
# Enable audit logging in .env
ENABLE_AUDIT_LOG=true

# Review audit logs
tail -f storage/logs/audit.log
```

### 2. Data Retention

```bash
# Set retention policy
# Delete old evidence after 90 days
find storage/evidence -type f -mtime +90 -delete

# Schedule with cron
0 3 * * * find storage/evidence -type f -mtime +90 -delete
```

### 3. Compliance Reports

Generate compliance reports:

```bash
# Monthly report script
python generate_compliance_report.py
```

## Support & Escalation

For production issues:

1. **Check logs first**:
   ```bash
   tail -f storage/logs/error.log
   ```

2. **Review status**:
   ```bash
   systemctl status compliance-analyzer
   ```

3. **Restart if needed**:
   ```bash
   sudo systemctl restart compliance-analyzer
   ```

4. **Contact support** with:
   - Error messages from logs
   - System information
   - Recent changes
   - API usage statistics

---

**Production deployment checklist complete!** ✅

Your Telegram Content Compliance Analyzer is ready for production use.
