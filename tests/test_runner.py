#!/usr/bin/env python3
"""
Automated Test Runner
=====================

This script runs all lab solutions and verifies they work.
Used by MiniMax for automated verification.
"""

import subprocess
import sys
from pathlib import Path

def run_test(lab_path: Path, lab_name: str) -> dict:
    """Run a single lab test."""
    print(f"\n{'='*50}")
    print(f"Testing: {lab_name}")
    print(f"{'='*50}")
    
    solution = lab_path / "solution.py"
    if not solution.exists():
        return {"name": lab_name, "status": "SKIP", "error": "No solution.py"}
    
    try:
        # Run the solution
        result = subprocess.run(
            [sys.executable, str(solution)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return {
                "name": lab_name,
                "status": "PASS",
                "output": result.stdout
            }
        else:
            return {
                "name": lab_name,
                "status": "FAIL",
                "error": result.stderr,
                "output": result.stdout
            }
    except subprocess.TimeoutExpired:
        return {"name": lab_name, "status": "TIMEOUT", "error": "Test took too long"}
    except Exception as e:
        return {"name": lab_name, "status": "ERROR", "error": str(e)}

def main():
    print("LangGraph 100 Essentials - Test Runner")
    print("=" * 50)
    
    labs_dir = Path(__file__).parent / "labs"
    results = []
    
    # Test each lab
    for lab_num in range(1, 6):
        lab_path = labs_dir / f"Lab{lab_num}"
        result = run_test(lab_path, f"Lab{lab_num}")
        results.append(result)
    
    # Summary
    print("\n" + "=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    errors = sum(1 for r in results if r["status"] in ("ERROR", "TIMEOUT"))
    
    for r in results:
        status_icon = "✓" if r["status"] == "PASS" else "✗" if r["status"] == "FAIL" else "○"
        print(f"{status_icon} {r['name']}: {r['status']}")
    
    print(f"\nPassed: {passed}/{len(results)}")
    print(f"Failed: {failed}/{len(results)}")
    print(f"Errors: {errors}/{len(results)}")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
