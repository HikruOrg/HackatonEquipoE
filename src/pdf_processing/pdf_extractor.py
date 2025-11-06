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
    
    def __init__(self):
        """Initialize PDF extractor."""
        if pdfplumber is None:
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
        }

