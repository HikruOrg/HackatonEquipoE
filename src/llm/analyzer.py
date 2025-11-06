"""LLM-based resume/JD analysis."""
from typing import Dict
import logging

from .client import LLMClient
from src.prompts.prompt_loader import PromptLoader

logger = logging.getLogger(__name__)


class LLMAnalyzer:
    """Analyze resumes against job descriptions using LLM."""
    
    def __init__(self, llm_client: LLMClient, prompt_loader: PromptLoader):
        """
        Initialize LLM analyzer.
        
        Args:
            llm_client: LLM client instance
            prompt_loader: Prompt loader instance
        """
        self.llm_client = llm_client
        self.prompt_loader = prompt_loader
    
    def analyze_candidate(self, resume: Dict, job_description: Dict) -> Dict:
        """
        Analyze candidate resume against job description.
        
        Args:
            resume: Structured resume JSON
            job_description: Structured JD JSON
            
        Returns:
            Analysis results with scores and reason codes
        """
        logger.info(f"Analyzing candidate {resume.get('candidate_id', 'unknown')} against JD {job_description.get('jd_id', 'unknown')}")
        
        # Load and format scoring prompt
        prompt = self.prompt_loader.format_prompt(
            "scoring_prompt",
            job_description=job_description.get("description", ""),
            must_have_requirements="\n".join(job_description.get("must_have_requirements", [])),
            resume_text=resume.get("raw_text", ""),
            candidate_name=resume.get("name", "Unknown"),
            candidate_skills=", ".join(resume.get("skills", [])),
        )
        
        # Invoke LLM
        try:
            response = self.llm_client.invoke(prompt, parse_json=True)
            
            # Validate response structure
            if not isinstance(response, dict):
                raise ValueError("LLM response is not a dictionary")
            
            # Ensure required fields
            analysis = {
                "overall_score": response.get("overall_score", 0.0),
                "similarity_score": response.get("similarity_score", 0.0),
                "must_have_matches": response.get("must_have_matches", []),
                "reason_codes": response.get("reason_codes", []),
                "matched_sections": response.get("matched_sections", {}),
            }
            
            logger.info(f"Analysis complete. Overall score: {analysis['overall_score']}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing candidate: {str(e)}")
            # Return default analysis on error
            return {
                "overall_score": 0.0,
                "similarity_score": 0.0,
                "must_have_matches": [],
                "reason_codes": ["ERROR: Analysis failed"],
                "matched_sections": {},
            }

