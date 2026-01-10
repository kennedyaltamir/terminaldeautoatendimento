import os
import sys

def verify():
    print("🔍 Verifying GTM Readiness Checklist...")
    target_file = "docs/GTM_CHECKLIST.md"
    
    if not os.path.exists(target_file):
        print(f"❌ File not found: {target_file}")
        sys.exit(1)
        
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    required_sections = [
        "Infrastructure & Resilience",
        "Observability & Monitoring",
        "Mobile & Distribution",
        "Compliance & Legal",
        "Fintech Integrity",
        "Security Hardening"
    ]
    
    for section in required_sections:
        if section not in content:
            print(f"❌ Missing section: {section}")
            sys.exit(1)
            
    print("✅ GTM Checklist generated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    verify()