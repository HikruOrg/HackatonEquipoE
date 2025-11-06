"""Test the auto-processing functionality."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.startup import AutoProcessor
from src.config import config

def test_auto_processor():
    """Test auto-processor."""
    print("=" * 60)
    print("Testing Auto-Processor")
    print("=" * 60)
    
    # Show directories being monitored
    print(f"\nDirectories being monitored:")
    print(f"  Resumes raw: {config.resumes_raw_dir}")
    print(f"  Job descriptions raw: {config.jd_raw_dir}")
    
    # List files in directories
    resume_files = list(config.resumes_raw_dir.glob("*"))
    jd_files = list(config.jd_raw_dir.glob("*"))
    
    print(f"\nFiles found:")
    print(f"  Resumes: {len([f for f in resume_files if f.is_file()])} files")
    for f in resume_files:
        if f.is_file():
            print(f"    - {f.name} ({f.suffix})")
    
    print(f"  Job descriptions: {len([f for f in jd_files if f.is_file()])} files")
    for f in jd_files:
        if f.is_file():
            print(f"    - {f.name} ({f.suffix})")
    
    # Run auto-processor
    print("\n" + "=" * 60)
    print("Running auto-processor...")
    print("=" * 60 + "\n")
    
    processor = AutoProcessor()
    results = processor.process_all()
    
    # Show results
    print("\n" + "=" * 60)
    print("Results Summary:")
    print("=" * 60)
    print(f"\nResumes:")
    print(f"  Total: {results['resumes']['total']}")
    print(f"  Processed: {results['resumes']['processed']}")
    print(f"  Skipped: {results['resumes']['skipped']}")
    print(f"  Failed: {results['resumes']['failed']}")
    
    print(f"\nJob Descriptions:")
    print(f"  Total: {results['job_descriptions']['total']}")
    print(f"  Processed: {results['job_descriptions']['processed']}")
    print(f"  Skipped: {results['job_descriptions']['skipped']}")
    print(f"  Failed: {results['job_descriptions']['failed']}")
    
    # Check storage
    from src.storage import LocalStorage
    storage = LocalStorage()
    
    stored_resumes = storage.list_resumes()
    stored_jds = storage.list_jds()
    
    print(f"\nStored in database:")
    print(f"  Resumes: {len(stored_resumes)}")
    print(f"  Job descriptions: {len(stored_jds)}")
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    test_auto_processor()
