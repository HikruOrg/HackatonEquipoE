"""FastAPI REST API for AI Talent Matcher."""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import logging
import os
from pathlib import Path
import tempfile
import shutil
from datetime import datetime

from src.config import config
from src.pdf_processing import PDFExtractor, PDFValidator
from src.preprocessing import ResumeParser, JDParser
from src.llm import LLMClient, LLMAnalyzer
from src.prompts import PromptLoader
from src.scoring import HybridScorer
from src.storage import LocalStorage
from src.export import CSVExporter
from src.explainability import ReasonCodes, HitMapper
from src.startup import AutoProcessor

# Pydantic models for request bodies
class ProcessRequest(BaseModel):
    """Request model for processing endpoint."""
    resume_files: List[str]
    jd_file: str

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
pdf_extractor = PDFExtractor(require_pdfplumber=False)  # Allow TXT extraction without pdfplumber
pdf_validator = PDFValidator()
resume_parser = ResumeParser(use_llm=True, llm_client=llm_client) if llm_client else ResumeParser()
jd_parser = JDParser(use_llm=True, llm_client=llm_client) if llm_client else JDParser()

# Processing state
processing_state = {
    "status": "idle",
    "progress": 0,
    "total": 0,
    "results": [],
    "errors": [],
}


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting AI Talent Matcher API...")
    
    # Auto-process raw files
    try:
        auto_processor = AutoProcessor(llm_client=llm_client)
        auto_processor.process_all()
    except Exception as e:
        logger.error(f"Error during auto-processing: {e}")
        # Don't fail startup if auto-processing fails
        logger.warning("Continuing startup despite auto-processing error...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Talent Matcher API", "version": "1.0.0"}


