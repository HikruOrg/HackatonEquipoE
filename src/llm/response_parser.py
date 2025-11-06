"""Parse LLM structured responses."""
from typing import Dict, List
import json
import logging

logger = logging.getLogger(__name__)


class ResponseParser:
    """Parse and validate LLM responses."""
    
    @staticmethod
    def parse_analysis_response(response: str | Dict) -> Dict:
        """
        Parse LLM analysis response.
        
        Args:
            response: Raw response string or dict
            
        Returns:
            Parsed analysis dictionary
        """
        if isinstance(response, dict):
            return response
        
        try:
            # Try to parse as JSON
            parsed = json.loads(response)
            return parsed
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, attempting extraction")
            # Try to extract JSON from text
            return ResponseParser._extract_json_from_text(response)
    
    @staticmethod
    def _extract_json_from_text(text: str) -> Dict:
        """
        Extract JSON from text response.
        
        Args:
            text: Text that may contain JSON
            
        Returns:
            Extracted dictionary
        """
        import re
        
        # Try to find JSON object in text
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Return default structure if extraction fails
        logger.warning("Could not extract JSON from response")
        return {
            "overall_score": 0.0,
            "similarity_score": 0.0,
            "must_have_matches": [],
            "reason_codes": [],
            "matched_sections": {},
        }
    
    @staticmethod
    def validate_analysis_response(response: Dict) -> bool:
        """
        Validate analysis response structure.
        
        Args:
            response: Analysis response dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["overall_score", "similarity_score"]
        
        if not all(field in response for field in required_fields):
            return False
        
        # Validate score ranges
        if not (0.0 <= response.get("overall_score", -1) <= 100.0):
            return False
        
        if not (0.0 <= response.get("similarity_score", -1) <= 100.0):
            return False
        
        return True

