"""
Test script to verify TXT file upload and processing functionality.
"""
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  'requests' module not available. API tests will be skipped.")

from pathlib import Path

# API endpoint
BASE_URL = "http://localhost:8000"

def test_txt_upload():
    """Test uploading a TXT file as job description."""
    
    # Path to the test TXT file
    txt_file_path = Path("data/job_descriptions/raw/test_job.txt")
    
    if not txt_file_path.exists():
        print(f"❌ Test file not found: {txt_file_path}")
        return False
    
    print(f"📄 Testing TXT file upload: {txt_file_path.name}")
    print(f"📊 File size: {txt_file_path.stat().st_size} bytes")
    
    # Upload the TXT file as a job description
    try:
        with open(txt_file_path, 'rb') as f:
            files = {'file': (txt_file_path.name, f, 'text/plain')}
            response = requests.post(
                f"{BASE_URL}/api/upload/job-description",
                files=files
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful!")
            print(f"   - Filename: {result.get('filename')}")
            print(f"   - Type: {result.get('type')}")
            print(f"   - Path: {result.get('path')}")
            return True
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {str(e)}")
        return False

def test_txt_validation():
    """Test TXT file validation."""
    from src.pdf_processing import PDFValidator
    
    txt_file_path = Path("data/job_descriptions/raw/test_job.txt")
    
    if not txt_file_path.exists():
        print(f"❌ Test file not found: {txt_file_path}")
        return False
    
    print(f"\n🔍 Testing TXT file validation...")
    
    validator = PDFValidator()
    
    # Check if file is recognized as TXT
    is_txt = validator.is_txt(txt_file_path)
    print(f"   - Is TXT: {is_txt}")
    
    # Validate TXT file
    is_valid, error = validator.validate_txt(txt_file_path)
    
    if is_valid:
        print(f"✅ Validation successful!")
        return True
    else:
        print(f"❌ Validation failed: {error}")
        return False

def test_txt_extraction():
    """Test TXT file text extraction."""
    from src.pdf_processing import PDFExtractor
    
    txt_file_path = Path("data/job_descriptions/raw/test_job.txt")
    
    if not txt_file_path.exists():
        print(f"❌ Test file not found: {txt_file_path}")
        return False
    
    print(f"\n📖 Testing TXT file extraction...")
    
    extractor = PDFExtractor(require_pdfplumber=False)
    
    try:
        # Extract text with metadata
        result = extractor.extract_text_from_txt_with_metadata(txt_file_path)
        
        print(f"✅ Extraction successful!")
        print(f"   - Text length: {len(result['text'])} characters")
        print(f"   - File type: {result['file_type']}")
        print(f"   - First 100 chars: {result['text'][:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TXT File Support Test Suite")
    print("=" * 60)
    
    # Test validation
    test_txt_validation()
    
    # Test extraction
    test_txt_extraction()
    
    # Test upload (requires server to be running)
    if REQUESTS_AVAILABLE:
        print(f"\n🌐 Testing API upload (requires server running)...")
        try:
            # Check if server is running
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                test_txt_upload()
            else:
                print("❌ Server is not responding correctly")
        except requests.exceptions.ConnectionError:
            print("⚠️  Server is not running. Skipping API test.")
            print("   To test API upload, run: python run_server.py")
    else:
        print(f"\n⚠️  Skipping API tests (requests module not installed)")
        print("   Install with: pip install requests")
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)
