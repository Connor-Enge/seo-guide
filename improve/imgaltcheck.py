import os
import re

def audit_img_alt(out_dir: str) -> list[dict]:
    TAG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
    ALT_RE = re.compile(r'(?i)\balt\s*=')
    problems = []
    
    for root, _, files in os.walk(out_dir):
        for name in files:
            if not name.endswith('.html'):
                continue
            with open(os.path.join(root, name), 'r', encoding='utf-8') as f:
                content = f.read()
                for m in TAG_RE.finditer(content):
                    tag = m.group(0)
                    if not ALT_RE.search(tag):
                        problems.append({
                            'page': os.path.relpath(os.path.join(root, name), out_dir).replace('\\', '/'),
                            'kind': 'img_missing_alt',
                            'detail': '<img> missing alt attribute: ' + tag[:120],
                            'severity': 'error'
                        })
    
    return problems
