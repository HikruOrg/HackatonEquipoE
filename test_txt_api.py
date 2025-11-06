"""Quick test to verify TXT support through the API."""
import requests
import sys
from pathlib import Path

def test_txt_upload():
    """Test uploading TXT files through API."""
    
    print("=" * 60)
    print("Testing TXT File Upload through API")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/")
        print(f"\n✓ Backend server is running: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Backend server is not running!")
        print("Please start the server with: python run_server.py")
        return False
    
    # Test 1: Upload job description TXT
    print("\n" + "=" * 60)
    print("Test 1: Upload Job Description TXT")
    print("=" * 60)
    
    jd_file = Path("data/job_descriptions/raw/test_job.txt")
    if not jd_file.exists():
        print(f"❌ Test file not found: {jd_file}")
        return False
    
    try:
        with open(jd_file, "rb") as f:
            files = {"file": (jd_file.name, f, "text/plain")}
            response = requests.post(
                "http://localhost:8000/api/upload/job-description",
                files=files
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Job description uploaded successfully!")
            print(f"  Filename: {data.get('filename')}")
            print(f"  Type: {data.get('type')}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading JD: {e}")
        return False
    
    # Test 2: Upload resume TXT
    print("\n" + "=" * 60)
    print("Test 2: Upload Resume TXT")
    print("=" * 60)
    
    resume_file = Path("data/resumes/raw/test_resume.txt")
    if not resume_file.exists():
        print(f"❌ Test file not found: {resume_file}")
        return False
    
    try:
        with open(resume_file, "rb") as f:
            files = {"files": (resume_file.name, f, "text/plain")}
            response = requests.post(
                "http://localhost:8000/api/upload/resumes",
                files=files
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Resume uploaded successfully!")
            print(f"  Uploaded: {data.get('uploaded')}")
            print(f"  Files: {len(data.get('files', []))}")
            if data.get('files'):
                print(f"  First file type: {data['files'][0].get('type')}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading resume: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ All API tests passed!")
    print("=" * 60)
    print("\nTXT file upload is working correctly through the API!")
    print("You can now use .txt files in the frontend application.")
    
    return True


if __name__ == "__main__":
    success = test_txt_upload()
    sys.exit(0 if success else 1)
