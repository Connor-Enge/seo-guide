import os
import re

def audit_script_src(docs_dir, base_url=None):
    problems = []
    script_tag_re = re.compile(r'<script\s+(?:[^>]*?\s+)?src=["\'](.*?)["\'][^>]*>')
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.html'):
                html_path = os.path.join(root, file)
                with open(html_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for match in script_tag_re.finditer(content):
                    src = match.group(1)
                    if '?query' in src or '#fragment' in src:
                        src = src.split('?')[0].split('#')[0]
                    
                    if '/assets/' in src:
                        local_path = os.path.normpath(os.path.join(docs_dir, 'assets', src.split('/assets/')[-1]))
                        if not os.path.isfile(local_path):
                            problems.append({
                                "kind": "script_src_missing",
                                "page": html_path[len(docs_dir):].lstrip('/').replace('\\', '/'),
                                "detail": f"references {src} but assets/{os.path.basename(src)} is missing from docs/assets/"
                            })
    
    return sorted(problems, key=lambda x: (x['page'], x['detail']))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scriptsrccheck.py <docs_dir>")
        sys.exit(1)
    
    docs_dir = sys.argv[1]
    problems = audit_script_src(docs_dir)
    for prob in problems:
        print(prob)