@app.post("/api/upload/resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """Upload resume files (PDF, JSON, or TXT) and save to storage."""
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
            file_type = None
            if pdf_validator.is_pdf(tmp_path):
                is_valid, error = pdf_validator.validate_pdf(tmp_path)
                if not is_valid:
                    errors.append(f"{file.filename}: {error}")
                    continue
                file_type = "pdf"
            elif pdf_validator.is_json(tmp_path):
                is_valid, error = pdf_validator.validate_json(tmp_path)
                if not is_valid:
                    errors.append(f"{file.filename}: {error}")
                    continue
                file_type = "json"
            elif pdf_validator.is_txt(tmp_path):
                is_valid, error = pdf_validator.validate_txt(tmp_path)
                if not is_valid:
                    errors.append(f"{file.filename}: {error}")
                    continue
                file_type = "txt"
            else:
                errors.append(f"{file.filename}: Unsupported file type")
                continue
            
            # Process and save to storage immediately
            logger.info(f"Processing uploaded resume file: {file.filename} ({file_type})")
            
            # Extract text from file
            text_content = None
            if file_type == "pdf":
                try:
                    text_content = pdf_extractor.extract_text(tmp_path)
                except Exception as pdf_error:
                    logger.error(f"Failed to extract PDF text: {pdf_error}")
                    # Fallback: try reading as text file
                    logger.info("Attempting to read PDF as text file...")
                    try:
                        with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                            text_content = f.read()
                    except Exception as txt_error:
                        logger.error(f"Failed to read as text: {txt_error}")
                        errors.append(f"{file.filename}: Could not extract text from PDF")
                        continue
            elif file_type == "json":
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    # If it's already structured, save it directly
                    storage.save_resume(json_data)
                    resume_id = json_data.get("candidate_id", "unknown")
                    logger.info(f"Saved JSON resume to storage with ID: {resume_id}")
                    uploaded_files.append({
                        "filename": file.filename,
                        "resume_id": resume_id,
                        "type": file_type,
                        "status": "saved"
                    })
                    # Clean up temp file
                    try:
                        os.unlink(tmp_path)
                    except Exception as e:
                        logger.warning(f"Failed to delete temp file {tmp_path}: {e}")
                    continue
            else:  # txt
                logger.info(f"Reading TXT file: {tmp_path}")
                with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text_content = f.read()
                logger.info(f"Read {len(text_content)} characters from TXT file")
            
            # Parse the text content to structured JSON
            logger.info(f"Parsing resume text content ({len(text_content) if text_content else 0} chars)...")
            parsed_resume = resume_parser.parse_from_text(text_content)
            logger.info(f"Successfully parsed resume")
            
            # Save to storage
            storage.save_resume(parsed_resume)
            resume_id = parsed_resume.get("candidate_id", "unknown")
            logger.info(f"Saved parsed resume to storage with ID: {resume_id}")
            
            uploaded_files.append({
                "filename": file.filename,
                "resume_id": resume_id,
                "type": file_type,
                "status": "saved"
            })
            
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {tmp_path}: {e}")
            
        except Exception as e:
            logger.error(f"Error uploading resume {file.filename}: {e}")
            errors.append(f"{file.filename}: {str(e)}")
    
    return {
        "uploaded": len(uploaded_files),
        "files": uploaded_files,
        "errors": errors,
    }


@app.post("/api/upload/job-description")
async def upload_job_description(file: UploadFile = File(...)):
    """Upload job description file (PDF, JSON, or TXT) and save to storage."""
    try:
        # Save uploaded file temporarily
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Validate file
        file_type = None
        if pdf_validator.is_pdf(tmp_path):
            is_valid, error = pdf_validator.validate_pdf(tmp_path)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            file_type = "pdf"
        elif pdf_validator.is_json(tmp_path):
            is_valid, error = pdf_validator.validate_json(tmp_path)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            file_type = "json"
        elif pdf_validator.is_txt(tmp_path):
            is_valid, error = pdf_validator.validate_txt(tmp_path)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            file_type = "txt"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Process and save to storage immediately
        logger.info(f"Processing uploaded JD file: {file.filename} ({file_type})")
        
        # Extract text from file
        text_content = None
        if file_type == "pdf":
            try:
                text_content = pdf_extractor.extract_text(tmp_path)
            except Exception as pdf_error:
                logger.error(f"Failed to extract PDF text: {pdf_error}")
                # Fallback: try reading as text file
                logger.info("Attempting to read PDF as text file...")
                try:
                    with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                        text_content = f.read()
                except Exception as txt_error:
                    logger.error(f"Failed to read as text: {txt_error}")
                    raise HTTPException(status_code=500, detail=f"Could not extract text from PDF: {str(pdf_error)}")
        elif file_type == "json":
            with open(tmp_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                # If it's already structured, save it directly
                storage.save_jd(json_data)
                jd_id = json_data.get("jd_id", "unknown")
                logger.info(f"Saved JSON JD to storage with ID: {jd_id}")
                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except Exception as e:
                    logger.warning(f"Failed to delete temp file {tmp_path}: {e}")
                return {
                    "filename": file.filename,
                    "jd_id": jd_id,
                    "type": file_type,
                    "status": "saved"
                }
        else:  # txt
            logger.info(f"Reading TXT file: {tmp_path}")
            with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                text_content = f.read()
            logger.info(f"Read {len(text_content)} characters from TXT file")
        
        # Parse the text content to structured JSON
        logger.info(f"Parsing JD text content ({len(text_content) if text_content else 0} chars)...")
        parsed_jd = jd_parser.parse_from_text(text_content)
        logger.info(f"Successfully parsed JD")
        
        # Save to storage
        storage.save_jd(parsed_jd)
        jd_id = parsed_jd.get("jd_id", "unknown")
        logger.info(f"Saved parsed JD to storage with ID: {jd_id}")
        
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except Exception as e:
            logger.warning(f"Failed to delete temp file {tmp_path}: {e}")
        
        return {
            "filename": file.filename,
            "jd_id": jd_id,
            "type": file_type,
            "status": "saved"
        }
        
    except Exception as e:
        logger.error(f"Error uploading job description: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/process")
async def start_processing(
    request: ProcessRequest,
    background_tasks: BackgroundTasks,
):
    """Start processing pipeline."""
    global processing_state
    
    if processing_state["status"] == "processing":
        raise HTTPException(status_code=400, detail="Processing already in progress")
    
    processing_state = {
        "status": "processing",
        "progress": 0,
        "total": len(request.resume_files),
        "results": [],
        "errors": [],
    }
    
    # Start background processing
    background_tasks.add_task(process_pipeline, request.resume_files, request.jd_file)
    
    return {"status": "started", "message": "Processing started"}


@app.post("/api/process/stored")
async def start_processing_stored(
    jd_id: str,
    background_tasks: BackgroundTasks,
):
    """Start processing pipeline using stored files."""
    global processing_state
    
    if processing_state["status"] == "processing":
        raise HTTPException(status_code=400, detail="Processing already in progress")
    
    # Load JD file
    jd_file_path = config.storage_jd_path / f"jd_{jd_id}.json"
    if not jd_file_path.exists():
        raise HTTPException(status_code=404, detail=f"Job description not found: {jd_id}")
    
    # Load all resume files
    resume_files = []
    for resume_file in config.storage_resume_path.glob("*.json"):
        resume_files.append(str(resume_file))
    
    if not resume_files:
        raise HTTPException(status_code=400, detail="No resumes found in storage")
    
    processing_state = {
        "status": "processing",
        "progress": 0,
        "total": len(resume_files),
        "results": [],
        "errors": [],
    }
    
    # Start background processing
    background_tasks.add_task(process_pipeline, resume_files, str(jd_file_path), jd_id, True)
    
    return {
        "status": "started",
        "message": "Processing started",
        "jd_id": jd_id,
        "total_resumes": len(resume_files)
    }


def process_pipeline(resume_files: List[str], jd_file: str, jd_id: str = None, skip_processing: bool = False):
    """Process resumes against job description.
    
    Args:
        resume_files: List of resume file paths
        jd_file: Path to job description file
        jd_id: Optional JD ID to use
        skip_processing: If True, load files directly instead of processing them
    """
    global processing_state
    
    try:
        # Process or load job description
        logger.info("Processing job description...")
        if skip_processing:
            # Load JD directly from storage (already processed)
            with open(jd_file, 'r', encoding='utf-8') as f:
                jd_data = json.load(f)
        else:
            jd_data = process_jd_file(jd_file)
        
        # Use provided jd_id if given, otherwise use from jd_data
        if jd_id:
            jd_data["jd_id"] = jd_id
        
        # Process resumes
        results = []
        for i, resume_file in enumerate(resume_files):
            try:
                logger.info(f"Processing resume {i+1}/{len(resume_files)}: {resume_file}")
                
                # Process or load resume
                if skip_processing:
                    # Load resume directly from storage (already processed)
                    with open(resume_file, 'r', encoding='utf-8') as f:
                        resume_data = json.load(f)
                else:
                    resume_data = process_resume_file(resume_file)
                
                # Analyze with LLM
                if llm_analyzer is None:
                    raise ValueError("LLM analyzer is not available. Please configure API keys in .env file.")
                
                try:
                    llm_analysis = llm_analyzer.analyze_candidate(resume_data, jd_data)
                except Exception as llm_error:
                    logger.error(f"LLM analysis failed for candidate {resume_data.get('candidate_id')}: {str(llm_error)}")
                    # Use default values if LLM fails
                    llm_analysis = {
                        "similarity_score": 0.0,
                        "must_have_matches": [],
                        "strengths": [],
                        "weaknesses": []
                    }
                
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
        
        # Save results to file for persistence
        try:
            results_file = config.output_path / "latest_results.json"
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump({
                    "jd_file": jd_file,
                    "jd_id": jd_data.get("jd_id"),
                    "timestamp": datetime.now().isoformat(),
                    "results": results,
                    "total_processed": len(results),
                    "total_failed": len(processing_state["errors"])
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {results_file}")
        except Exception as e:
            logger.error(f"Error saving results to file: {e}")
        
    except Exception as e:
        logger.error(f"Error in processing pipeline: {str(e)}")
        processing_state["status"] = "error"
        processing_state["errors"].append(str(e))


def process_resume_file(file_path: str) -> Dict:
    """Process a resume file (PDF, JSON, or TXT)."""
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
    
    elif pdf_validator.is_txt(path):
        # Extract text from TXT
        text_data = pdf_extractor.extract_text_from_txt_with_metadata(path)
        text = text_data["text"]
        
        # Parse to structured JSON
        resume_data = resume_parser.parse_from_text(text)
        
        # Save to storage
        storage.save_resume(resume_data)
        
        return resume_data
    
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")


def process_jd_file(file_path: str) -> Dict:
    """Process a job description file (PDF, JSON, or TXT)."""
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
    
    elif pdf_validator.is_txt(path):
        # Extract text from TXT
        text_data = pdf_extractor.extract_text_from_txt_with_metadata(path)
        text = text_data["text"]
        
        # Parse to structured JSON
        jd_data = jd_parser.parse_from_text(text)
        
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
    # First check if there's an active processing with results
    if processing_state["status"] == "completed" and processing_state["results"]:
        return {
            "results": processing_state["results"],
            "total": len(processing_state["results"]),
        }
    
    # Otherwise, try to load from file
    try:
        results_file = config.output_path / "latest_results.json"
        if results_file.exists():
            with open(results_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "results": data.get("results", []),
                    "total": len(data.get("results", [])),
                    "timestamp": data.get("timestamp"),
                    "jd_id": data.get("jd_id")
                }
    except Exception as e:
        logger.error(f"Error loading results from file: {e}")
    
    # If no results found anywhere
    raise HTTPException(status_code=400, detail="Processing not completed")


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
    resumes_summary = storage.list_resumes()
    # Get full resume data for each
    full_resumes = []
    for resume_info in resumes_summary:
        try:
            full_resume = storage.get_resume(resume_info['candidate_id'])
            full_resumes.append(full_resume)
        except Exception as e:
            logger.warning(f"Error loading resume {resume_info['candidate_id']}: {e}")
    return full_resumes


@app.get("/api/storage/job-descriptions")
async def list_job_descriptions():
    """List all stored job descriptions."""
    jds_summary = storage.list_jds()
    # Get full JD data for each
    full_jds = []
    for jd_info in jds_summary:
        try:
            full_jd = storage.get_jd(jd_info['jd_id'])
            full_jds.append(full_jd)
        except Exception as e:
            logger.warning(f"Error loading JD {jd_info['jd_id']}: {e}")
    return full_jds


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

