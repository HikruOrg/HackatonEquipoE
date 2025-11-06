"""PDF file validation."""
from pathlib import Path
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class PDFValidator:
    """Validate PDF files before processing."""
    
    @staticmethod
    def is_pdf(file_path: str | Path) -> bool:
        """Check if file is a PDF."""
        path = Path(file_path)
        return path.suffix.lower() == ".pdf" and path.exists()
    
    @staticmethod
    def is_json(file_path: str | Path) -> bool:
        """Check if file is a JSON."""
        path = Path(file_path)
        return path.suffix.lower() == ".json" and path.exists()
    
    @staticmethod
    def is_txt(file_path: str | Path) -> bool:
        """Check if file is a TXT."""
        path = Path(file_path)
        return path.suffix.lower() == ".txt" and path.exists()
    
    @staticmethod
    def validate_pdf(file_path: str | Path) -> Tuple[bool, str]:
        """
        Validate PDF file.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(file_path)
        
        if not path.exists():
            return False, f"File does not exist: {file_path}"
        
        if not path.suffix.lower() == ".pdf":
            return False, f"File is not a PDF: {file_path}"
        
        # Check file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB
        if path.stat().st_size > max_size:
            return False, f"PDF file too large (max 50MB): {file_path}"
        
        # Try to read first bytes to check if it's a valid PDF
        try:
            with open(path, "rb") as f:
                header = f.read(4)
                if header != b"%PDF":
                    return False, f"Invalid PDF header: {file_path}"
        except Exception as e:
            return False, f"Error reading PDF file: {str(e)}"
        
        return True, ""
    
    @staticmethod
    def validate_json(file_path: str | Path) -> Tuple[bool, str]:
        """
        Validate JSON file.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        import json
        
        path = Path(file_path)
        
        if not path.exists():
            return False, f"File does not exist: {file_path}"
        
        if not path.suffix.lower() == ".json":
            return False, f"File is not a JSON: {file_path}"
        
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if path.stat().st_size > max_size:
            return False, f"JSON file too large (max 10MB): {file_path}"
        
        # Try to parse JSON
        try:
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON format: {str(e)}"
        except Exception as e:
            return False, f"Error reading JSON file: {str(e)}"
        
        return True, ""
    
    @staticmethod
    def validate_txt(file_path: str | Path) -> Tuple[bool, str]:
        """
        Validate TXT file.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(file_path)
        
        if not path.exists():
            return False, f"File does not exist: {file_path}"
        
        if not path.suffix.lower() == ".txt":
            return False, f"File is not a TXT: {file_path}"
        
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if path.stat().st_size > max_size:
            return False, f"TXT file too large (max 10MB): {file_path}"
        
        # Try to read the file to ensure it's readable
        try:
            with open(path, "r", encoding="utf-8") as f:
                f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(path, "r", encoding="latin-1") as f:
                    f.read()
            except Exception as e:
                return False, f"Error reading TXT file: {str(e)}"
        except Exception as e:
            return False, f"Error reading TXT file: {str(e)}"
        
        return True, ""
    
    @staticmethod
    def validate_files(file_paths: List[str | Path]) -> Tuple[List[Path], List[str]]:
        """
        Validate multiple files.
        
        Returns:
            Tuple of (valid_files, error_messages)
        """
        valid_files = []
        errors = []
        
        for file_path in file_paths:
            path = Path(file_path)
            
            if PDFValidator.is_pdf(path):
                is_valid, error = PDFValidator.validate_pdf(path)
                if is_valid:
                    valid_files.append(path)
                else:
                    errors.append(f"{path.name}: {error}")
            elif PDFValidator.is_json(path):
                is_valid, error = PDFValidator.validate_json(path)
                if is_valid:
                    valid_files.append(path)
                else:
                    errors.append(f"{path.name}: {error}")
            elif PDFValidator.is_txt(path):
                is_valid, error = PDFValidator.validate_txt(path)
                if is_valid:
                    valid_files.append(path)
                else:
                    errors.append(f"{path.name}: {error}")
            else:
                errors.append(f"{path.name}: Unsupported file type")
        
        return valid_files, errors

