"""Test LLM-based parsing for resumes and job descriptions."""
import sys
from pathlib import Path
import json
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.llm import LLMClient
from src.preprocessing import ResumeParser, JDParser
from src.pdf_processing import PDFExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_llm_availability():
    """Test if LLM client is properly configured."""
    print("\n" + "="*80)
    print("TEST 1: LLM Client Availability")
    print("="*80)
    
    try:
        config.validate()
        llm_client = LLMClient(config)
        print("✅ LLM client initialized successfully")
        print("✅ LLM is ready for parsing tasks")
        return llm_client
    except Exception as e:
        print(f"❌ LLM client initialization failed: {e}")
        print("⚠️  Make sure Google API key is configured in .env file")
        return None


def test_resume_parsing_txt(llm_client):
    """Test resume parsing from TXT file with LLM."""
    print("\n" + "="*80)
    print("TEST 2: Resume Parsing from TXT (LLM-based)")
    print("="*80)
    
    txt_file = Path("data/resumes/raw/test_resume.txt")
    
    if not txt_file.exists():
        print(f"❌ Test file not found: {txt_file}")
        return False
    
    try:
        # Extract text
        extractor = PDFExtractor(require_pdfplumber=False)
        text_data = extractor.extract_text_from_txt_with_metadata(txt_file)
        print(f"✅ Text extracted from {txt_file.name}")
        print(f"   Text length: {len(text_data['text'])} characters")
        print(f"   Preview: {text_data['text'][:200]}...")
        
        # Parse with LLM
        parser = ResumeParser(use_llm=True, llm_client=llm_client)
        result = parser.parse_from_text(text_data['text'], "test_candidate_001")
        
        print(f"\n✅ Resume parsed successfully")
        print(f"   Candidate: {result.get('name', 'N/A')}")
        print(f"   Email: {result.get('email', 'N/A')}")
        print(f"   Skills: {len(result.get('skills', []))} skills found")
        print(f"   Experience: {len(result.get('experience', []))} positions")
        print(f"   Education: {len(result.get('education', []))} entries")
        
        # Show detailed output
        print("\n📊 Parsed Resume Data:")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])
        
        return True
        
    except Exception as e:
        print(f"❌ Resume parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_resume_parsing_json(llm_client):
    """Test resume parsing from JSON file (should use existing data)."""
    print("\n" + "="*80)
    print("TEST 3: Resume Parsing from JSON (Direct)")
    print("="*80)
    
    json_file = Path("data/resumes/raw/test_resume.json")
    
    if not json_file.exists():
        print(f"❌ Test file not found: {json_file}")
        return False
    
    try:
        parser = ResumeParser(use_llm=True, llm_client=llm_client)
        result = parser.parse_from_json(str(json_file))
        
        print(f"✅ Resume parsed from JSON")
        print(f"   Candidate: {result.get('name', 'N/A')}")
        print(f"   Email: {result.get('email', 'N/A')}")
        print(f"   Skills: {len(result.get('skills', []))} skills")
        
        return True
        
    except Exception as e:
        print(f"❌ JSON resume parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_jd_parsing_txt(llm_client):
    """Test job description parsing from TXT file with LLM."""
    print("\n" + "="*80)
    print("TEST 4: Job Description Parsing from TXT (LLM-based)")
    print("="*80)
    
    txt_file = Path("data/job_descriptions/raw/Senior Cloud Java Engineer.txt")
    
    if not txt_file.exists():
        # Try alternative
        txt_file = Path("data/job_descriptions/raw/test_job.txt")
        if not txt_file.exists():
            print(f"❌ No TXT job description files found")
            return False
    
    try:
        # Extract text
        extractor = PDFExtractor(require_pdfplumber=False)
        text_data = extractor.extract_text_from_txt_with_metadata(txt_file)
        print(f"✅ Text extracted from {txt_file.name}")
        print(f"   Text length: {len(text_data['text'])} characters")
        print(f"   Preview: {text_data['text'][:200]}...")
        
        # Parse with LLM
        parser = JDParser(use_llm=True, llm_client=llm_client)
        result = parser.parse_from_text(text_data['text'], "test_jd_001")
        
        print(f"\n✅ Job Description parsed successfully")
        print(f"   Title: {result.get('title', 'N/A')}")
        print(f"   Must-have requirements: {len(result.get('must_have_requirements', []))}")
        print(f"   Nice-to-have: {len(result.get('nice_to_have', []))}")
        print(f"   Experience required: {result.get('experience_years_required', 'N/A')} years")
        
        # Show requirements
        print("\n📋 Must-Have Requirements:")
        for i, req in enumerate(result.get('must_have_requirements', [])[:5], 1):
            print(f"   {i}. {req}")
        
        print("\n📊 Parsed JD Data:")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])
        
        return True
        
    except Exception as e:
        print(f"❌ Job description parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_jd_parsing_json(llm_client):
    """Test job description parsing from JSON file."""
    print("\n" + "="*80)
    print("TEST 5: Job Description Parsing from JSON (Direct)")
    print("="*80)
    
    json_file = Path("data/job_descriptions/raw/jd_backend_python_senior.json")
    
    if not json_file.exists():
        print(f"❌ Test file not found: {json_file}")
        return False
    
    try:
        parser = JDParser(use_llm=True, llm_client=llm_client)
        result = parser.parse_from_json(str(json_file))
        
        print(f"✅ Job Description parsed from JSON")
        print(f"   Title: {result.get('title', 'N/A')}")
        print(f"   Must-have: {len(result.get('must_have_requirements', []))}")
        print(f"   Experience: {result.get('experience_years_required', 'N/A')} years")
        
        return True
        
    except Exception as e:
        print(f"❌ JSON JD parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fallback_mechanism():
    """Test that fallback to rule-based parsing works."""
    print("\n" + "="*80)
    print("TEST 6: Fallback Mechanism (No LLM)")
    print("="*80)
    
    try:
        # Create parser without LLM
        parser = ResumeParser(use_llm=False)
        
        sample_text = """
        John Doe
        Email: john.doe@example.com
        
        Skills: Python, FastAPI, React
        
        Experience:
        - Senior Developer at Tech Corp (2020-2023)
        - Junior Developer at StartUp Inc (2018-2020)
        """
        
        result = parser.parse_from_text(sample_text, "fallback_test")
        
        print(f"✅ Fallback parsing works")
        print(f"   Name: {result.get('name', 'N/A')}")
        print(f"   Email: {result.get('email', 'N/A')}")
        print(f"   Skills: {result.get('skills', [])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_comparison_llm_vs_rules():
    """Compare LLM parsing vs rule-based parsing."""
    print("\n" + "="*80)
    print("TEST 7: LLM vs Rule-based Comparison")
    print("="*80)
    
    try:
        # Initialize LLM client
        llm_client = LLMClient(config)
        
        # Sample resume text
        txt_file = Path("data/resumes/raw/test_resume.txt")
        if not txt_file.exists():
            print("⚠️  Skipping comparison - test file not found")
            return True
        
        extractor = PDFExtractor(require_pdfplumber=False)
        text_data = extractor.extract_text_from_txt_with_metadata(txt_file)
        text = text_data['text']
        
        # Parse with LLM
        llm_parser = ResumeParser(use_llm=True, llm_client=llm_client)
        llm_result = llm_parser.parse_from_text(text, "comparison_llm")
        
        # Parse with rules
        rule_parser = ResumeParser(use_llm=False)
        rule_result = rule_parser.parse_from_text(text, "comparison_rules")
        
        print("\n📊 Comparison Results:")
        print(f"\n{'Metric':<25} {'LLM-based':<20} {'Rule-based':<20}")
        print("-" * 65)
        print(f"{'Name found':<25} {llm_result.get('name', 'N/A'):<20} {rule_result.get('name', 'N/A'):<20}")
        print(f"{'Email found':<25} {llm_result.get('email', 'N/A'):<20} {rule_result.get('email', 'N/A'):<20}")
        print(f"{'Skills count':<25} {len(llm_result.get('skills', [])):<20} {len(rule_result.get('skills', [])):<20}")
        print(f"{'Experience entries':<25} {len(llm_result.get('experience', [])):<20} {len(rule_result.get('experience', [])):<20}")
        print(f"{'Education entries':<25} {len(llm_result.get('education', [])):<20} {len(rule_result.get('education', [])):<20}")
        
        print("\n✅ Comparison complete")
        return True
        
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all LLM parsing tests."""
    print("\n" + "="*80)
    print("🧪 LLM PARSING COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # Test 1: LLM availability
    llm_client = test_llm_availability()
    if llm_client is None:
        print("\n⚠️  LLM not available - some tests will be skipped")
        results["skipped"] += 5
        
        # Only run fallback test
        if test_fallback_mechanism():
            results["passed"] += 1
        else:
            results["failed"] += 1
    else:
        results["passed"] += 1
        
        # Test 2-5: Parsing tests
        tests = [
            ("Resume TXT Parsing", lambda: test_resume_parsing_txt(llm_client)),
            ("Resume JSON Parsing", lambda: test_resume_parsing_json(llm_client)),
            ("JD TXT Parsing", lambda: test_jd_parsing_txt(llm_client)),
            ("JD JSON Parsing", lambda: test_jd_parsing_json(llm_client)),
            ("Fallback Mechanism", test_fallback_mechanism),
            ("LLM vs Rules", test_comparison_llm_vs_rules),
        ]
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    results["passed"] += 1
                else:
                    results["failed"] += 1
            except Exception as e:
                print(f"\n❌ {test_name} crashed: {e}")
                results["failed"] += 1
    
    # Print summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"✅ Passed:  {results['passed']}")
    print(f"❌ Failed:  {results['failed']}")
    print(f"⏭️  Skipped: {results['skipped']}")
    print(f"\nTotal: {results['passed'] + results['failed'] + results['skipped']}")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed")
    
    return results['failed'] == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
