"""Job Description text parsing to structured JSON."""
import json
import uuid
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class JDParser:
    """Parse job description text to structured JSON format."""
    
    def __init__(self, use_llm: bool = False, llm_client=None):
        """
        Initialize JD parser.
        
        Args:
            use_llm: Whether to use LLM for intelligent parsing
            llm_client: LLM client instance (if use_llm=True)
        """
        self.use_llm = use_llm
        self.llm_client = llm_client
    
    def parse_from_text(self, text: str, jd_id: Optional[str] = None) -> Dict:
        """
        Parse JD text to structured JSON.
        
        Args:
            text: Raw text extracted from PDF or JSON
            jd_id: Optional JD ID (generated if not provided)
            
        Returns:
            Structured JD JSON
        """
        if not jd_id:
            jd_id = str(uuid.uuid4())
        
        if self.use_llm and self.llm_client:
            return self._parse_with_llm(text, jd_id)
        else:
            return self._parse_basic(text, jd_id)
    
    def _parse_basic(self, text: str, jd_id: str) -> Dict:
        """
        Basic parsing without LLM.
        
        Args:
            text: Raw text
            jd_id: JD ID
            
        Returns:
            Basic structured JD
        """
        # Try to parse as JSON first
        try:
            data = json.loads(text)
            # Validate structure
            if self._validate_jd_json(data):
                return data
        except json.JSONDecodeError:
            pass
        
        # If not JSON, create basic structure
        return {
            "jd_id": jd_id,
            "title": self._extract_title(text),
            "must_have_requirements": self._extract_must_have(text),
            "nice_to_have": self._extract_nice_to_have(text),
            "description": text,
            "experience_years_required": self._extract_years_required(text),
            "raw_text": text,
        }
    
    def _parse_with_llm(self, text: str, jd_id: str) -> Dict:
        """
        Parse with LLM for intelligent extraction.
        
        Args:
            text: Raw text
            jd_id: JD ID
            
        Returns:
            Structured JD JSON
        """
        if not self.llm_client:
            logger.warning("LLM client not available, using basic parsing")
            return self._parse_basic(text, jd_id)
        
        try:
            # Import PromptLoader here to avoid circular dependency
            from src.prompts import PromptLoader
            
            prompt_loader = PromptLoader()
            prompt = prompt_loader.load_prompt("parse_job_description")
            
            # Replace placeholders
            prompt = prompt.replace("{{jd_id}}", jd_id)
            prompt = prompt.replace("{{raw_text}}", text)
            prompt = prompt.replace("{{job_description_text}}", text)
            
            # Call LLM
            logger.info("Using LLM to parse job description...")
            response = self.llm_client.invoke(prompt)
            
            # Response is already a dict from JsonOutputParser
            if isinstance(response, dict):
                parsed_data = response
            else:
                # Fallback: try to parse as JSON string
                import json
                parsed_data = json.loads(response)
            
            # Ensure required fields
            if not self._validate_jd_json(parsed_data):
                logger.warning("LLM parsing returned invalid structure, using basic parsing")
                return self._parse_basic(text, jd_id)
            
            logger.info("✓ Successfully parsed JD with LLM")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing with LLM: {e}, falling back to basic parsing")
            return self._parse_basic(text, jd_id)
    
    def _extract_title(self, text: str) -> str:
        """Extract job title from text."""
        lines = text.split("\n")
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line) < 100:  # Title is usually short
                # Common title keywords
                if any(keyword in line.lower() for keyword in ["developer", "engineer", "manager", "analyst", "specialist"]):
                    return line
        return "Job Title"
    
    def _extract_must_have(self, text: str) -> List[str]:
        """Extract must-have requirements from text."""
        requirements = []
        text_lower = text.lower()
        
        # Look for sections with "must have", "required", "essential"
        lines = text.split("\n")
        in_must_have_section = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ["must have", "required", "essential", "mandatory"]):
                in_must_have_section = True
                continue
            
            if in_must_have_section:
                if line.strip() and (line.strip().startswith("-") or line.strip().startswith("•")):
                    requirements.append(line.strip().lstrip("-•").strip())
                elif "nice to have" in line_lower or "preferred" in line_lower:
                    break
        
        # If no structured section found, extract common requirements
        if not requirements:
            skills_keywords = [
                "python", "javascript", "java", "react", "node", "sql", "aws",
                "docker", "kubernetes", "git", "linux", "mongodb", "postgresql"
            ]
            
            for skill in skills_keywords:
                if skill in text_lower:
                    requirements.append(skill.title())
        
        return requirements[:10]  # Limit to 10 requirements
    
    def _extract_nice_to_have(self, text: str) -> List[str]:
        """Extract nice-to-have requirements from text."""
        requirements = []
        text_lower = text.lower()
        
        # Look for sections with "nice to have", "preferred", "bonus"
        lines = text.split("\n")
        in_nice_to_have_section = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ["nice to have", "preferred", "bonus", "plus"]):
                in_nice_to_have_section = True
                continue
            
            if in_nice_to_have_section:
                if line.strip() and (line.strip().startswith("-") or line.strip().startswith("•")):
                    requirements.append(line.strip().lstrip("-•").strip())
        
        return requirements[:10]  # Limit to 10 requirements
    
    def _extract_years_required(self, text: str) -> int:
        """Extract years of experience required."""
        import re
        
        # Look for patterns like "3+ years", "5 years", etc.
        patterns = [
            r"(\d+)\+?\s*years?\s*(?:of\s*)?experience",
            r"(\d+)\+?\s*years?\s*(?:of\s*)?exp",
            r"minimum\s*(\d+)\s*years",
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return int(match.group(1))
        
        return 0  # Default to 0 if not found
    
    def _validate_jd_json(self, data: Dict) -> bool:
        """Validate JD JSON structure."""
        required_fields = ["jd_id", "title", "must_have_requirements", "description", "raw_text"]
        return all(field in data for field in required_fields)
    
    def parse_from_json(self, json_path: str) -> Dict:
        """
        Parse JD from JSON file.
        
        Args:
            json_path: Path to JSON file
            
        Returns:
            Structured JD JSON
        """
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not self._validate_jd_json(data):
            raise ValueError(f"Invalid JD JSON structure: {json_path}")
        
        return data

