"""Detailed validation tests for LLM parsing quality."""
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.llm import LLMClient
from src.preprocessing import ResumeParser, JDParser
from src.pdf_processing import PDFExtractor


def validate_resume_structure(result: dict) -> tuple[bool, list[str]]:
    """
    Validate resume parsing structure and quality.
    
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Required fields
    required_fields = ['candidate_id', 'name', 'email', 'skills', 'experience', 'education']
    for field in required_fields:
        if field not in result:
            issues.append(f"Missing required field: {field}")
    
    # Check name is not generic
    if 'name' in result:
        if result['name'] in ['Unknown', 'N/A', '', None]:
            issues.append("Name not properly extracted")
        elif len(result['name']) < 3:
            issues.append("Name seems too short")
    
    # Check email format
    if 'email' in result and result['email']:
        email = result['email']
        if '@' not in email or '.' not in email:
            issues.append(f"Invalid email format: {email}")
    
    # Check skills
    if 'skills' in result:
        if not isinstance(result['skills'], list):
            issues.append("Skills should be a list")
        elif len(result['skills']) == 0:
            issues.append("No skills extracted")
        elif len(result['skills']) < 3:
            issues.append("Very few skills extracted (< 3)")
    
    # Check experience
    if 'experience' in result:
        if not isinstance(result['experience'], list):
            issues.append("Experience should be a list")
        else:
            for i, exp in enumerate(result['experience']):
                if not isinstance(exp, dict):
                    issues.append(f"Experience entry {i} should be a dict")
                else:
                    # Check for important fields in experience
                    if 'company' not in exp and 'position' not in exp:
                        issues.append(f"Experience entry {i} missing company/position")
    
    # Check education
    if 'education' in result:
        if not isinstance(result['education'], list):
            issues.append("Education should be a list")
    
    return len(issues) == 0, issues


def validate_jd_structure(result: dict) -> tuple[bool, list[str]]:
    """
    Validate job description parsing structure and quality.
    
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Required fields
    required_fields = ['jd_id', 'title', 'must_have_requirements', 'nice_to_have']
    for field in required_fields:
        if field not in result:
            issues.append(f"Missing required field: {field}")
    
    # Check title
    if 'title' in result:
        if result['title'] in ['Unknown', 'N/A', '', None]:
            issues.append("Title not properly extracted")
        elif len(result['title']) < 5:
            issues.append("Title seems too short")
    
    # Check must-have requirements
    if 'must_have_requirements' in result:
        if not isinstance(result['must_have_requirements'], list):
            issues.append("Must-have requirements should be a list")
        elif len(result['must_have_requirements']) == 0:
            issues.append("No must-have requirements extracted")
    
    # Check nice-to-have
    if 'nice_to_have' in result:
        if not isinstance(result['nice_to_have'], list):
            issues.append("Nice-to-have should be a list")
    
    # Check experience years if present
    if 'experience_years_required' in result:
        exp_years = result['experience_years_required']
        if not isinstance(exp_years, (int, float)):
            issues.append(f"Experience years should be a number, got: {type(exp_years)}")
        elif exp_years < 0 or exp_years > 30:
            issues.append(f"Unrealistic experience years: {exp_years}")
    
    return len(issues) == 0, issues


