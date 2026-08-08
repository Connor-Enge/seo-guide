import os
import re

def audit_fenced_code(out_dir: str) -> list[dict]:
    problems = []
    pattern = re.compile(r'<pre[^>]*>.*?</pre>', re.IGNORECASE | re.DOTALL)
    tag_pattern = re.compile(r'<\s*(script|meta|link|img)\b', re.IGNORECASE)

    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for match in pattern.finditer(content):
                        code_block = match.group(0)
                        if tag_pattern.search(code_block):
                            problems.append({
                                'page': os.path.relpath(file_path).replace('\\', '/'),
                                'kind': 'fenced_code_real_tag',
                                'detail': f'real <{tag_pattern.findall(code_block)[0]}> tag inside a <pre><code> block',
                                'severity': 'error'
                            })

    return problems
