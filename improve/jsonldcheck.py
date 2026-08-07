import os
import re
import json

def audit_jsonld(out_dir, base_url):
    problems = []
    pattern = r'<script[^>]*type=[\"\']application/ld\\+json[\"\'][^>]*>(.*?)</script>'
    
    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                page_id = os.path.relpath(os.path.join(root, file), out_dir).replace(os.sep, '/')
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                    if not matches:
                        continue
                    nodes = []
                    for match in matches:
                        try:
                            payload = json.loads(match)
                        except json.JSONDecodeError as err:
                            problems.append({'page': page_id, 'kind': 'invalid_json', 'severity': 'error', 'detail': str(err)})
                            continue
                        if isinstance(payload, dict) and '@graph' in payload:
                            nodes.extend(payload['@graph'])
                        elif isinstance(payload, dict):
                            nodes.append(payload)
                        elif isinstance(payload, list):
                            nodes.extend(payload)
                    
                    if not nodes:
                        continue
                    
                    core_types = ['Organization', 'WebSite', 'Person']
                    for core_type in core_types:
                        if any(node.get('@type') == core_type or (isinstance(node.get('@type'), list) and core_type in node['@type']) for node in nodes):
                            continue
                        problems.append({'page': page_id, 'kind': f'missing_{core_type.lower()}', 'severity': 'error', 'detail': f'Missing {core_type}'})
                    
                    for node in nodes:
                        if '@id' in node and isinstance(node['@id'], str):
                            if not node['@id'].startswith(base_url) or node['@id'].startswith('/'):
                                problems.append({'page': page_id, 'kind': 'nonabsolute_id', 'severity': 'error', 'detail': f'Non-absolute @id: {node["@id"]}'})
                        if 'url' in node and isinstance(node['url'], str):
                            if not node['url'].startswith(base_url) or node['url'].startswith('/'):
                                problems.append({'page': page_id, 'kind': 'nonabsolute_url', 'severity': 'error', 'detail': f'Non-absolute url: {node["url"]}'})
    
    absolute_ids = {}
    for problem in problems:
        if problem['kind'] in ['missing_organization', 'missing_website', 'missing_person']:
            continue
        if isinstance(problem['detail'], str) and problem['detail'].startswith(base_url) and not problem['detail'].startswith('/'):
            core_type = problem['kind'].replace('nonabsolute_', '').replace('_id', '')
            if core_type not in absolute_ids:
                absolute_ids[core_type] = {}
            absolute_ids[core_type][problem['page']] = problem['detail']
    
    for core_type, page_ids in absolute_ids.items():
        canonical_id = sorted(page_ids.values()).count(max(set(page_ids.values()), key=page_ids.values().count))
        if canonical_id != 1:
            canonical_id = min(sorted(page_ids.values()))
        for page_id, id_value in page_ids.items():
            if id_value != canonical_id:
                problems.append({'page': page_id, 'kind': f'inconsistent_{core_type.lower()}_id', 'severity': 'error', 'detail': f'Inconsistent {core_type} id: {id_value}, expected {canonical_id}'})
    
    return problems
