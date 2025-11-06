"""Configuration management for AI Talent Matcher."""
from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration loaded from environment variables."""
    
    # LLM Provider Configuration (LangChain Unified)
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    # Google Gemini Configuration
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    # Anthropic Configuration
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    
    # Ollama Configuration
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Common LLM Parameters
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    llm_timeout: int = int(os.getenv("LLM_TIMEOUT", "60"))
    
    # Scoring Weights
    similarity_weight: float = float(os.getenv("SIMILARITY_WEIGHT", "0.6"))
    must_have_boost_weight: float = float(os.getenv("MUST_HAVE_BOOST_WEIGHT", "0.3"))
    recency_boost_weight: float = float(os.getenv("RECENCY_BOOST_WEIGHT", "0.1"))
    
    # Storage Configuration
    storage_type: str = os.getenv("STORAGE_TYPE", "local")
    storage_path: str = os.getenv("STORAGE_PATH", "./data/storage")
    
    # Cache Configuration
    enable_cache: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    cache_path: str = os.getenv("CACHE_PATH", "./data/cache")
    cache_embeddings: bool = os.getenv("CACHE_EMBEDDINGS", "true").lower() == "true"
    cache_llm_responses: bool = os.getenv("CACHE_LLM_RESPONSES", "true").lower() == "true"
    cache_scores: bool = os.getenv("CACHE_SCORES", "true").lower() == "true"
    cache_ttl: int = int(os.getenv("CACHE_TTL", "2592000"))  # 30 days default
    
    # Output Configuration
    output_dir: str = os.getenv("OUTPUT_DIR", "./data/output")
    csv_encoding: str = os.getenv("CSV_ENCODING", "utf-8")
    
    # Prompt Paths
    prompts_dir: str = os.getenv("PROMPTS_DIR", "./src/prompts")
    
    # Data Paths
    resumes_raw_dir: Path = Path(os.getenv("RESUMES_RAW_DIR", "./data/resumes/raw"))
    resumes_processed_dir: Path = Path(os.getenv("RESUMES_PROCESSED_DIR", "./data/resumes/processed"))
    jd_raw_dir: Path = Path(os.getenv("JD_RAW_DIR", "./data/job_descriptions/raw"))
    jd_processed_dir: Path = Path(os.getenv("JD_PROCESSED_DIR", "./data/job_descriptions/processed"))
    
    def __post_init__(self):
        """Ensure directories exist."""
        # Create directories if they don't exist
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)
        Path(self.cache_path).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        self.resumes_raw_dir.mkdir(parents=True, exist_ok=True)
        self.resumes_processed_dir.mkdir(parents=True, exist_ok=True)
        self.jd_raw_dir.mkdir(parents=True, exist_ok=True)
        self.jd_processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Create storage subdirectories
        Path(self.storage_path, "resumes").mkdir(parents=True, exist_ok=True)
        Path(self.storage_path, "job_descriptions").mkdir(parents=True, exist_ok=True)
        
        # Create cache subdirectories
        Path(self.cache_path, "embeddings").mkdir(parents=True, exist_ok=True)
        Path(self.cache_path, "llm_responses").mkdir(parents=True, exist_ok=True)
        Path(self.cache_path, "scores").mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> bool:
        """Validate configuration."""
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        if self.llm_provider == "gemini" and not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required when LLM_PROVIDER=gemini")
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")
        
        # Validate weights sum to 1.0
        total_weight = self.similarity_weight + self.must_have_boost_weight + self.recency_boost_weight
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Scoring weights must sum to 1.0, got {total_weight}")
        
        return True


# Global config instance
config = Config()

