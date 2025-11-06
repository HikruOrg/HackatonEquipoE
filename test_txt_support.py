"""Test script to verify TXT file support for job descriptions."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.pdf_processing import PDFExtractor, PDFValidator
from src.preprocessing import JDParser

def test_txt_support():
    """Test TXT file support."""
    print("=" * 60)
    print("Testing TXT File Support for Job Descriptions")
    print("=" * 60)
    
    # Test file path
    txt_file = Path("data/job_descriptions/raw/test_job.txt")
    
    if not txt_file.exists():
        print(f"❌ Test file not found: {txt_file}")
        return False
    
    print(f"\n✓ Test file found: {txt_file}")
    
    # Test 1: Validate TXT file
    print("\n" + "=" * 60)
    print("Test 1: Validating TXT file")
    print("=" * 60)
    
    validator = PDFValidator()
    
    # Check if it's recognized as TXT
    is_txt = validator.is_txt(txt_file)
    print(f"Is TXT file: {is_txt}")
    
    if not is_txt:
        print("❌ File not recognized as TXT")
        return False
    
    # Validate TXT
    is_valid, error = validator.validate_txt(txt_file)
    print(f"Validation result: {is_valid}")
    if error:
        print(f"Validation error: {error}")
        return False
    
    print("✓ TXT file validated successfully")
    
    # Test 2: Extract text from TXT file
    print("\n" + "=" * 60)
    print("Test 2: Extracting text from TXT file")
    print("=" * 60)
    
    extractor = PDFExtractor(require_pdfplumber=False)
    
    try:
        text_data = extractor.extract_text_from_txt_with_metadata(txt_file)
        text = text_data["text"]
        metadata = text_data["metadata"]
        
        print(f"Extracted {len(text)} characters")
        print(f"Metadata: {metadata}")
        print(f"\nFirst 200 characters:\n{text[:200]}...")
        print("\n✓ Text extracted successfully")
        
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return False
    
    # Test 3: Parse JD from text
    print("\n" + "=" * 60)
    print("Test 3: Parsing job description from text")
    print("=" * 60)
    
    parser = JDParser()
    
    try:
        jd_data = parser.parse_from_text(text)
        
        print(f"Job Title: {jd_data.get('title')}")
        print(f"Must Have Requirements: {len(jd_data.get('must_have_requirements', []))} items")
        print(f"Nice to Have: {len(jd_data.get('nice_to_have', []))} items")
        print(f"Years Required: {jd_data.get('experience_years_required')}")
        
        print(f"\nMust Have Requirements:")
        for req in jd_data.get('must_have_requirements', [])[:5]:
            print(f"  - {req}")
        
        if jd_data.get('nice_to_have'):
            print(f"\nNice to Have:")
            for req in jd_data.get('nice_to_have', [])[:5]:
                print(f"  - {req}")
        
        print("\n✓ Job description parsed successfully")
        
    except Exception as e:
        print(f"❌ Error parsing JD: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print("\nTXT file support is working correctly!")
    print("You can now upload .txt files for job descriptions in addition to PDF and JSON files.")
    
    return True


if __name__ == "__main__":
    success = test_txt_support()
    sys.exit(0 if success else 1)
