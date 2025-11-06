# Infrastructure Guidelines

## Technology Stack

### Core Technologies
- **Programming Language:** Python 3.9+
- **PDF Processing:**
  - `PyPDF2` or `pdfplumber` for PDF text extraction
  - `pypdf` (modern alternative to PyPDF2)
  - Optional: `pytesseract` + `pdf2image` for OCR on scanned PDFs
- **LLM Framework:** 
  - `openai` for OpenAI API (GPT-4, GPT-3.5)
  - `anthropic` for Claude API (alternative)
  - `langchain` for LLM orchestration and prompt management
  - `ollama` for local LLM models (optional)
- **Storage:**
  - `boto3` for AWS S3 integration
  - `azure-storage-blob` for Azure Blob Storage
  - `google-cloud-storage` for Google Cloud Storage
  - Local filesystem as default option
- **Data Processing:**
  - `pandas` for data manipulation
  - `json` for JSON parsing
- **Export:**
  - `csv` module or `pandas.to_csv()` for CSV export

### Recommended Dependencies
```python
# PDF Processing
pdfplumber>=0.10.0  # PDF text extraction (recommended)
# Alternative: PyPDF2>=3.0.0 or pypdf>=3.0.0
# Optional for OCR: pytesseract>=0.3.10, pdf2image>=1.16.0, Pillow>=10.0.0

# Core LLM/AI
openai>=1.0.0  # OpenAI API client
langchain>=0.1.0  # LLM orchestration and prompt management
langchain-openai>=0.0.5  # LangChain OpenAI integration
# Alternative: anthropic>=0.18.0 for Claude

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Storage (Optional - choose based on provider)
boto3>=1.28.0  # AWS S3
azure-storage-blob>=12.19.0  # Azure Blob Storage
google-cloud-storage>=2.10.0  # Google Cloud Storage

# Utilities
python-dotenv>=1.0.0  # Environment variables
pydantic>=2.0.0  # Data validation
tenacity>=8.2.0  # Retry logic for API calls
```

## Project Structure

```
HackatonEquipoE/
├── src/
│   ├── __init__.py
│   ├── pdf_processing/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py      # Extract text from PDFs
│   │   └── pdf_validator.py      # Validate PDF files
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── resume_parser.py      # Parse text to structured JSON resumes
│   │   └── jd_parser.py          # Parse text to structured JSON job descriptions
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py              # LLM client initialization
│   │   ├── analyzer.py            # LLM-based resume/JD analysis
│   │   └── response_parser.py    # Parse LLM structured responses
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── scoring_prompt.py      # Prompt for scoring candidates
│   │   ├── similarity_prompt.py   # Prompt for similarity analysis
│   │   ├── reason_codes_prompt.py # Prompt for reason code generation
│   │   └── templates/             # Prompt templates directory
│   │       ├── scoring_template.txt
│   │       ├── similarity_template.txt
│   │       └── reason_codes_template.txt
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── hybrid_scorer.py      # Hybrid scoring system
│   │   └── rule_boosts.py         # Rule-based boosts
│   ├── explainability/
│   │   ├── __init__.py
│   │   ├── reason_codes.py       # Reason code mapping
│   │   └── hit_mapper.py         # Map hits to resume lines
│   ├── export/
│   │   ├── __init__.py
│   │   └── csv_exporter.py       # CSV export functionality
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── storage_client.py     # Storage client abstraction
│   │   ├── local_storage.py      # Local filesystem storage
│   │   ├── s3_storage.py         # AWS S3 storage
│   │   ├── azure_storage.py      # Azure Blob storage
│   │   └── gcs_storage.py        # Google Cloud Storage
│   ├── config.py                  # Configuration management
│   └── main.py                   # Main application entry point
├── data/
│   ├── resumes/                  # Input resume files
│   │   ├── raw/                  # Original PDF files
│   │   └── processed/            # Extracted JSON files
│   ├── job_descriptions/         # Input JD files
│   │   ├── raw/                  # Original PDF files
│   │   └── processed/            # Extracted JSON files
│   ├── storage/                  # Storage for JSONs
│   │   ├── resumes/              # Stored resume JSONs
│   │   └── job_descriptions/     # Stored JD JSONs
│   └── output/                   # Generated CSV exports
├── prompts/                      # Centralized prompt definitions
│   ├── scoring_prompts.yaml      # YAML format prompts (optional)
│   └── prompt_library.md         # Documentation of all prompts
├── tests/
│   ├── __init__.py
│   ├── test_pdf_extraction.py
│   ├── test_preprocessing.py
│   ├── test_llm.py
│   ├── test_scoring.py
│   └── test_export.py
├── docs/
│   ├── PROJECT_GUIDELINES.md
│   ├── INFRA_GUIDELINES.MD
│   └── REQUIREMENTES.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Environment Setup

### Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file (use `.env.example` as template):
```env
# LLM Provider Configuration
LLM_PROVIDER=openai  # Options: openai, anthropic, ollama
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview  # Options: gpt-4, gpt-4-turbo-preview, gpt-3.5-turbo
# Alternative: ANTHROPIC_API_KEY=your_anthropic_key (if using Claude)
# Alternative: OLLAMA_BASE_URL=http://localhost:11434 (if using local Ollama)

