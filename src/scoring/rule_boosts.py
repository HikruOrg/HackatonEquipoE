"""Rule-based scoring boosts."""
from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RuleBoosts:
    """Calculate rule-based boosts for scoring."""
    
    def calculate_must_have_boost(
        self,
        resume: Dict,
        job_description: Dict,
        llm_analysis: Dict,
    ) -> float:
        """
        Calculate boost based on must-have requirements matched.
        
        Args:
            resume: Structured resume JSON
            job_description: Structured JD JSON
            llm_analysis: LLM analysis results
            
        Returns:
            Boost value (0.0 to 1.0)
        """
        must_have_requirements = job_description.get("must_have_requirements", [])
        
        if not must_have_requirements:
            return 0.0
        
        # Get matches from LLM analysis
        matches = llm_analysis.get("must_have_matches", [])
        
        # Also check resume skills against requirements
        resume_skills = [s.lower() for s in resume.get("skills", [])]
        resume_text_lower = resume.get("raw_text", "").lower()
        
        matched_count = 0
        for requirement in must_have_requirements:
            req_lower = requirement.lower()
            
            # Check if requirement is in matches
            if any(req_lower in match.lower() for match in matches):
                matched_count += 1
                continue
            
            # Check if requirement keyword is in skills
            if any(req_lower in skill for skill in resume_skills):
                matched_count += 1
                continue
            
            # Check if requirement is in raw text
            if req_lower in resume_text_lower:
                matched_count += 1
        
        # Calculate boost (0.0 to 1.0)
        boost = matched_count / len(must_have_requirements) if must_have_requirements else 0.0
        
        logger.debug(f"Must-have boost: {matched_count}/{len(must_have_requirements)} = {boost:.2f}")
        return min(1.0, boost)  # Cap at 1.0
    
    def calculate_recency_boost(self, resume: Dict) -> float:
        """
        Calculate boost based on recency of experience.
        
        Args:
            resume: Structured resume JSON
            
        Returns:
            Boost value (0.0 to 1.0)
        """
        experiences = resume.get("experience", [])
        
        if not experiences:
            return 0.0
        
        # Find most recent experience
        current_year = datetime.now().year
        most_recent_year = 0
        
        for exp in experiences:
            end_date = exp.get("end_date", "")
            start_date = exp.get("start_date", "")
            
            # Try to extract year from date
            year = self._extract_year(end_date or start_date)
            if year:
                most_recent_year = max(most_recent_year, year)
        
        if most_recent_year == 0:
            return 0.0
        
        # Calculate boost based on how recent (last 2 years = full boost)
        years_ago = current_year - most_recent_year
        
        if years_ago <= 0:
            boost = 1.0  # Current year
        elif years_ago <= 2:
            boost = 1.0 - (years_ago * 0.3)  # Decay over 2 years
        else:
            boost = max(0.0, 0.4 - ((years_ago - 2) * 0.1))  # Further decay
        
        logger.debug(f"Recency boost: {most_recent_year} ({years_ago} years ago) = {boost:.2f}")
        return max(0.0, min(1.0, boost))
    
    def _extract_year(self, date_str: str) -> int:
        """Extract year from date string."""
        if not date_str:
            return 0
        
        import re
        
        # Try to find 4-digit year
        match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if match:
            return int(match.group())
        
        return 0

