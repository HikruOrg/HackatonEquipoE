"""PDF text extraction."""
from pathlib import Path
from typing import Optional
import logging

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract text from PDF files."""
    
    def __init__(self, require_pdfplumber: bool = True):
        """
        Initialize PDF extractor.
        
        Args:
            require_pdfplumber: Whether to require pdfplumber (False if only using TXT extraction)
        """
        self._pdfplumber_available = pdfplumber is not None
        if require_pdfplumber and not self._pdfplumber_available:
            raise ImportError(
                "pdfplumber is required for PDF extraction. "
                "Install it with: pip install pdfplumber"
            )
    
    def extract_text(self, pdf_path: str | Path) -> str:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        if not self._pdfplumber_available:
            raise ImportError(
                "pdfplumber is required for PDF extraction. "
                "Install it with: pip install pdfplumber"
            )
        
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting text from PDF: {pdf_path.name}")
        
        text_parts = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                logger.info(f"PDF has {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                    else:
                        logger.warning(f"No text found on page {page_num} of {pdf_path.name}")
                
                full_text = "\n\n".join(text_parts)
                
                if not full_text.strip():
                    logger.warning(f"No text extracted from PDF: {pdf_path.name}")
                    raise ValueError(f"No text could be extracted from PDF: {pdf_path.name}")
                
                logger.info(f"Extracted {len(full_text)} characters from {pdf_path.name}")
                return full_text
                
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path.name}: {str(e)}")
            raise
    
    def extract_text_with_metadata(self, pdf_path: str | Path) -> dict:
        """
        Extract text and metadata from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with 'text' and 'metadata' keys
        """
        if not self._pdfplumber_available:
            raise ImportError(
                "pdfplumber is required for PDF extraction. "
                "Install it with: pip install pdfplumber"
            )
        
        pdf_path = Path(pdf_path)
        
        text = self.extract_text(pdf_path)
        
        metadata = {
            "file_name": pdf_path.name,
            "file_size": pdf_path.stat().st_size,
            "num_pages": 0,
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                metadata["num_pages"] = len(pdf.pages)
        except Exception as e:
            logger.warning(f"Could not extract metadata: {str(e)}")
        
        return {
            "text": text,
            "metadata": metadata,
            "file_type": "pdf",
        }
    
    def extract_text_from_txt(self, txt_path: str | Path) -> str:
        """
        Extract text from TXT file.
        
        Args:
            txt_path: Path to TXT file
            
        Returns:
            Extracted text as string
        """
        txt_path = Path(txt_path)
        
        if not txt_path.exists():
            raise FileNotFoundError(f"TXT file not found: {txt_path}")
        
        logger.info(f"Extracting text from TXT: {txt_path.name}")
        
        try:
            # Try UTF-8 encoding first
            try:
                with open(txt_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                # Fallback to latin-1 encoding
                logger.warning(f"UTF-8 decoding failed for {txt_path.name}, trying latin-1")
                with open(txt_path, "r", encoding="latin-1") as f:
                    text = f.read()
            
            if not text.strip():
                logger.warning(f"No text found in TXT file: {txt_path.name}")
                raise ValueError(f"TXT file is empty: {txt_path.name}")
            
            logger.info(f"Extracted {len(text)} characters from {txt_path.name}")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from TXT {txt_path.name}: {str(e)}")
            raise
    
    def extract_text_from_txt_with_metadata(self, txt_path: str | Path) -> dict:
        """
        Extract text and metadata from TXT file.
        
        Args:
            txt_path: Path to TXT file
            
        Returns:
            Dictionary with 'text' and 'metadata' keys
        """
        txt_path = Path(txt_path)
        
        text = self.extract_text_from_txt(txt_path)
        
        metadata = {
            "file_name": txt_path.name,
            "file_size": txt_path.stat().st_size,
            "num_pages": 1,  # TXT files are single "page"
        }
        
        return {
            "text": text,
            "metadata": metadata,
            "file_type": "txt",
        }


