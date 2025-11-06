"""Hybrid scoring system."""
from typing import Dict
import logging

from src.config import config
from .rule_boosts import RuleBoosts

logger = logging.getLogger(__name__)


class HybridScorer:
    """Calculate hybrid scores combining similarity and rule-based boosts."""
    
    def __init__(self):
        """Initialize hybrid scorer."""
        self.rule_boosts = RuleBoosts()
    
    def calculate_final_score(
        self,
        similarity_score: float,
        resume: Dict,
        job_description: Dict,
        llm_analysis: Dict,
    ) -> Dict:
        """
        Calculate final hybrid score.
        
        Args:
            similarity_score: Similarity score from LLM (0-100)
            resume: Structured resume JSON
            job_description: Structured JD JSON
            llm_analysis: LLM analysis results
            
        Returns:
            Dictionary with final score and breakdown
        """
        # Normalize similarity score to 0-1
        similarity_normalized = similarity_score / 100.0
        
        # Calculate rule-based boosts
        must_have_boost = self.rule_boosts.calculate_must_have_boost(
            resume, job_description, llm_analysis
        )
        
        recency_boost = self.rule_boosts.calculate_recency_boost(resume)
        
        # Apply weights
        weighted_similarity = similarity_normalized * config.similarity_weight
        weighted_must_have = must_have_boost * config.must_have_boost_weight
        weighted_recency = recency_boost * config.recency_boost_weight
        
        # Calculate final score (0-100)
        final_score_normalized = weighted_similarity + weighted_must_have + weighted_recency
        final_score = final_score_normalized * 100.0
        
        # Ensure score is in valid range
        final_score = max(0.0, min(100.0, final_score))
        
        logger.debug(
            f"Score calculation - Similarity: {similarity_score:.2f}, "
            f"Must-Have Boost: {must_have_boost:.2f}, "
            f"Recency Boost: {recency_boost:.2f}, "
            f"Final: {final_score:.2f}"
        )
        
        return {
            "final_score": round(final_score, 2),
            "similarity_score": round(similarity_score, 2),
            "must_have_boost": round(must_have_boost * 100, 2),
            "recency_boost": round(recency_boost * 100, 2),
            "score_breakdown": {
                "similarity_weighted": round(weighted_similarity * 100, 2),
                "must_have_weighted": round(weighted_must_have * 100, 2),
                "recency_weighted": round(weighted_recency * 100, 2),
            },
        }

