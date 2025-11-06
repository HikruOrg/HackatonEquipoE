"""Storage client abstraction."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pathlib import Path


class StorageClient(ABC):
    """Abstract base class for storage clients."""
    
    @abstractmethod
    def save_resume(self, resume_data: Dict, filename: Optional[str] = None) -> str:
        """Save resume JSON to storage."""
        pass
    
    @abstractmethod
    def save_jd(self, jd_data: Dict, filename: Optional[str] = None) -> str:
        """Save job description JSON to storage."""
        pass
    
    @abstractmethod
    def get_resume(self, file_id: str) -> Dict:
        """Retrieve resume JSON from storage."""
        pass
    
    @abstractmethod
    def get_jd(self, file_id: str) -> Dict:
        """Retrieve job description JSON from storage."""
        pass
    
    @abstractmethod
    def list_resumes(self) -> List[Dict]:
        """List all stored resumes."""
        pass
    
    @abstractmethod
    def list_jds(self) -> List[Dict]:
        """List all stored job descriptions."""
        pass
    
    @abstractmethod
    def search(self, query: str, file_type: Optional[str] = None) -> List[Dict]:
        """Search stored files."""
        pass
    
    @abstractmethod
    def delete(self, file_id: str, file_type: str) -> bool:
        """Delete file from storage."""
        pass

