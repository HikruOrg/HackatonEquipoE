"""Verify system status - resumes and job descriptions."""
from pathlib import Path
import json

def count_files_in_dir(directory: Path, extension: str = "") -> int:
    """Count files in directory with optional extension filter."""
    if not directory.exists():
        return 0
    if extension:
        return len(list(directory.glob(f"*{extension}")))
    return len([f for f in directory.iterdir() if f.is_file()])

print("\n" + "="*70)
print("📊 SYSTEM STATUS REPORT")
print("="*70)

# Raw files
print("\n📁 RAW FILES:")
resumes_raw = Path("data/resumes/raw")
jd_raw = Path("data/job_descriptions/raw")

print(f"   Resumes (raw):")
print(f"      PDF: {count_files_in_dir(resumes_raw, '.pdf')}")
print(f"      JSON: {count_files_in_dir(resumes_raw, '.json')}")
print(f"      TXT: {count_files_in_dir(resumes_raw, '.txt')}")
print(f"      TOTAL: {count_files_in_dir(resumes_raw)}")

print(f"\n   Job Descriptions (raw):")
print(f"      PDF: {count_files_in_dir(jd_raw, '.pdf')}")
print(f"      JSON: {count_files_in_dir(jd_raw, '.json')}")
print(f"      TXT: {count_files_in_dir(jd_raw, '.txt')}")
print(f"      TOTAL: {count_files_in_dir(jd_raw)}")

# Processed files
print("\n📦 PROCESSED FILES (Storage):")
resumes_storage = Path("data/storage/resumes")
jd_storage = Path("data/storage/job_descriptions")

resume_count = count_files_in_dir(resumes_storage)
jd_count = count_files_in_dir(jd_storage)

print(f"   Resumes: {resume_count}")
print(f"   Job Descriptions: {jd_count}")

# Processing cache
print("\n🔖 PROCESSING CACHE:")
cache_file = Path("data/cache/processed_files.json")
if cache_file.exists():
    with open(cache_file, 'r') as f:
        cache = json.load(f)
    
    resume_cache = len([k for k in cache.keys() if "resumes\\raw" in k or "resumes/raw" in k])
    jd_cache = len([k for k in cache.keys() if "job_descriptions\\raw" in k or "job_descriptions/raw" in k])
    
    print(f"   Cached resumes: {resume_cache}")
    print(f"   Cached job descriptions: {jd_cache}")
    print(f"   Total cached: {len(cache)}")
else:
    print("   ⚠️  Cache file not found")

# Status
print("\n✅ STATUS:")
raw_total = count_files_in_dir(resumes_raw)
processed_total = resume_count

if raw_total == processed_total:
    print(f"   ✅ All resumes processed ({processed_total}/{raw_total})")
else:
    print(f"   ⚠️  Pending resumes: {raw_total - processed_total}")
    print(f"      Processed: {processed_total}/{raw_total}")

raw_jd_total = count_files_in_dir(jd_raw)
if raw_jd_total == jd_count:
    print(f"   ✅ All job descriptions processed ({jd_count}/{raw_jd_total})")
else:
    print(f"   ⚠️  Pending job descriptions: {raw_jd_total - jd_count}")
    print(f"      Processed: {jd_count}/{raw_jd_total}")

print("\n" + "="*70)
