"""Prompt loader for managing LLM prompts."""
from pathlib import Path
from typing import Dict
import logging

from src.config import config

logger = logging.getLogger(__name__)


class PromptLoader:
    """Load and manage LLM prompts."""
    
    def __init__(self, prompts_dir: str | Path = None):
        """
        Initialize prompt loader.
        
        Args:
            prompts_dir: Directory containing prompt files
        """
        self.prompts_dir = Path(prompts_dir or config.prompts_dir)
        self._prompts: Dict[str, str] = {}
        
        # Ensure prompts directory exists
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        (self.prompts_dir / "templates").mkdir(parents=True, exist_ok=True)
    
    def load_prompt(self, prompt_name: str) -> str:
        """
        Load prompt from file or cache.
        
        Args:
            prompt_name: Name of the prompt (without extension)
            
        Returns:
            Prompt text
        """
        if prompt_name in self._prompts:
            return self._prompts[prompt_name]
        
        # Try .txt file first
        prompt_file = self.prompts_dir / f"{prompt_name}.txt"
        if not prompt_file.exists():
            # Try templates directory with _template suffix
            prompt_file = self.prompts_dir / "templates" / f"{prompt_name}_template.txt"
        if not prompt_file.exists():
            # Try templates directory without suffix
            prompt_file = self.prompts_dir / "templates" / f"{prompt_name}.txt"
        
        if prompt_file.exists():
            with open(prompt_file, "r", encoding="utf-8") as f:
                prompt = f.read()
                self._prompts[prompt_name] = prompt
                return prompt
        
        # Return default prompt if file not found
        logger.warning(f"Prompt file not found: {prompt_name}, using default")
        return self._get_default_prompt(prompt_name)
    
    def format_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        Load and format prompt with variables.
        
        Args:
            prompt_name: Name of the prompt
            **kwargs: Variables to format the prompt
            
        Returns:
            Formatted prompt text
        """
        prompt_template = self.load_prompt(prompt_name)
        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            logger.warning(f"Missing variable in prompt {prompt_name}: {e}")
            return prompt_template
    
    def _get_default_prompt(self, prompt_name: str) -> str:
        """Get default prompt if file not found."""
        if prompt_name == "scoring_prompt":
            return """You are an expert recruiter analyzing candidate resumes against a job description.

Job Description:
{job_description}

Must-Have Requirements:
{must_have_requirements}

Candidate Resume:
{resume_text}

Candidate Name: {candidate_name}
Candidate Skills: {candidate_skills}

Please analyze and provide:
1. Overall match score (0-100)
2. Similarity score (0-100)
3. Must-have requirements matched (list)
4. Reason codes explaining the match
5. Specific resume sections that match JD requirements

Format your response as JSON:
{{
    "overall_score": <float>,
    "similarity_score": <float>,
    "must_have_matches": [<list>],
    "reason_codes": [<list>],
    "matched_sections": {{
        "requirement": "resume_section_reference"
    }}
}}"""
        else:
            return "Please analyze the provided information."

