"""CSV export functionality."""
import csv
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

from src.config import config

logger = logging.getLogger(__name__)


class CSVExporter:
    """Export ranked results to CSV."""
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize CSV exporter.
        
        Args:
            output_dir: Output directory (defaults to config.output_dir)
        """
        self.output_dir = Path(output_dir or config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_results(self, results: List[Dict], filename: Optional[str] = None) -> str:
        """
        Export ranked results to CSV.
        
        Args:
            results: List of ranked candidate results
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to exported CSV file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ranked_candidates_{timestamp}.csv"
        
        file_path = self.output_dir / filename
        
        # Define CSV columns
        fieldnames = [
            "rank",
            "candidate_id",
            "name",
            "overall_score",
            "similarity_score",
            "must_have_hits",
            "recency_boost",
            "reason_codes",
            "matched_requirements",
        ]
        
        # Write CSV
        with open(file_path, "w", newline="", encoding=config.csv_encoding) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                row = {
                    "rank": result.get("rank", ""),
                    "candidate_id": result.get("candidate_id", ""),
                    "name": result.get("name", ""),
                    "overall_score": result.get("final_score", 0.0),
                    "similarity_score": result.get("similarity_score", 0.0),
                    "must_have_hits": len(result.get("must_have_matches", [])),
                    "recency_boost": result.get("recency_boost", 0.0),
                    "reason_codes": "; ".join(result.get("reason_codes", [])),
                    "matched_requirements": "; ".join(result.get("must_have_matches", [])),
                }
                writer.writerow(row)
        
        logger.info(f"Exported {len(results)} results to {file_path}")
        return str(file_path)

