import os
import re
from html import unescape

def audit_meta(out_dir, max_title_chars=60, max_desc_chars=155):
    problems = []
    title_texts = {}
    desc_texts = {}

    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                page = os.path.relpath(full_path, out_dir).replace(chr(92), '/')
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                title_matches = re.findall(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
                if len(title_matches) == 0:
                    problems.append({'page': page, 'kind': 'missing_title', 'severity': 'error', 'detail': 'no <title> tag'})
                elif len(title_matches) > 1:
                    problems.append({'page': page, 'kind': 'multiple_title', 'severity': 'error', 'detail': f'{len(title_matches)} <title> tags'})
                else:
                    title_text = unescape(title_matches[0]).strip()
                    if title_text == '':
                        problems.append({'page': page, 'kind': 'empty_title', 'severity': 'warn', 'detail': 'empty <title>'})
                    elif len(title_text) > max_title_chars:
                        problems.append({'page': page, 'kind': 'long_title', 'severity': 'warn', 'detail': f'{len(title_text)} chars (max {max_title_chars})'})
                    else:
                        title_texts[title_text] = title_texts.get(title_text, []) + [page]

                desc_matches = re.findall(r'<meta\s+name="description"\s+content="(.*?)">', content, re.IGNORECASE | re.DOTALL)
                if len(desc_matches) == 0:
                    problems.append({'page': page, 'kind': 'missing_description', 'severity': 'error', 'detail': 'no <meta name=description>'})
                elif len(desc_matches) > 1:
                    problems.append({'page': page, 'kind': 'multiple_description', 'severity': 'error', 'detail': f'{len(desc_matches)} meta description tags'})
                else:
                    desc_text = unescape(desc_matches[0]).strip()
                    if desc_text == '':
                        problems.append({'page': page, 'kind': 'empty_description', 'severity': 'warn', 'detail': 'empty meta description'})
                    elif len(desc_text) > max_desc_chars:
                        problems.append({'page': page, 'kind': 'long_description', 'severity': 'warn', 'detail': f'{len(desc_text)} chars (max {max_desc_chars})'})
                    else:
                        desc_texts[desc_text] = desc_texts.get(desc_text, []) + [page]

    for title_text, pages in title_texts.items():
        if len(pages) > 1:
            for page in pages:
                problems.append({'page': page, 'kind': 'duplicate_title', 'severity': 'warn', 'detail': f'title also used on: {", ".join(sorted(set(pages) - {page}))}'})
    
    for desc_text, pages in desc_texts.items():
        if len(pages) > 1:
            for page in pages:
                problems.append({'page': page, 'kind': 'duplicate_description', 'severity': 'warn', 'detail': f'description also used on: {", ".join(sorted(set(pages) - {page}))}'})
    
    return problems
