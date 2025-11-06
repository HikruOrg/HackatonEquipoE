"""Map hits to resume sections."""
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class HitMapper:
    """Map scoring hits to specific resume sections."""
    
    @staticmethod
    def map_hits_to_sections(
        llm_analysis: Dict,
        resume: Dict,
        job_description: Dict,
    ) -> Dict[str, str]:
        """
        Map hits to resume sections.
        
        Args:
            llm_analysis: LLM analysis results
            resume: Structured resume JSON
            job_description: Structured JD JSON
            
        Returns:
            Dictionary mapping requirements to resume sections
        """
        matched_sections = llm_analysis.get("matched_sections", {})
        
        # Enhance with explicit section references
        enhanced_mappings = {}
        
        for requirement, section_ref in matched_sections.items():
            enhanced_mappings[requirement] = section_ref
        
        # Add mappings for must-have matches
        must_have_matches = llm_analysis.get("must_have_matches", [])
        for match in must_have_matches:
            # Try to find where this match appears in resume
            section = HitMapper._find_section_for_match(match, resume)
            if section:
                enhanced_mappings[match] = section
        
        return enhanced_mappings
    
    @staticmethod
    def _find_section_for_match(match: str, resume: Dict) -> str:
        """Find resume section where match appears."""
        match_lower = match.lower()
        
        # Check skills
        skills = resume.get("skills", [])
        for skill in skills:
            if match_lower in skill.lower():
                return f"Skills: {skill}"
        
        # Check experience
        experiences = resume.get("experience", [])
        for exp in experiences:
            company = exp.get("company", "")
            position = exp.get("position", "")
            description = exp.get("description", "")
            
            if match_lower in company.lower() or match_lower in position.lower():
                return f"Experience > {company} > {position}"
            
            if match_lower in description.lower():
                return f"Experience > {company} > {position} > Description"
        
        # Check education
        education = resume.get("education", [])
        for edu in education:
            institution = edu.get("institution", "")
            if match_lower in institution.lower():
                return f"Education > {institution}"
        
        # Check raw text
        raw_text = resume.get("raw_text", "")
        if match_lower in raw_text.lower():
            return "Resume Text"
        
        return ""