# LLM Configuration
LLM_TEMPERATURE=0.3  # Lower temperature for more consistent scoring
LLM_MAX_TOKENS=2000  # Maximum tokens for LLM responses
LLM_TIMEOUT=60  # Timeout in seconds for API calls

# Scoring Weights (0.0 to 1.0)
SIMILARITY_WEIGHT=0.6
MUST_HAVE_BOOST_WEIGHT=0.3
RECENCY_BOOST_WEIGHT=0.1

# Storage Configuration
STORAGE_TYPE=local  # Options: local, s3, azure, gcs
STORAGE_PATH=./data/storage  # Local path or cloud bucket name

# AWS S3 Configuration (if STORAGE_TYPE=s3)
# AWS_ACCESS_KEY_ID=your_access_key
# AWS_SECRET_ACCESS_KEY=your_secret_key
# AWS_S3_BUCKET=your_bucket_name
# AWS_REGION=us-east-1

# Azure Blob Storage Configuration (if STORAGE_TYPE=azure)
# AZURE_STORAGE_CONNECTION_STRING=your_connection_string
# AZURE_STORAGE_CONTAINER=your_container_name

# Google Cloud Storage Configuration (if STORAGE_TYPE=gcs)
# GCS_PROJECT_ID=your_project_id
# GCS_BUCKET_NAME=your_bucket_name
# GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Output Configuration
OUTPUT_DIR=./data/output
CSV_ENCODING=utf-8

