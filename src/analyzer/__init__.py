"""Message Analyzer using OpenAI"""

import json
from typing import Dict, Optional, List
import asyncio
from openai import AsyncOpenAI, RateLimitError
import logging


class MessageAnalyzer:
    """Analyze messages using OpenAI API"""
    
    CATEGORIES = [
        "Legal Content",
        "Suspicious Content",
        "Scam",
        "Fraud",
        "Phishing",
        "Malware Mention",
        "Privacy Leak",
        "Copyright Concern",
        "Harassment",
        "Adult Content",
        "Extremist Content",
        "Other",
    ]
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview", timeout: int = 30):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.timeout = timeout
        self.logger = logging.getLogger("analysis")
    
    async def analyze_message(self, message_text: str, message_id: int) -> Optional[Dict]:
        """Analyze a single message"""
        if not message_text or len(message_text.strip()) == 0:
            return {
                "message_id": message_id,
                "category": "Legal Content",
                "risk_score": 0.0,
                "confidence_score": 1.0,
                "explanation": "Empty message",
                "evidence": []
            }
        
        try:
            prompt = self._create_analysis_prompt(message_text, message_id)
            
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a content compliance analyzer. Analyze the given message and return a JSON response."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=500,
                ),
                timeout=self.timeout
            )
            
            result_text = response.choices[0].message.content
            
            # Parse JSON response
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    return self._default_analysis(message_id, message_text)
            
            result['message_id'] = message_id
            return result
        
        except asyncio.TimeoutError:
            self.logger.warning(f"Timeout analyzing message {message_id}")
            return None
        except RateLimitError:
            self.logger.warning("Rate limit exceeded, retrying...")
            await asyncio.sleep(1)
            return await self.analyze_message(message_text, message_id)
        except Exception as e:
            self.logger.error(f"Error analyzing message {message_id}: {e}")
            return None
    
    async def analyze_batch(self, messages: List[Dict], batch_size: int = 10) -> List[Dict]:
        """Analyze a batch of messages"""
        results = []
        
        for i in range(0, len(messages), batch_size):
            batch = messages[i:i + batch_size]
            tasks = [
                self.analyze_message(msg['text'], msg['id'])
                for msg in batch
            ]
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if result is not None and not isinstance(result, Exception):
                    results.append(result)
            
            # Rate limiting
            if i + batch_size < len(messages):
                await asyncio.sleep(0.5)
        
        return results
    
    def _create_analysis_prompt(self, message_text: str, message_id: int) -> str:
        """Create analysis prompt for OpenAI"""
        categories_str = ", ".join(self.CATEGORIES)
        
        return f"""Analyze the following Telegram message for compliance and security issues.

Message ID: {message_id}
Message Text: "{message_text}"

Evaluate the message against these categories: {categories_str}

Return a JSON response with the following structure:
{{
    "category": "<one of the categories>",
    "risk_score": <0.0 to 1.0>,
    "confidence_score": <0.0 to 1.0>,
    "explanation": "<brief explanation of the risk>",
    "evidence": [<list of specific concerns if any>]
}}

Risk Score: 0.0 (no risk) to 1.0 (critical risk)
Confidence Score: How confident you are in this assessment

Respond ONLY with the JSON object, no additional text."""
    
    def _default_analysis(self, message_id: int, message_text: str) -> Dict:
        """Return default analysis for fallback"""
        return {
            "message_id": message_id,
            "category": "Legal Content",
            "risk_score": 0.0,
            "confidence_score": 0.5,
            "explanation": "Unable to analyze message",
            "evidence": []
        }


class AnalysisResult:
    """Store analysis results"""
    
    def __init__(self):
        self.findings: List[Dict] = []
        self.categories: Dict[str, int] = {cat: 0 for cat in MessageAnalyzer.CATEGORIES}
        self.high_risk_count = 0
        self.medium_risk_count = 0
        self.low_risk_count = 0
    
    def add_finding(self, analysis: Dict) -> None:
        """Add an analysis finding"""
        if analysis['risk_score'] >= 0.7:
            self.high_risk_count += 1
        elif analysis['risk_score'] >= 0.4:
            self.medium_risk_count += 1
        else:
            self.low_risk_count += 1
        
        category = analysis.get('category', 'Other')
        self.categories[category] = self.categories.get(category, 0) + 1
        
        self.findings.append(analysis)
    
    def get_summary(self) -> Dict:
        """Get results summary"""
        return {
            "total_findings": len(self.findings),
            "high_risk": self.high_risk_count,
            "medium_risk": self.medium_risk_count,
            "low_risk": self.low_risk_count,
            "categories": self.categories,
            "findings": self.findings,
        }
