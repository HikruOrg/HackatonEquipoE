"""Auto-processor for raw files on startup."""
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import hashlib

from src.config import config
from src.pdf_processing import PDFExtractor, PDFValidator
from src.preprocessing import ResumeParser, JDParser
from src.storage import LocalStorage

logger = logging.getLogger(__name__)


class AutoProcessor:
    """Automatically process raw files on startup."""
    
    def __init__(self):
        """Initialize auto processor."""
        self.pdf_extractor = PDFExtractor(require_pdfplumber=False)
        self.pdf_validator = PDFValidator()
        self.resume_parser = ResumeParser()
        self.jd_parser = JDParser()
        self.storage = LocalStorage()
        
        # Track processed files
        self.processed_tracking_file = Path(config.cache_path) / "processed_files.json"
        self.processed_files = self._load_processed_files()
    
    def _load_processed_files(self) -> Dict[str, str]:
        """Load tracking of previously processed files."""
        if self.processed_tracking_file.exists():
            try:
                with open(self.processed_tracking_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load processed files tracking: {e}")
        return {}
    
    def _save_processed_files(self):
        """Save tracking of processed files."""
        try:
            self.processed_tracking_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.processed_tracking_file, "w", encoding="utf-8") as f:
                json.dump(self.processed_files, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save processed files tracking: {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get hash of file content for change detection."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Could not hash file {file_path}: {e}")
            return ""
    
    def _is_file_processed(self, file_path: Path) -> bool:
        """Check if file has been processed and hasn't changed."""
        file_key = str(file_path.absolute())
        
        if file_key not in self.processed_files:
            return False
        
        # Check if file hash matches (detects changes)
        current_hash = self._get_file_hash(file_path)
        return self.processed_files.get(file_key) == current_hash
    
    def _mark_file_processed(self, file_path: Path):
        """Mark file as processed."""
        file_key = str(file_path.absolute())
        file_hash = self._get_file_hash(file_path)
        self.processed_files[file_key] = file_hash
    
    def _get_raw_files(self, directory: Path, extensions: List[str]) -> List[Path]:
        """Get all raw files with specified extensions from directory."""
        files = []
        for ext in extensions:
            files.extend(directory.glob(f"*{ext}"))
        return sorted(files)
    
    def _process_resume_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        Process a single resume file.
        
        Returns:
            Tuple of (success, error_message)
        """
        try:
            logger.info(f"Processing resume: {file_path.name}")
            
            # Validate file
            if self.pdf_validator.is_pdf(file_path):
                is_valid, error = self.pdf_validator.validate_pdf(file_path)
                if not is_valid:
                    return False, error
                # Extract text from PDF
                text_data = self.pdf_extractor.extract_text_with_metadata(file_path)
                text = text_data["text"]
                
            elif self.pdf_validator.is_json(file_path):
                is_valid, error = self.pdf_validator.validate_json(file_path)
                if not is_valid:
                    return False, error
                # Parse JSON directly
                resume_data = self.resume_parser.parse_from_json(file_path)
                self.storage.save_resume(resume_data)
                return True, ""
                
            elif self.pdf_validator.is_txt(file_path):
                is_valid, error = self.pdf_validator.validate_txt(file_path)
                if not is_valid:
                    return False, error
                # Extract text from TXT
                text_data = self.pdf_extractor.extract_text_from_txt_with_metadata(file_path)
                text = text_data["text"]
                
            else:
                return False, f"Unsupported file type: {file_path.suffix}"
            
            # Parse text to structured JSON (for PDF and TXT)
            resume_data = self.resume_parser.parse_from_text(text)
            
            # Save to storage
            self.storage.save_resume(resume_data)
            
            logger.info(f"✓ Successfully processed resume: {file_path.name}")
            return True, ""
            
        except Exception as e:
            error_msg = f"Error processing resume {file_path.name}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _process_jd_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        Process a single job description file.
        
        Returns:
            Tuple of (success, error_message)
        """
        try:
            logger.info(f"Processing job description: {file_path.name}")
            
            # Validate file
            if self.pdf_validator.is_pdf(file_path):
                is_valid, error = self.pdf_validator.validate_pdf(file_path)
                if not is_valid:
                    return False, error
                # Extract text from PDF
                text_data = self.pdf_extractor.extract_text_with_metadata(file_path)
                text = text_data["text"]
                
            elif self.pdf_validator.is_json(file_path):
                is_valid, error = self.pdf_validator.validate_json(file_path)
                if not is_valid:
                    return False, error
                # Parse JSON directly
                jd_data = self.jd_parser.parse_from_json(file_path)
                self.storage.save_jd(jd_data)
                return True, ""
                
            elif self.pdf_validator.is_txt(file_path):
                is_valid, error = self.pdf_validator.validate_txt(file_path)
                if not is_valid:
                    return False, error
                # Extract text from TXT
                text_data = self.pdf_extractor.extract_text_from_txt_with_metadata(file_path)
                text = text_data["text"]
                
            else:
                return False, f"Unsupported file type: {file_path.suffix}"
            
            # Parse text to structured JSON (for PDF and TXT)
            jd_data = self.jd_parser.parse_from_text(text)
            
            # Save to storage
            self.storage.save_jd(jd_data)
            
            logger.info(f"✓ Successfully processed JD: {file_path.name}")
            return True, ""
            
        except Exception as e:
            error_msg = f"Error processing JD {file_path.name}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def process_resumes(self) -> Dict[str, int]:
        """
        Process all unprocessed resumes from raw directory.
        
        Returns:
            Dictionary with processing statistics
        """
        logger.info("=" * 60)
        logger.info("Auto-processing resumes from raw directory...")
        logger.info("=" * 60)
        
        # Get all raw resume files
        resume_files = self._get_raw_files(
            config.resumes_raw_dir,
            [".pdf", ".json", ".txt"]
        )
        
        stats = {
            "total": len(resume_files),
            "processed": 0,
            "skipped": 0,
            "failed": 0,
        }
        
        for file_path in resume_files:
            # Skip if already processed
            if self._is_file_processed(file_path):
                logger.info(f"⊙ Skipping (already processed): {file_path.name}")
                stats["skipped"] += 1
                continue
            
            # Process file
            success, error = self._process_resume_file(file_path)
            
            if success:
                self._mark_file_processed(file_path)
                stats["processed"] += 1
            else:
                logger.error(f"✗ Failed: {file_path.name} - {error}")
                stats["failed"] += 1
        
        # Save tracking
        self._save_processed_files()
        
        logger.info("=" * 60)
        logger.info(f"Resume processing complete:")
        logger.info(f"  Total files: {stats['total']}")
        logger.info(f"  Processed: {stats['processed']}")
        logger.info(f"  Skipped: {stats['skipped']}")
        logger.info(f"  Failed: {stats['failed']}")
        logger.info("=" * 60)
        
        return stats
    
    def process_job_descriptions(self) -> Dict[str, int]:
        """
        Process all unprocessed job descriptions from raw directory.
        
        Returns:
            Dictionary with processing statistics
        """
        logger.info("=" * 60)
        logger.info("Auto-processing job descriptions from raw directory...")
        logger.info("=" * 60)
        
        # Get all raw JD files
        jd_files = self._get_raw_files(
            config.jd_raw_dir,
            [".pdf", ".json", ".txt"]
        )
        
        stats = {
            "total": len(jd_files),
            "processed": 0,
            "skipped": 0,
            "failed": 0,
        }
        
        for file_path in jd_files:
            # Skip if already processed
            if self._is_file_processed(file_path):
                logger.info(f"⊙ Skipping (already processed): {file_path.name}")
                stats["skipped"] += 1
                continue
            
            # Process file
            success, error = self._process_jd_file(file_path)
            
            if success:
                self._mark_file_processed(file_path)
                stats["processed"] += 1
            else:
                logger.error(f"✗ Failed: {file_path.name} - {error}")
                stats["failed"] += 1
        
        # Save tracking
        self._save_processed_files()
        
        logger.info("=" * 60)
        logger.info(f"Job description processing complete:")
        logger.info(f"  Total files: {stats['total']}")
        logger.info(f"  Processed: {stats['processed']}")
        logger.info(f"  Skipped: {stats['skipped']}")
        logger.info(f"  Failed: {stats['failed']}")
        logger.info("=" * 60)
        
        return stats
    
    def process_all(self) -> Dict[str, Dict[str, int]]:
        """
        Process all unprocessed files (resumes and job descriptions).
        
        Returns:
            Dictionary with statistics for both resumes and JDs
        """
        logger.info("\n")
        logger.info("╔" + "=" * 58 + "╗")
        logger.info("║" + " " * 10 + "AUTO-PROCESSING RAW FILES ON STARTUP" + " " * 11 + "║")
        logger.info("╚" + "=" * 58 + "╝")
        logger.info("\n")
        
        results = {
            "resumes": self.process_resumes(),
            "job_descriptions": self.process_job_descriptions(),
        }
        
        total_processed = results["resumes"]["processed"] + results["job_descriptions"]["processed"]
        total_skipped = results["resumes"]["skipped"] + results["job_descriptions"]["skipped"]
        total_failed = results["resumes"]["failed"] + results["job_descriptions"]["failed"]
        
        logger.info("\n")
        logger.info("╔" + "=" * 58 + "╗")
        logger.info("║" + " " * 18 + "OVERALL SUMMARY" + " " * 25 + "║")
        logger.info("╠" + "=" * 58 + "╣")
        logger.info(f"║  Total processed: {total_processed:3d}" + " " * 38 + "║")
        logger.info(f"║  Total skipped:   {total_skipped:3d}" + " " * 38 + "║")
        logger.info(f"║  Total failed:    {total_failed:3d}" + " " * 38 + "║")
        logger.info("╚" + "=" * 58 + "╝")
        logger.info("\n")
        
        return results
