"""Resume text parsing to structured JSON."""
import json
import uuid
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResumeParser:
    """Parse resume text to structured JSON format."""
    
    def __init__(self, use_llm: bool = False, llm_client=None):
        """
        Initialize resume parser.
        
        Args:
            use_llm: Whether to use LLM for intelligent parsing
            llm_client: LLM client instance (if use_llm=True)
        """
        self.use_llm = use_llm
        self.llm_client = llm_client
    
    def parse_from_text(self, text: str, candidate_id: Optional[str] = None) -> Dict:
        """
        Parse resume text to structured JSON.
        
        Args:
            text: Raw text extracted from PDF or JSON
            candidate_id: Optional candidate ID (generated if not provided)
            
        Returns:
            Structured resume JSON
        """
        if not candidate_id:
            candidate_id = str(uuid.uuid4())
        
        if self.use_llm and self.llm_client:
            return self._parse_with_llm(text, candidate_id)
        else:
            return self._parse_basic(text, candidate_id)
    
    def _parse_basic(self, text: str, candidate_id: str) -> Dict:
        """
        Basic parsing without LLM (for JSON files or simple extraction).
        
        Args:
            text: Raw text
            candidate_id: Candidate ID
            
        Returns:
            Basic structured resume
        """
        # Try to parse as JSON first
        try:
            data = json.loads(text)
            # Validate structure
            if self._validate_resume_json(data):
                return data
        except json.JSONDecodeError:
            pass
        
        # If not JSON, create basic structure
        return {
            "candidate_id": candidate_id,
            "name": self._extract_name(text),
            "skills": self._extract_skills(text),
            "experience": self._extract_experience(text),
            "education": self._extract_education(text),
            "raw_text": text,
        }
    
    def _parse_with_llm(self, text: str, candidate_id: str) -> Dict:
        """
        Parse with LLM for intelligent extraction.
        
        Args:
            text: Raw text
            candidate_id: Candidate ID
            
        Returns:
            Structured resume JSON
        """
        if not self.llm_client:
            logger.warning("LLM client not available, using basic parsing")
            return self._parse_basic(text, candidate_id)
        
        try:
            # Import PromptLoader here to avoid circular dependency
            from src.prompts import PromptLoader
            
            prompt_loader = PromptLoader()
            prompt = prompt_loader.load_prompt("parse_resume")
            
            # Replace placeholders
            prompt = prompt.replace("{{candidate_id}}", candidate_id)
            prompt = prompt.replace("{{raw_text}}", text)
            prompt = prompt.replace("{{resume_text}}", text)
            
            # Call LLM
            logger.info("Using LLM to parse resume...")
            response = self.llm_client.invoke(prompt)
            
            # Response is already a dict from JsonOutputParser
            if isinstance(response, dict):
                parsed_data = response
            else:
                # Fallback: try to parse as JSON string
                import json
                parsed_data = json.loads(response)
            
            # Ensure required fields
            if not self._validate_resume_json(parsed_data):
                logger.warning("LLM parsing returned invalid structure, using basic parsing")
                return self._parse_basic(text, candidate_id)
            
            logger.info("✓ Successfully parsed resume with LLM")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing with LLM: {e}, falling back to basic parsing")
            return self._parse_basic(text, candidate_id)
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name from text."""
        # Simple heuristic: first line that looks like a name
        lines = text.split("\n")
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and line[0].isupper():
                return line
        return "Unknown"
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text."""
        # Common tech skills keywords
        skills_keywords = [
            "python", "javascript", "java", "react", "node", "sql", "aws",
            "docker", "kubernetes", "git", "linux", "mongodb", "postgresql",
            "typescript", "angular", "vue", "django", "flask", "fastapi"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience from text."""
        # Basic extraction - would be improved with LLM
        experiences = []
        
        # Look for common patterns
        lines = text.split("\n")
        current_exp = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Simple heuristic: lines with dates might be experience entries
            if any(year in line for year in ["2020", "2021", "2022", "2023", "2024"]):
                if current_exp:
                    experiences.append(current_exp)
                current_exp = {
                    "company": "Unknown",
                    "position": line,
                    "start_date": "",
                    "end_date": "",
                    "description": "",
                }
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences[:5]  # Limit to 5 most recent
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education from text."""
        # Basic extraction
        education = []
        
        # Look for common education keywords
        edu_keywords = ["university", "college", "degree", "bachelor", "master", "phd"]
        
        lines = text.split("\n")
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in edu_keywords):
                education.append({
                    "institution": line,
                    "degree": "",
                    "field": "",
                    "year": None,
                })
        
        return education[:3]  # Limit to 3 entries
    
    def _validate_resume_json(self, data: Dict) -> bool:
        """Validate resume JSON structure."""
        required_fields = ["candidate_id", "name", "skills", "experience", "education", "raw_text"]
        return all(field in data for field in required_fields)
    
    def parse_from_json(self, json_path: str) -> Dict:
        """
        Parse resume from JSON file.
        
        Args:
            json_path: Path to JSON file
            
        Returns:
            Structured resume JSON
        """
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not self._validate_resume_json(data):
            raise ValueError(f"Invalid resume JSON structure: {json_path}")
        
        return data

