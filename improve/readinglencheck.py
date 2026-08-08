import os
import re
import json

def audit_reading_length(out_dir):
    problems = []
    script_tag_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    
    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                script_tags = re.findall(script_tag_pattern, content, re.IGNORECASE | re.DOTALL)
                for tag in script_tags:
                    try:
                        payload = json.loads(tag)
                        if isinstance(payload, dict):
                            nodes = [payload] + (payload.get('@graph', []) if '@graph' in payload else [])
                        elif isinstance(payload, list):
                            nodes = payload
                        else:
                            continue
                        
                        for node in nodes:
                            if has_target_type(node) and 'timeRequired' in node:
                                tr = node['timeRequired']
                                wc = node.get('wordCount')
                                
                                if not re.fullmatch(r'^PT\d+M$', tr):
                                    problems.append({
                                        "page": os.path.relpath(file_path, out_dir),
                                        "kind": "timerequired_malformed",
                                        "severity": "error",
                                        "detail": repr(tr)
                                    })
                                    continue
                                
                                if wc is None or not isinstance(wc, int) or wc <= 0:
                                    problems.append({
                                        "page": os.path.relpath(file_path, out_dir),
                                        "kind": "wordcount_invalid",
                                        "severity": "error",
                                        "detail": repr(wc)
                                    })
                                    continue
                                
                                tr_minutes = int(tr[2:-1])
                                expected = max(1, int(round(wc / 220.0)))
                                if tr_minutes != expected:
                                    problems.append({
                                        "page": os.path.relpath(file_path, out_dir),
                                        "kind": "reading_length_mismatch",
                                        "severity": "error",
                                        "detail": f'PT{tr_minutes}M vs {wc} words -> expected PT{expected}M'
                                    })
                    except json.JSONDecodeError:
                        continue
    
    return problems

def has_target_type(node):
    target_types = ['Article', 'BlogPosting']
    node_type = node.get('@type')
    if isinstance(node_type, list):
        return any(t in target_types for t in node_type)
    else:
        return node_type in target_types