# Retry Configuration
API_MAX_RETRIES=3
API_RETRY_DELAY=2  # seconds
```

## Data Handling

### Input Format

#### PDF Input (Primary)
- **Resume PDFs:** Place PDF files in `data/resumes/raw/` directory
- **Job Description PDFs:** Place PDF files in `data/job_descriptions/raw/` directory
- **Supported Formats:** PDF files with native text (preferred) or scanned PDFs (requires OCR)

#### Resume JSON Structure (After PDF Processing)
```json
{
  "candidate_id": "unique_id",
  "name": "Candidate Name",
  "skills": ["skill1", "skill2", "skill3"],
  "experience": [
    {
      "company": "Company Name",
      "position": "Job Title",
      "start_date": "2020-01",
      "end_date": "2022-12",
      "description": "Job description text"
    }
  ],
  "education": [
    {
      "institution": "University Name",
      "degree": "Degree Type",
      "field": "Field of Study",
      "year": 2020
    }
  ],
  "raw_text": "Full extracted text from resume"
}
```

#### Job Description Format (After PDF Processing)
```json
{
  "jd_id": "unique_jd_id",
  "title": "Job Title",
  "must_have_requirements": [
    "requirement1",
    "requirement2"
  ],
  "nice_to_have": [
    "requirement3"
  ],
  "description": "Full job description text",
  "experience_years_required": 3
}
```

### Output Format

#### CSV Export Structure
```csv
rank,candidate_id,name,overall_score,similarity_score,must_have_hits,recency_boost,reason_codes,matched_requirements
1,id_001,John Doe,0.85,0.72,3,0.13,"SKILL_MATCH,EXPERIENCE_MATCH,RECENT_EXP","Python,5+ years,2023"
```

## Development Workflow

### Code Standards
- **Style:** Follow PEP 8 Python style guide
- **Type Hints:** Use type hints for function signatures
- **Documentation:** Docstrings for all functions and classes
- **Linting:** Use `flake8` or `pylint`
- **Formatting:** Use `black` for code formatting

### Testing Strategy
- **Unit Tests:** Test individual components (PDF extraction, preprocessing, LLM, scoring)
- **Integration Tests:** Test end-to-end workflow (PDF → JSON → Analysis → Export)
- **Test Data:** Use sample PDF resumes and JDs in `tests/fixtures/`

### Version Control
- **Branch Strategy:** Feature branches from `main`
- **Commit Messages:** Clear, descriptive commit messages
- **Git Ignore:** Exclude `venv/`, `__pycache__/`, `.env`, `data/output/`

## Prompt Management

### Prompt Structure
Prompts should be defined in `src/prompts/` directory and follow a consistent structure:

#### Prompt Template Format
```python
# src/prompts/scoring_prompt.py
SCORING_PROMPT = """
You are an expert recruiter analyzing candidate resumes against a job description.

Job Description:
{job_description}

Must-Have Requirements:
{must_have_requirements}

Candidate Resume:
{resume_text}

Please analyze and provide:
1. Overall match score (0-100)
2. Similarity score (0-100)
3. Must-have requirements matched (list)
4. Reason codes explaining the match
5. Specific resume sections that match JD requirements

Format your response as JSON:
{{
    "overall_score": <float>,
    "similarity_score": <float>,
    "must_have_matches": [<list>],
    "reason_codes": [<list>],
    "matched_sections": {{
        "requirement": "resume_section_reference"
    }}
}}
"""
```

### Prompt Organization
- **Centralized Storage:** Store all prompts in `src/prompts/` directory
- **Template Files:** Use `.txt` files for complex multi-line prompts
- **Python Modules:** Use `.py` files for prompts with dynamic variables
- **Version Control:** Track prompt changes in git
- **Documentation:** Document prompt purpose and expected output format

### Prompt Best Practices
- **Clear Instructions:** Provide explicit instructions to the LLM
- **Structured Output:** Request JSON or structured format for parsing
- **Examples:** Include few-shot examples when helpful
- **Constraints:** Specify score ranges, format requirements
- **Context:** Provide sufficient context (JD, resume, requirements)

## Performance Considerations

### LLM API Usage
- **Rate Limiting:** Implement rate limiting to respect API quotas
- **Caching:** Cache LLM responses for identical inputs to reduce API calls
- **Batch Processing:** Process multiple candidates sequentially with delays
- **Async Processing:** Use async/await for concurrent API calls (with rate limits)
- **Token Management:** Monitor token usage to control costs

### Model Selection
- **Cost vs Quality:** Balance between model cost and accuracy
  - GPT-3.5-turbo: Faster, cheaper, good for initial filtering
  - GPT-4: More accurate, better reasoning, higher cost
  - Claude: Alternative with good reasoning capabilities
- **Temperature:** Use lower temperature (0.1-0.3) for consistent scoring

### Memory Management
- **Streaming:** Process large datasets in batches
- **Response Caching:** Cache parsed LLM responses to avoid reprocessing
- **Resource Limits:** Set memory limits for production
- **Connection Pooling:** Reuse API connections when possible

## Security & Privacy

### Data Protection
- **Sensitive Data:** Do not commit resume data or personal information to git
- **Environment Variables:** Store API keys and secrets in `.env` (not committed)
- **Data Anonymization:** Consider anonymizing candidate data for testing

### Access Control
- **File Permissions:** Restrict access to data directories
- **API Keys:** Rotate keys regularly if using external APIs

## Deployment Considerations

### Local Development
- **Requirements:** Python 3.9+, 4GB+ RAM recommended
- **Dependencies:** Install via `requirements.txt`
- **Data:** Place sample data in `data/` directories

### Production Deployment
- **Containerization:** Consider Docker for consistent environments
- **API Service:** If needed, use FastAPI or Flask for REST API
- **Scaling:** Consider async processing for large batches
- **Monitoring:** Log scoring metrics and performance

## Configuration Management

### Configuration Files
- **LLM Config:** Store LLM provider and model selection in config
- **Prompt Config:** Centralize prompt loading and management
- **Scoring Weights:** Make weights configurable via environment variables
- **File Paths:** Use relative paths with configurable base directory

### Example Configuration Class
```python
# src/config.py
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # LLM Configuration
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    llm_timeout: int = int(os.getenv("LLM_TIMEOUT", "60"))
    
    # Retry Configuration
    api_max_retries: int = int(os.getenv("API_MAX_RETRIES", "3"))
    api_retry_delay: int = int(os.getenv("API_RETRY_DELAY", "2"))
    
    # Scoring Weights
    similarity_weight: float = float(os.getenv("SIMILARITY_WEIGHT", "0.6"))
    must_have_boost_weight: float = float(os.getenv("MUST_HAVE_BOOST_WEIGHT", "0.3"))
    recency_boost_weight: float = float(os.getenv("RECENCY_BOOST_WEIGHT", "0.1"))
    
    # Output Configuration
    output_dir: str = os.getenv("OUTPUT_DIR", "./data/output")
    csv_encoding: str = os.getenv("CSV_ENCODING", "utf-8")
    
    # Prompt Paths
    prompts_dir: str = os.getenv("PROMPTS_DIR", "./src/prompts")
