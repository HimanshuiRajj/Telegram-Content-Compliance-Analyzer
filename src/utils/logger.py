"""Logger utility module"""
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from src.config import Settings


class LoggerSetup:
    """Configure and manage application logging"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._setup_loggers()

    def _setup_loggers(self):
        """Setup multiple log files"""
        loggers = {
            "login": "login.log",
            "scan": "scan.log",
            "analysis": "analysis.log",
            "export": "export.log",
            "error": "error.log",
            "audit": "audit.log",
        }

        log_path = Path(self.settings.log_path)

        for logger_name, filename in loggers.items():
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, self.settings.log_level))

            # File handler
            handler = logging.handlers.RotatingFileHandler(
                log_path / filename,
                maxBytes=10_000_000,  # 10MB
                backupCount=5
            )

            formatter = logging.Formatter(self.settings.log_format)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger instance"""
        return logging.getLogger(name)


# Convenience functions
def get_login_logger():
    """Get login logger"""
    return logging.getLogger("login")


def get_scan_logger():
    """Get scan logger"""
    return logging.getLogger("scan")


def get_analysis_logger():
    """Get analysis logger"""
    return logging.getLogger("analysis")


def get_export_logger():
    """Get export logger"""
    return logging.getLogger("export")


def get_error_logger():
    """Get error logger"""
    return logging.getLogger("error")


def get_audit_logger():
    """Get audit logger"""
    return logging.getLogger("audit")
