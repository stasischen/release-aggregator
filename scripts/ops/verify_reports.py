import re

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Pattern to find Korean code blocks/inline code with Chinese characters
    # Example: `사話`
    corrupted_pattern = re.compile(r'`[^`]*[\u4E00-\u9FFF][^`]*`')
    
    for i, line in enumerate(lines):
        matches = corrupted_pattern.findall(line)
        if matches:
            # We want to allow Chinese in translations (which are in parentheses)
            # but NOT inside the backticks which typically represent Korean strings.
            print(f"Line {i+1}: {line.strip()}")
            print(f"  Possible corruption: {matches}")

print("Checking PILOT_EXTRACTION_NOTE.md...")
check_file(r"f:\Githubs\lingo\release-aggregator\docs\tasks\KNOWLEDGE_LAB_ENRICHMENT_PILOT_EXTRACTION_NOTE.md")
print("\nChecking MANIFEST.md...")
check_file(r"f:\Githubs\lingo\release-aggregator\docs\tasks\KNOWLEDGE_LAB_ENRICHMENT_EXTRACT_READY_MANIFEST.md")
