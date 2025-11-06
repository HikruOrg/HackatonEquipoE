"""FastAPI REST API for AI Talent Matcher."""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Optional, Dict
import json
import logging
from pathlib import Path
import tempfile
import shutil

from src.config import config
from src.pdf_processing import PDFExtractor, PDFValidator
from src.preprocessing import ResumeParser, JDParser
from src.llm import LLMClient, LLMAnalyzer
from src.prompts import PromptLoader
from src.scoring import HybridScorer
from src.storage import LocalStorage
from src.export import CSVExporter
from src.explainability import ReasonCodes, HitMapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI Talent Matcher API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
# Validate configuration (warning only, will fail when LLM is actually used)
try:
    config.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.warning(f"Configuration warning: {e}. Server will start but LLM features may not work until API keys are configured.")

# Initialize LLM client (may fail if API keys are missing, but server will still start)
try:
    llm_client = LLMClient(config)
except Exception as e:
    logger.warning(f"LLM client initialization failed: {e}. LLM features will not be available.")
    llm_client = None

prompt_loader = PromptLoader()
llm_analyzer = LLMAnalyzer(llm_client, prompt_loader) if llm_client else None
hybrid_scorer = HybridScorer()
storage = LocalStorage()
csv_exporter = CSVExporter()
pdf_extractor = PDFExtractor()
pdf_validator = PDFValidator()
resume_parser = ResumeParser()
jd_parser = JDParser()

# Processing state
processing_state = {
    "status": "idle",
    "progress": 0,
    "total": 0,
    "results": [],
    "errors": [],
}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Talent Matcher API", "version": "1.0.0"}


