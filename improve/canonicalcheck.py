import os
import re
from html import unescape

def audit_canonicals(out_dir, base_url):
    problems = []
    seen_urls = set()
    
    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                page_path = os.path.relpath(os.path.join(root, file), out_dir).replace('\\', '/')
                full_path = os.path.join(root, file)
                
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                expected_url = compute_expected_url(base_url, page_path)
                
                canonical_tags = re.findall(r'<link\s+[^>]*rel="canonical"[^>]*href=["\'](.*?)["\'][^>]*>', content)
                num_canonicals = len(canonical_tags)
                
                if num_canonicals == 0:
                    problems.append({'page': page_path, 'kind': 'missing', 'detail': 'no rel=canonical link'})
                elif num_canonicals > 1:
                    problems.append({'page': page_path, 'kind': 'duplicate', 'detail': f'{num_canonicals} canonical tags'})
                else:
                    href = unescape(canonical_tags[0])
                    if href != expected_url:
                        problems.append({'page': page_path, 'kind': 'mismatch', 'detail': f'got {href} expected {expected_url}'})
                
                seen_urls.add(expected_url)
    
    return problems

def compute_expected_url(base_url, relpath):
    base_url = base_url.rstrip('/')
    if os.path.basename(relpath) == 'index.html':
        d = os.path.dirname(relpath).strip('/')
        if not d:
            expected = f'{base_url}/'
        else:
            expected = f'{base_url}/{d}/'
    else:
        expected = f'{base_url}/{relpath}'
    
    return expected
