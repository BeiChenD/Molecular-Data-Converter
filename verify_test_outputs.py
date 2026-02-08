#!/usr/bin/env python3
"""
Quick Verification Script
=========================
Verifies that all test output files were created correctly.

Author: Bei Chen
Date: February 8, 2026
"""

import os
import sys

def verify_test_outputs():
    """Verify all expected test output files exist."""
    
    print("="*70)
    print("VERIFYING TEST OUTPUT FILES")
    print("="*70)
    
    expected_files = {
        'quick_test_output/test.xyz': 'XYZ coordinate file',
        'quick_test_output/test.csv': 'CSV coordinate file',
        'quick_test_output/structure_frame_0.png': '3D structure plot',
        'quick_test_output/elemental_distribution_analysis.png': 'RDF analysis plot',
        'quick_test_output/elemental_analysis_summary.txt': 'Statistical summary'
    }
    
    all_exist = True
    
    for filepath, description in expected_files.items():
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"\n[OK] {description}")
            print(f"     File: {filepath}")
            print(f"     Size: {size:,} bytes ({size/1024:.1f} KB)")
        else:
            print(f"\n[MISSING] {description}")
            print(f"          File: {filepath}")
            all_exist = False
    
    print("\n" + "="*70)
    if all_exist:
        print("[SUCCESS] All test output files verified!")
        print("="*70)
        return 0
    else:
        print("[ERROR] Some test files are missing!")
        print("="*70)
        return 1

if __name__ == "__main__":
    sys.exit(verify_test_outputs())
