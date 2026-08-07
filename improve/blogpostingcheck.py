import os
import re
import json

def audit_blog_posting(out_dir, base_url=None):
    """
    Audit blog posts for missing or incomplete BlogPosting data.
    
    Returns a list of problem dicts with keys: kind, page, detail, severity.
    """
    problems = []
    blog_dir = os.path.join(out_dir, 'blog')
    
    if not os.path.exists(blog_dir):
        return problems
    
    post_pages = sorted([os.path.join(root, 'index.html') for root, _, files in os.walk(blog_dir) if 'index.html' in files and root != blog_dir])
    
    for page in post_pages:
        with open(page, 'r', encoding='utf-8') as f:
            html = f.read()
        
        script_blocks = re.findall(r'<script\s+type="application/ld\+json"[^>]*>([\s\S]*?)<\/script>', html, re.IGNORECASE | re.DOTALL)
        parsed_blocks = []
        
        for block in script_blocks:
            try:
                parsed_block = json.loads(block)
                parsed_blocks.append(parsed_block)
            except json.JSONDecodeError:
                problems.append({
                    'kind': 'json_decode_error',
                    'page': os.path.relpath(page, out_dir),
                    'detail': 'Failed to decode JSON-LD block',
                    'severity': 'error'
                })
        
        blog_posting_node = None
        
        for block in parsed_blocks:
            if isinstance(block, dict):
                nodes = [block] + (block.get('@graph', []) if '@graph' in block else [])
                for node in nodes:
                    if isinstance(node, dict) and ('@type' in node and 'BlogPosting' in node['@type']):
                        blog_posting_node = node
                        break
            if blog_posting_node:
                break
        
        if not blog_posting_node:
            problems.append({
                'kind': 'missing_blogposting',
                'page': os.path.relpath(page, out_dir),
                'detail': 'No BlogPosting found in JSON-LD blocks',
                'severity': 'error'
            })
            continue
        
        required_fields = ['headline', 'datePublished', 'dateModified', 'author']
        missing_fields = [field for field in required_fields if not blog_posting_node.get(field) or (isinstance(blog_posting_node[field], str) and blog_posting_node[field].strip() == '')]
        
        if missing_fields:
            problems.append({
                'kind': 'incomplete_blogposting',
                'page': os.path.relpath(page, out_dir),
                'detail': f'BlogPosting missing/empty: {", ".join(missing_fields)}',
                'severity': 'error'
            })
    
    return problems