def test_resume_quality():
    """Test quality of resume parsing."""
    print("\n" + "="*80)
    print("QUALITY TEST: Resume Parsing Validation")
    print("="*80)
    
    try:
        llm_client = LLMClient(config)
        extractor = PDFExtractor(require_pdfplumber=False)
        
        txt_file = Path("data/resumes/raw/test_resume.txt")
        text_data = extractor.extract_text_from_txt_with_metadata(txt_file)
        
        parser = ResumeParser(use_llm=True, llm_client=llm_client)
        result = parser.parse_from_text(text_data['text'], "quality_test")
        
        is_valid, issues = validate_resume_structure(result)
        
        print(f"\n📊 Resume Quality Report:")
        print(f"   File: {txt_file.name}")
        print(f"   Valid Structure: {'✅ Yes' if is_valid else '❌ No'}")
        print(f"   Name: {result.get('name', 'N/A')}")
        print(f"   Email: {result.get('email', 'N/A')}")
        print(f"   Skills Count: {len(result.get('skills', []))}")
        print(f"   Experience Entries: {len(result.get('experience', []))}")
        print(f"   Education Entries: {len(result.get('education', []))}")
        
        if issues:
            print(f"\n⚠️  Quality Issues Found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"\n✅ No quality issues found!")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ Quality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_jd_quality():
    """Test quality of job description parsing."""
    print("\n" + "="*80)
    print("QUALITY TEST: Job Description Parsing Validation")
    print("="*80)
    
    try:
        llm_client = LLMClient(config)
        extractor = PDFExtractor(require_pdfplumber=False)
        
        txt_file = Path("data/job_descriptions/raw/Senior Cloud Java Engineer.txt")
        if not txt_file.exists():
            txt_file = Path("data/job_descriptions/raw/test_job.txt")
        
        text_data = extractor.extract_text_from_txt_with_metadata(txt_file)
        
        parser = JDParser(use_llm=True, llm_client=llm_client)
        result = parser.parse_from_text(text_data['text'], "quality_test")
        
        is_valid, issues = validate_jd_structure(result)
        
        print(f"\n📊 Job Description Quality Report:")
        print(f"   File: {txt_file.name}")
        print(f"   Valid Structure: {'✅ Yes' if is_valid else '❌ No'}")
        print(f"   Title: {result.get('title', 'N/A')}")
        print(f"   Must-Have Count: {len(result.get('must_have_requirements', []))}")
        print(f"   Nice-to-Have Count: {len(result.get('nice_to_have', []))}")
        print(f"   Experience Required: {result.get('experience_years_required', 'N/A')} years")
        
        if issues:
            print(f"\n⚠️  Quality Issues Found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"\n✅ No quality issues found!")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ Quality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_vs_rules_detailed():
    """Detailed comparison between LLM and rule-based parsing."""
    print("\n" + "="*80)
    print("COMPARISON: LLM vs Rule-based (Detailed)")
    print("="*80)
    
    try:
        llm_client = LLMClient(config)
        extractor = PDFExtractor(require_pdfplumber=False)
        
        txt_file = Path("data/resumes/raw/test_resume.txt")
        text_data = extractor.extract_text_from_txt_with_metadata(txt_file)
        text = text_data['text']
        
        # LLM parsing
        llm_parser = ResumeParser(use_llm=True, llm_client=llm_client)
        llm_result = llm_parser.parse_from_text(text, "llm_comparison")
        llm_valid, llm_issues = validate_resume_structure(llm_result)
        
        # Rule-based parsing
        rule_parser = ResumeParser(use_llm=False)
        rule_result = rule_parser.parse_from_text(text, "rule_comparison")
        rule_valid, rule_issues = validate_resume_structure(rule_result)
        
        print(f"\n📊 Detailed Comparison:")
        print(f"\n{'Aspect':<30} {'LLM-based':<25} {'Rule-based':<25}")
        print("-" * 80)
        print(f"{'Valid Structure':<30} {'✅ Yes' if llm_valid else '❌ No':<25} {'✅ Yes' if rule_valid else '❌ No':<25}")
        print(f"{'Name Extracted':<30} {llm_result.get('name', 'N/A'):<25} {rule_result.get('name', 'N/A'):<25}")
        print(f"{'Email Extracted':<30} {(llm_result.get('email') or 'N/A'):<25} {(rule_result.get('email') or 'N/A'):<25}")
        print(f"{'Phone Extracted':<30} {(llm_result.get('phone') or 'N/A'):<25} {(rule_result.get('phone') or 'N/A'):<25}")
        print(f"{'Skills Count':<30} {len(llm_result.get('skills', [])):<25} {len(rule_result.get('skills', [])):<25}")
        print(f"{'Experience Entries':<30} {len(llm_result.get('experience', [])):<25} {len(rule_result.get('experience', [])):<25}")
        print(f"{'Education Entries':<30} {len(llm_result.get('education', [])):<25} {len(rule_result.get('education', [])):<25}")
        print(f"{'Quality Issues':<30} {len(llm_issues):<25} {len(rule_issues):<25}")
        
        # Show detailed skills comparison
        llm_skills = set(llm_result.get('skills', []))
        rule_skills = set(rule_result.get('skills', []))
        
        print(f"\n📋 Skills Analysis:")
        print(f"   LLM unique skills: {len(llm_skills - rule_skills)}")
        print(f"   Rule-based unique skills: {len(rule_skills - llm_skills)}")
        print(f"   Common skills: {len(llm_skills & rule_skills)}")
        
        if llm_skills - rule_skills:
            print(f"\n   Skills only found by LLM (showing first 10):")
            for skill in list(llm_skills - rule_skills)[:10]:
                print(f"      - {skill}")
        
        # Winner determination
        print(f"\n🏆 Winner:")
        llm_score = sum([
            len(llm_result.get('skills', [])) > len(rule_result.get('skills', [])),
            bool(llm_result.get('email')),
            bool(llm_result.get('phone')),
            len(llm_issues) < len(rule_issues),
            llm_valid
        ])
        
        rule_score = sum([
            len(rule_result.get('skills', [])) > len(llm_result.get('skills', [])),
            bool(rule_result.get('email')),
            bool(rule_result.get('phone')),
            len(rule_issues) < len(llm_issues),
            rule_valid
        ])
        
        if llm_score > rule_score:
            print(f"   ✅ LLM-based parsing (score: {llm_score}/5)")
        elif rule_score > llm_score:
            print(f"   ✅ Rule-based parsing (score: {rule_score}/5)")
        else:
            print(f"   🤝 Tie (both scored {llm_score}/5)")
        
        return True
        
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 LLM PARSING QUALITY VALIDATION SUITE")
    print("="*80)
    
    passed = 0
    failed = 0
    
    if test_resume_quality():
        passed += 1
    else:
        failed += 1
    
    if test_jd_quality():
        passed += 1
    else:
        failed += 1
    
    if test_llm_vs_rules_detailed():
        passed += 1
    else:
        failed += 1
    
    print("\n" + "="*80)
    print("📊 QUALITY TEST SUMMARY")
    print("="*80)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL QUALITY TESTS PASSED!")
    
    sys.exit(0 if failed == 0 else 1)
