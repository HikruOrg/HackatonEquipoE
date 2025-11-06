"""Reason code mapping."""
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class ReasonCodes:
    """Generate and manage reason codes for scoring explanations."""
    
    REASON_CODE_TYPES = {
        "SKILL_MATCH": "Habilidades que coinciden con el JD",
        "EXPERIENCE_MATCH": "Experiencia relevante encontrada",
        "MUST_HAVE_MATCH": "Requisitos obligatorios cumplidos",
        "RECENT_EXP": "Experiencia reciente (últimos 2 años)",
        "EDUCATION_MATCH": "Educación relevante",
        "MISSING_REQUIREMENT": "Requisitos faltantes",
    }
    
    @staticmethod
    def format_reason_codes(reason_codes: List[str]) -> List[str]:
        """
        Format reason codes for display.
        
        Args:
            reason_codes: List of reason code strings
            
        Returns:
            Formatted reason codes
        """
        formatted = []
        for code in reason_codes:
            if isinstance(code, str):
                # Check if it's a structured code (e.g., "SKILL_MATCH: Python, JavaScript")
                if ":" in code:
                    formatted.append(code)
                else:
                    # Add description if available
                    description = ReasonCodes.REASON_CODE_TYPES.get(code, code)
                    formatted.append(f"{code}: {description}")
            else:
                formatted.append(str(code))
        
        return formatted
    
    @staticmethod
    def generate_reason_codes_from_analysis(llm_analysis: Dict, resume: Dict, job_description: Dict) -> List[str]:
        """
        Generate reason codes from LLM analysis.
        
        Args:
            llm_analysis: LLM analysis results
            resume: Structured resume JSON
            job_description: Structured JD JSON
            
        Returns:
            List of reason codes
        """
        reason_codes = []
        
        # Get reason codes from LLM analysis
        llm_reason_codes = llm_analysis.get("reason_codes", [])
        reason_codes.extend(llm_reason_codes)
        
        # Add additional reason codes based on analysis
        must_have_matches = llm_analysis.get("must_have_matches", [])
        if must_have_matches:
            reason_codes.append(f"MUST_HAVE_MATCH: {len(must_have_matches)} requisitos cumplidos")
        
        # Check for recent experience
        experiences = resume.get("experience", [])
        if experiences:
            reason_codes.append("EXPERIENCE_MATCH: Experiencia laboral encontrada")
        
        # Check for education match
        education = resume.get("education", [])
        if education:
            reason_codes.append("EDUCATION_MATCH: Educación relevante encontrada")
        
        return reason_codes

