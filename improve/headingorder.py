import os
import re

def audit_heading_order(out_dir: str) -> list[dict]:
    results = []
    for root, _, files in sorted(os.walk(out_dir)):
        for file in sorted([f for f in files if f.endswith('.html')]):
            full_path = os.path.join(root, file)
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            headings = re.findall(r'<h([1-6])(?:\s[^>]*)?>', content, re.IGNORECASE)
            prev_level = None
            for level in map(int, headings):
                if prev_level is not None and level > prev_level + 1:
                    results.append({
                        'page': os.path.relpath(full_path, out_dir),
                        'kind': 'skipped_heading_level',
                        'severity': 'warn',
                        'detail': f'heading level jumps from h{prev_level} to h{level} (skips h{prev_level+1})'
                    })
                prev_level = level
    return results
