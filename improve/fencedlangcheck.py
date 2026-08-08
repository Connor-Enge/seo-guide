import os
import re

def audit_fenced_lang(out_dir: str) -> list[dict]:
    defects = []
    pattern = re.compile(r'<pre\b[^>]*>\s*(<code\b[^>]*>)', re.IGNORECASE)
    for root, _, files in os.walk(out_dir):
        for file_name in files:
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    for match in pattern.finditer(content):
                        code_tag = match.group(1)
                        if not re.search(r'language-[A-Za-z0-9+#._-]', code_tag):
                            defects.append({
                                'page': os.path.relpath(file_path).replace('\\', '/'),
                                'kind': 'fenced_code_missing_lang',
                                'detail': 'a <pre><code> code block has no non-empty language-* class (unlabeled fence)',
                                'severity': 'error'
                            })
    return defects
