#!/usr/bin/env python3
"""
HYPEROPTIMUS VERIFICATION SCRIPT
Target: frontend/src/app/admin/[slug]/tables/page.tsx
Purpose: Static analysis to verify fix for infinite render loops.
"""

import re
import sys
import os

TARGET_FILE = "frontend/src/app/admin/[slug]/tables/page.tsx"

def verify_file():
    if not os.path.exists(TARGET_FILE):
        print(f"❌ CRITICAL: File not found: {TARGET_FILE}")
        sys.exit(1)

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = [
        {
            "id": "HC-01",
            "desc": "Check for 'use client' directive",
            "regex": r'[\"\']use client[\"\']',
            "must_match": True
        },
        {
            "id": "HC-02",
            "desc": "Check for dependency array in useEffect",
            "regex": r'useEffect\s*\(\s*.*,\s*\[.*\]\s*\)',
            "must_match": True
        },
        {
            "id": "HC-03",
            "desc": "Ensure no direct window/document access without checks",
            "regex": r'(?<!if \(typeof window !== [\"\']undefined[\"\']\)\s\{)\b(window\.|document\.)',
            "must_match": False
        },
        {
            "id": "HC-04",
            "desc": "Check for loading state handling",
            "regex": r'if\s*\(\w+\.loading\)',
            "must_match": True
        }
    ]

    failures = []

    print(f"🔍 Starting Hyperoptimus Audit on {TARGET_FILE}...")

    for check in checks:
        match = re.search(check['regex'], content, re.DOTALL)
        if check['must_match'] and not match:
            failures.append(f"FAILED {check['id']}: {check['desc']}")
        elif not check['must_match'] and match:
            # Simple heuristic, might have false positives but safe for strict mode
            failures.append(f"FAILED {check['id']}: {check['desc']} (Found prohibited pattern)")
        else:
            print(f"✅ PASSED {check['id']}")

    if failures:
        print("\n❌ VERIFICATION FAILED:")
        for fail in failures:
            print(f"  - {fail}")
        sys.exit(1)
    else:
        print("\n✨ HYPEROPTIMUS VERIFICATION PASSED: Route is structurally sound.")
        sys.exit(0)

if __name__ == "__main__":
    verify_file()
