import os
import re
import glob

def audit_h1(out_dir: str) -> list[dict]:
    problems = []
    h1_pattern = re.compile(r'<h1(?:\s[^>]*)?>', re.IGNORECASE)
    
    for root, _, files in sorted(os.walk(out_dir)):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                h1_count = len(h1_pattern.findall(content))
                if h1_count != 1:
                    problems.append({
                        'page': os.path.relpath(full_path, out_dir),
                        'count': h1_count,
                        'detail': 'expected exactly one <h1>, found {}'.format(h1_count)
                    })
    
    return problems
