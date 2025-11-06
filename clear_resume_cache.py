"""Force reprocessing of resumes by clearing cache entries."""
import json
from pathlib import Path

cache_file = Path("data/cache/processed_files.json")

if cache_file.exists():
    with open(cache_file, 'r') as f:
        cache = json.load(f)
    
    # Remove only resume entries
    keys_to_remove = [k for k in cache.keys() if "resumes\\raw" in k]
    
    print(f"Removing {len(keys_to_remove)} resume entries from cache:")
    for key in keys_to_remove:
        print(f"  - {Path(key).name}")
        del cache[key]
    
    # Save updated cache
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=2)
    
    print(f"\n✅ Cache updated. {len(cache)} entries remaining (job descriptions)")
else:
    print("❌ Cache file not found")