```

### Prompt Loading Example
```python
# src/prompts/prompt_loader.py
from pathlib import Path
from typing import Dict

class PromptLoader:
    def __init__(self, prompts_dir: str = "./src/prompts"):
        self.prompts_dir = Path(prompts_dir)
        self._prompts: Dict[str, str] = {}
    
    def load_prompt(self, prompt_name: str) -> str:
        """Load prompt from file or cache."""
        if prompt_name in self._prompts:
            return self._prompts[prompt_name]
        
        prompt_file = self.prompts_dir / f"{prompt_name}.txt"
        if prompt_file.exists():
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read()
                self._prompts[prompt_name] = prompt
                return prompt
        
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    def format_prompt(self, prompt_name: str, **kwargs) -> str:
        """Load and format prompt with variables."""
        prompt_template = self.load_prompt(prompt_name)
        return prompt_template.format(**kwargs)
```

## Logging & Monitoring

### Logging Setup
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Key Metrics to Track
- Processing time per resume
- LLM API call time and latency
- Token usage per request (input/output)
- API cost per candidate
- Scoring calculation time
- Memory usage
- Error rates and retry counts
- Rate limit hits

## Error Handling

### Exception Handling
- **File Not Found:** Handle missing input files gracefully
- **Invalid JSON:** Validate JSON structure before processing
- **API Errors:** Handle LLM API errors (rate limits, timeouts, invalid responses)
- **Rate Limiting:** Implement exponential backoff for rate limit errors
- **Timeout Errors:** Retry on timeout with exponential backoff
- **Invalid Responses:** Validate LLM response format and retry if invalid
- **Memory Errors:** Catch and handle out-of-memory situations

### Validation
- **Input Validation:** Validate resume and JD structure
- **Score Validation:** Ensure scores are within expected ranges (0-1)
- **Output Validation:** Verify CSV export integrity

## Dependencies Management

### requirements.txt Structure
```
# PDF Processing
pdfplumber>=0.10.0  # PDF text extraction
# Optional for OCR: pytesseract>=0.3.10, pdf2image>=1.16.0, Pillow>=10.0.0

# Core LLM/AI
openai>=1.0.0
langchain>=0.1.0
langchain-openai>=0.0.5
# Alternative: anthropic>=0.18.0  # For Claude API

# Storage (Optional - install based on provider)
boto3>=1.28.0  # AWS S3
azure-storage-blob>=12.19.0  # Azure Blob Storage
google-cloud-storage>=2.10.0  # Google Cloud Storage

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Utilities
python-dotenv>=1.0.0
pydantic>=2.0.0
tenacity>=8.2.0  # Retry logic for API calls
pyyaml>=6.0  # For YAML prompt files (optional)

# Development
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
```

### Dependency Updates
- **Regular Updates:** Keep dependencies updated for security
- **Version Pinning:** Pin major versions, allow minor/patch updates
- **Security Audits:** Run `pip-audit` or `safety` for vulnerability checks

## LLM Integration Example

### Basic LLM Client Setup
```python
# src/llm/client.py
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from src.config import Config

class LLMClient:
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def analyze_candidate(self, prompt: str) -> str:
        """Call LLM API with retry logic."""
        try:
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": "You are an expert recruiter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.llm_temperature,
                max_tokens=self.config.llm_max_tokens,
                response_format={"type": "json_object"}  # Request JSON response
            )
            return response.choices[0].message.content
        except Exception as e:
            # Log error and retry
            raise
```

### Using Prompts
```python
# src/llm/analyzer.py
from src.llm.client import LLMClient
from src.prompts.prompt_loader import PromptLoader
import json

class ResumeAnalyzer:
    def __init__(self, llm_client: LLMClient, prompt_loader: PromptLoader):
        self.llm_client = llm_client
        self.prompt_loader = prompt_loader
    
    def score_candidate(self, resume: dict, job_description: dict) -> dict:
        """Score a candidate against a job description."""
        # Load and format prompt
        prompt = self.prompt_loader.format_prompt(
            "scoring_prompt",
            job_description=job_description["description"],
            must_have_requirements="\n".join(job_description["must_have_requirements"]),
            resume_text=resume["raw_text"]
        )
        
        # Call LLM
        response = self.llm_client.analyze_candidate(prompt)
        
        # Parse JSON response
        result = json.loads(response)
        return result