@app.post("/api/upload/resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """Upload resume files (PDF or JSON)."""
    uploaded_files = []
    errors = []
    
    for file in files:
        try:
            # Save uploaded file temporarily
            suffix = Path(file.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                shutil.copyfileobj(file.file, tmp_file)
                tmp_path = tmp_file.name
            
            # Validate file
            if pdf_validator.is_pdf(tmp_path):
                is_valid, error = pdf_validator.validate_pdf(tmp_path)
                if not is_valid:
                    errors.append(f"{file.filename}: {error}")
                    continue
            elif pdf_validator.is_json(tmp_path):
                is_valid, error = pdf_validator.validate_json(tmp_path)
                if not is_valid:
                    errors.append(f"{file.filename}: {error}")
                    continue
            else:
                errors.append(f"{file.filename}: Unsupported file type")
                continue
            
            uploaded_files.append({
                "filename": file.filename,
                "path": tmp_path,
                "type": "pdf" if pdf_validator.is_pdf(tmp_path) else "json",
            })
            
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
    
    return {
        "uploaded": len(uploaded_files),
        "files": uploaded_files,
        "errors": errors,
    }


@app.post("/api/upload/job-description")
async def upload_job_description(file: UploadFile = File(...)):
    """Upload job description file (PDF or JSON)."""
    try:
        # Save uploaded file temporarily
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Validate file
        if pdf_validator.is_pdf(tmp_path):
            is_valid, error = pdf_validator.validate_pdf(tmp_path)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
        elif pdf_validator.is_json(tmp_path):
            is_valid, error = pdf_validator.validate_json(tmp_path)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        return {
            "filename": file.filename,
            "path": tmp_path,
            "type": "pdf" if pdf_validator.is_pdf(tmp_path) else "json",
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/process")
async def start_processing(
    resume_files: List[str],
    jd_file: str,
    background_tasks: BackgroundTasks,
):
    """Start processing pipeline."""
    global processing_state
    
    if processing_state["status"] == "processing":
        raise HTTPException(status_code=400, detail="Processing already in progress")
    
    processing_state = {
        "status": "processing",
        "progress": 0,
        "total": len(resume_files),
        "results": [],
        "errors": [],
    }
    
    # Start background processing
    background_tasks.add_task(process_pipeline, resume_files, jd_file)
    
    return {"status": "started", "message": "Processing started"}


def process_pipeline(resume_files: List[str], jd_file: str):
    """Process resumes against job description."""
    global processing_state
    
    try:
        # Process job description
        logger.info("Processing job description...")
        jd_data = process_jd_file(jd_file)
        
        # Process resumes
        results = []
        for i, resume_file in enumerate(resume_files):
            try:
                logger.info(f"Processing resume {i+1}/{len(resume_files)}: {resume_file}")
                
                # Process resume
                resume_data = process_resume_file(resume_file)
                
                # Analyze with LLM
                if llm_analyzer is None:
                    raise ValueError("LLM analyzer is not available. Please configure API keys in .env file.")
                llm_analysis = llm_analyzer.analyze_candidate(resume_data, jd_data)
                
                # Calculate hybrid score
                score_result = hybrid_scorer.calculate_final_score(
                    llm_analysis.get("similarity_score", 0.0),
                    resume_data,
                    jd_data,
                    llm_analysis,
                )
                
                # Generate reason codes
                reason_codes = ReasonCodes.generate_reason_codes_from_analysis(
                    llm_analysis, resume_data, jd_data
                )
                
                # Map hits to sections
                hit_mappings = HitMapper.map_hits_to_sections(
                    llm_analysis, resume_data, jd_data
                )
                
                # Combine results
                result = {
                    "candidate_id": resume_data.get("candidate_id"),
                    "name": resume_data.get("name", "Unknown"),
                    "final_score": score_result["final_score"],
                    "similarity_score": score_result["similarity_score"],
                    "must_have_matches": llm_analysis.get("must_have_matches", []),
                    "recency_boost": score_result["recency_boost"],
                    "reason_codes": reason_codes,
                    "hit_mappings": hit_mappings,
                }
                
                results.append(result)
                
                # Update progress
                processing_state["progress"] = i + 1
                
            except Exception as e:
                logger.error(f"Error processing resume {resume_file}: {str(e)}")
                processing_state["errors"].append(f"{resume_file}: {str(e)}")
        
        # Rank results
        results.sort(key=lambda x: x["final_score"], reverse=True)
        for i, result in enumerate(results, 1):
            result["rank"] = i
        
        processing_state["results"] = results
        processing_state["status"] = "completed"
        
    except Exception as e:
        logger.error(f"Error in processing pipeline: {str(e)}")
        processing_state["status"] = "error"
        processing_state["errors"].append(str(e))


def process_resume_file(file_path: str) -> Dict:
    """Process a resume file (PDF or JSON)."""
    path = Path(file_path)
    
    if pdf_validator.is_pdf(path):
        # Extract text from PDF
        text_data = pdf_extractor.extract_text_with_metadata(path)
        text = text_data["text"]
        
        # Parse to structured JSON
        resume_data = resume_parser.parse_from_text(text)
        
        # Save to storage
        storage.save_resume(resume_data)
        
        return resume_data
    
    elif pdf_validator.is_json(path):
        # Parse JSON directly
        resume_data = resume_parser.parse_from_json(path)
        
        # Save to storage
        storage.save_resume(resume_data)
        
        return resume_data
    
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")


def process_jd_file(file_path: str) -> Dict:
    """Process a job description file (PDF or JSON)."""
    path = Path(file_path)
    
    if pdf_validator.is_pdf(path):
        # Extract text from PDF
        text_data = pdf_extractor.extract_text_with_metadata(path)
        text = text_data["text"]
        
        # Parse to structured JSON
        jd_data = jd_parser.parse_from_text(text)
        
        # Save to storage
        storage.save_jd(jd_data)
        
        return jd_data
    
    elif pdf_validator.is_json(path):
        # Parse JSON directly
        jd_data = jd_parser.parse_from_json(path)
        
        # Save to storage
        storage.save_jd(jd_data)
        
        return jd_data
    
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")


@app.get("/api/process/status")
async def get_processing_status():
    """Get processing status."""
    return processing_state


@app.get("/api/results")
async def get_results():
    """Get ranked results."""
    if processing_state["status"] != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed")
    
    return {
        "results": processing_state["results"],
        "total": len(processing_state["results"]),
    }


@app.get("/api/results/{candidate_id}")
async def get_candidate_details(candidate_id: str):
    """Get detailed candidate information."""
    if processing_state["status"] != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed")
    
    # Find candidate in results
    for result in processing_state["results"]:
        if result.get("candidate_id") == candidate_id:
            # Get full resume from storage
            try:
                resume = storage.get_resume(candidate_id)
                result["full_resume"] = resume
            except FileNotFoundError:
                pass
            
            return result
    
    raise HTTPException(status_code=404, detail="Candidate not found")


@app.get("/api/storage/resumes")
async def list_resumes():
    """List all stored resumes."""
    return storage.list_resumes()


@app.get("/api/storage/job-descriptions")
async def list_job_descriptions():
    """List all stored job descriptions."""
    return storage.list_jds()


@app.get("/api/storage/search")
async def search_storage(query: str, file_type: Optional[str] = None):
    """Search stored files."""
    return storage.search(query, file_type)


@app.delete("/api/storage/{file_id}")
async def delete_file(file_id: str, file_type: str):
    """Delete file from storage."""
    success = storage.delete(file_id, file_type)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "File deleted successfully"}


@app.get("/api/export/csv")
async def export_csv():
    """Export results to CSV."""
    if processing_state["status"] != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed")
    
    csv_path = csv_exporter.export_results(processing_state["results"])
    
    return FileResponse(
        csv_path,
        media_type="text/csv",
        filename=Path(csv_path).name,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

