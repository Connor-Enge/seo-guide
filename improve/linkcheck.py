import os
import re
from html import unescape

def audit_internal_links(out_dir, base_url):
    problems = []
    
    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                page_path = os.path.relpath(os.path.join(root, file), out_dir).replace('\\', '/')
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                
                href_pattern = re.compile(r'href=["\'](.*?)["\']')
                for match in href_pattern.findall(content):
                    unescaped_href = unescape(match)
                    
                    if not unescaped_href or unescaped_href.startswith('#'):
                        continue
                    elif unescaped_href.startswith(('mailto:', 'tel:', 'javascript:', 'data:')):
                        continue
                    elif unescaped_href.startswith('//'):
                        continue
                    elif re.match(r'^https?://', unescaped_href):
                        if not unescaped_href.startswith(base_url):
                            continue
                        else:
                            remainder = unescaped_href[len(base_url):].split('#')[0].split('?')[0]
                            target_path = os.path.join(out_dir, remainder.lstrip('/'))
                            if remainder.endswith('/') and not os.path.exists(target_path + 'index.html'):
                                problems.append({
                                    'page': page_path,
                                    'href': unescaped_href,
                                    'kind': 'dangling',
                                    'detail': f"Missing index.html for {remainder}"
                                })
                            elif not os.path.exists(target_path):
                                problems.append({
                                    'page': page_path,
                                    'href': unescaped_href,
                                    'kind': 'dangling',
                                    'detail': f"Missing file or directory: {remainder}"
                                })
                    else:
                        problems.append({
                            'page': page_path,
                            'href': unescaped_href,
                            'kind': 'root-relative',
                            'detail': "Root-relative links are not allowed"
                        })
    
    return problems
