import os
import re
import json

def audit_jsonld_refs(out_dir, base_url=None) -> list[dict]:
    """
    Audit JSON-LD references in HTML files within out_dir.
    
    :param out_dir: Directory containing HTML files to audit.
    :param base_url: Ignored; for signature compatibility only.
    :return: List of problem dictionaries with keys 'page', 'kind', 'severity', and 'detail'.
    """
    problems = []
    ref_properties = {'author', 'publisher', 'isPartOf', 'about', 'mainEntity', 'mainEntityOfPage'}
    
    def is_reference(obj):
        return isinstance(obj, dict) and '@id' in obj and '@type' not in obj
    
    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                script_blocks = re.findall(r'<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
                nodes = []
                for block in script_blocks:
                    try:
                        payload = json.loads(block)
                        if isinstance(payload, dict) and '@graph' in payload:
                            nodes.extend(payload['@graph'])
                        elif isinstance(payload, dict):
                            nodes.append(payload)
                        elif isinstance(payload, list):
                            nodes.extend(item for item in payload if isinstance(item, dict))
                    except json.JSONDecodeError:
                        continue
                
                defined_ids = set()
                def collect_defined_ids(node):
                    if '@id' in node and '@type' in node and isinstance(node['@id'], str):
                        defined_ids.add(node['@id'])
                    for key, value in node.items():
                        if isinstance(value, dict):
                            collect_defined_ids(value)
                        elif isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict):
                                    collect_defined_ids(item)
                for node in nodes:
                    collect_defined_ids(node)
                
                for node in nodes:
                    for prop in ref_properties:
                        if prop in node:
                            candidates = [item for item in (node[prop] if isinstance(node[prop], list) else [node[prop]]) if is_reference(item)]
                            for candidate in candidates:
                                if candidate['@id'] not in defined_ids:
                                    problems.append({
                                        'page': os.path.relpath(file_path, out_dir).replace(os.sep, '/'),
                                        'kind': 'dangling_ref',
                                        'severity': 'error',
                                        'detail': f"{prop} -> {candidate['@id']} not defined in page graph"
                                    })
    
    return problems
