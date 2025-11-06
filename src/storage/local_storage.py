"""Local filesystem storage implementation."""
import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

from .storage_client import StorageClient
from src.config import config

logger = logging.getLogger(__name__)


class LocalStorage(StorageClient):
    """Local filesystem storage implementation."""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize local storage.
        
        Args:
            base_path: Base path for storage (defaults to config.storage_path)
        """
        self.base_path = Path(base_path or config.storage_path)
        self.resumes_dir = self.base_path / "resumes"
        self.jds_dir = self.base_path / "job_descriptions"
        
        # Create directories
        self.resumes_dir.mkdir(parents=True, exist_ok=True)
        self.jds_dir.mkdir(parents=True, exist_ok=True)
    
    def save_resume(self, resume_data: Dict, filename: Optional[str] = None) -> str:
        """Save resume JSON to storage."""
        if not filename:
            candidate_id = resume_data.get("candidate_id", str(uuid.uuid4()))
            filename = f"resume_{candidate_id}.json"
        
        file_path = self.resumes_dir / filename
        
        # Ensure candidate_id exists
        if "candidate_id" not in resume_data:
            resume_data["candidate_id"] = str(uuid.uuid4())
        
        # Add metadata
        resume_data["_metadata"] = {
            "saved_at": datetime.now().isoformat(),
            "filename": filename,
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(resume_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved resume to {file_path}")
        return str(file_path)
    
    def save_jd(self, jd_data: Dict, filename: Optional[str] = None) -> str:
        """Save job description JSON to storage."""
        if not filename:
            jd_id = jd_data.get("jd_id", str(uuid.uuid4()))
            filename = f"jd_{jd_id}.json"
        
        file_path = self.jds_dir / filename
        
        # Ensure jd_id exists
        if "jd_id" not in jd_data:
            jd_data["jd_id"] = str(uuid.uuid4())
        
        # Add metadata
        jd_data["_metadata"] = {
            "saved_at": datetime.now().isoformat(),
            "filename": filename,
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(jd_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved JD to {file_path}")
        return str(file_path)
    
    def get_resume(self, file_id: str) -> Dict:
        """Retrieve resume JSON from storage."""
        # file_id can be filename or candidate_id
        file_path = self.resumes_dir / file_id
        if not file_path.exists():
            # Try to find by candidate_id
            for json_file in self.resumes_dir.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data.get("candidate_id") == file_id:
                            return data
                except Exception:
                    continue
        
        if not file_path.exists():
            raise FileNotFoundError(f"Resume not found: {file_id}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get_jd(self, file_id: str) -> Dict:
        """Retrieve job description JSON from storage."""
        file_path = self.jds_dir / file_id
        if not file_path.exists():
            # Try to find by jd_id
            for json_file in self.jds_dir.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data.get("jd_id") == file_id:
                            return data
                except Exception:
                    continue
        
        if not file_path.exists():
            raise FileNotFoundError(f"Job description not found: {file_id}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def list_resumes(self) -> List[Dict]:
        """List all stored resumes."""
        resumes = []
        
        for json_file in self.resumes_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    resumes.append({
                        "file_id": json_file.name,
                        "candidate_id": data.get("candidate_id"),
                        "name": data.get("name", "Unknown"),
                        "saved_at": data.get("_metadata", {}).get("saved_at"),
                    })
            except Exception as e:
                logger.warning(f"Error reading resume {json_file}: {e}")
        
        return sorted(resumes, key=lambda x: x.get("saved_at", ""), reverse=True)
    
    def list_jds(self) -> List[Dict]:
        """List all stored job descriptions."""
        jds = []
        
        for json_file in self.jds_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    jds.append({
                        "file_id": json_file.name,
                        "jd_id": data.get("jd_id"),
                        "title": data.get("title", "Unknown"),
                        "saved_at": data.get("_metadata", {}).get("saved_at"),
                    })
            except Exception as e:
                logger.warning(f"Error reading JD {json_file}: {e}")
        
        return sorted(jds, key=lambda x: x.get("saved_at", ""), reverse=True)
    
    def search(self, query: str, file_type: Optional[str] = None) -> List[Dict]:
        """Search stored files."""
        results = []
        query_lower = query.lower()
        
        if file_type in [None, "resume"]:
            for json_file in self.resumes_dir.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        searchable_text = f"{data.get('name', '')} {data.get('raw_text', '')}".lower()
                        if query_lower in searchable_text:
                            results.append({
                                "file_id": json_file.name,
                                "type": "resume",
                                "candidate_id": data.get("candidate_id"),
                                "name": data.get("name", "Unknown"),
                            })
                except Exception:
                    continue
        
        if file_type in [None, "jd"]:
            for json_file in self.jds_dir.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        searchable_text = f"{data.get('title', '')} {data.get('description', '')}".lower()
                        if query_lower in searchable_text:
                            results.append({
                                "file_id": json_file.name,
                                "type": "jd",
                                "jd_id": data.get("jd_id"),
                                "title": data.get("title", "Unknown"),
                            })
                except Exception:
                    continue
        
        return results
    
    def delete(self, file_id: str, file_type: str) -> bool:
        """Delete file from storage."""
        if file_type == "resume":
            file_path = self.resumes_dir / file_id
        elif file_type == "jd":
            file_path = self.jds_dir / file_id
        else:
            raise ValueError(f"Invalid file_type: {file_type}")
        
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted {file_type}: {file_id}")
            return True
        
        return False