```

## Storage Integration Example

### Storage Client Abstraction
```python
# src/storage/storage_client.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import json

class StorageClient(ABC):
    """Abstract base class for storage implementations."""
    
    @abstractmethod
    def save_json(self, json_data: dict, file_name: str, file_type: str) -> bool:
        """Save JSON to storage. file_type: 'resume' or 'job_description'."""
        pass
    
    @abstractmethod
    def list_jsons(self, file_type: str, filters: Optional[Dict] = None) -> List[Dict]:
        """List available JSONs. Returns list of metadata dicts."""
        pass
    
    @abstractmethod
    def get_json(self, file_name: str, file_type: str) -> Optional[dict]:
        """Retrieve JSON from storage."""
        pass
    
    @abstractmethod
    def delete_json(self, file_name: str, file_type: str) -> bool:
        """Delete JSON from storage."""
        pass
    
    @abstractmethod
    def search_jsons(self, query: str, file_type: str) -> List[Dict]:
        """Search JSONs by name or content."""
        pass

# src/storage/local_storage.py
from pathlib import Path
from typing import List, Optional, Dict
import json
from datetime import datetime
from .storage_client import StorageClient

class LocalStorage(StorageClient):
    def __init__(self, base_path: str = "./data/storage"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save_json(self, json_data: dict, file_name: str, file_type: str) -> bool:
        """Save JSON to local filesystem."""
        try:
            file_path = self.base_path / file_type / f"{file_name}.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    def list_jsons(self, file_type: str, filters: Optional[Dict] = None) -> List[Dict]:
        """List available JSONs with metadata."""
        json_dir = self.base_path / file_type
        if not json_dir.exists():
            return []
        
        json_files = []
        for json_file in json_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    metadata = {
                        "file_name": json_file.stem,
                        "full_path": str(json_file),
                        "size": json_file.stat().st_size,
                        "modified": datetime.fromtimestamp(json_file.stat().st_mtime).isoformat(),
                        "name": data.get("name") or data.get("title", "Unknown")
                    }
                    json_files.append(metadata)
            except:
                continue
        
        return json_files
    
    def get_json(self, file_name: str, file_type: str) -> Optional[dict]:
        """Retrieve JSON from local storage."""
        file_path = self.base_path / file_type / f"{file_name}.json"
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return None
    
    def delete_json(self, file_name: str, file_type: str) -> bool:
        """Delete JSON from local storage."""
        file_path = self.base_path / file_type / f"{file_name}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    def search_jsons(self, query: str, file_type: str) -> List[Dict]:
        """Search JSONs by name or content."""
        all_jsons = self.list_jsons(file_type)
        query_lower = query.lower()
        
        results = []
        for json_meta in all_jsons:
            # Search in file name
            if query_lower in json_meta["file_name"].lower():
                results.append(json_meta)
                continue
            
            # Search in JSON content
            json_data = self.get_json(json_meta["file_name"], file_type)
            if json_data:
                json_str = json.dumps(json_data).lower()
                if query_lower in json_str:
                    results.append(json_meta)
        
        return results
```

## PDF Processing Example

### Basic PDF Text Extraction
```python
# src/pdf_processing/pdf_extractor.py
import pdfplumber
from pathlib import Path
from typing import Optional

class PDFExtractor:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text(self, pdf_path: str) -> Optional[str]:
        """Extract text from PDF file."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_parts = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                return '\n\n'.join(text_parts)
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {e}")
    
    def validate_pdf(self, pdf_path: str) -> bool:
        """Validate that PDF can be opened and processed."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages) > 0
        except:
            return False
```

## Quick Start Checklist

- [ ] Set up Python virtual environment
- [ ] Install dependencies from `requirements.txt` (including PDF processing libraries)
- [ ] Configure `.env` file with LLM API key and settings
- [ ] Create project directory structure (including `src/pdf_processing/` and `src/prompts/`)
- [ ] Define initial prompts in `src/prompts/` directory
- [ ] Place sample resume PDF files in `data/resumes/raw/`
- [ ] Place sample JD PDF files in `data/job_descriptions/raw/`
- [ ] Test PDF extraction with sample files
- [ ] Test LLM API connection with a simple prompt
- [ ] Run tests to verify setup
- [ ] Execute main pipeline with sample data (PDF → JSON → Analysis → Export)
