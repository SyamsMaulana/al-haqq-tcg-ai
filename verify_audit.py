



import os

def audit_files():
    total = 0
    passed = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                total += 1
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                has_schema = "application/ld+json" in content
                has_watermark = "Al-Haqq Protocol" in content
                
                if has_schema and has_watermark:
                    passed += 1
                    print(f"[PASS] {filepath}")
                else:
                    print(f"[FAIL] {filepath} (Schema: {has_schema}, Watermark: {has_watermark})")

    print(f"\nAudit Complete: {passed}/{total} files fully compliant with Al-Haqq Protocol.")

if __name__ == "__main__":
    audit_files()


