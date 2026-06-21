"""Storage management module"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging


class StorageManager:
    """Manage storage of evidence and data"""
    
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.evidence_path = self.storage_path / "evidence"
        self.cache_path = self.storage_path / "cache"
        
        self.evidence_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("storage")
    
    def save_raw_messages(self, messages: List[Dict], session_name: str) -> Optional[str]:
        """Save raw message data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.evidence_path / f"messages_{session_name}_{timestamp}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(messages)} raw messages to {file_path}")
            return str(file_path)
        
        except Exception as e:
            self.logger.error(f"Error saving messages: {e}")
            return None
    
    def save_findings(self, findings: List[Dict], session_name: str) -> Optional[str]:
        """Save analysis findings"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.evidence_path / f"findings_{session_name}_{timestamp}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(findings, f, indent=2)
            
            self.logger.info(f"Saved {len(findings)} findings to {file_path}")
            return str(file_path)
        
        except Exception as e:
            self.logger.error(f"Error saving findings: {e}")
            return None
    
    def cache_dialogs(self, dialogs: List[Dict], session_name: str) -> Optional[str]:
        """Cache dialog information"""
        try:
            file_path = self.cache_path / f"dialogs_{session_name}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'dialogs': dialogs
                }, f, indent=2)
            
            return str(file_path)
        
        except Exception as e:
            self.logger.error(f"Error caching dialogs: {e}")
            return None
    
    def load_cached_dialogs(self, session_name: str) -> Optional[List[Dict]]:
        """Load cached dialogs"""
        try:
            file_path = self.cache_path / f"dialogs_{session_name}.json"
            
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('dialogs', [])
        
        except Exception as e:
            self.logger.error(f"Error loading cached dialogs: {e}")
        
        return None
