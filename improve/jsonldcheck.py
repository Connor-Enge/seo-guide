import os
import re
import json
from collections import Counter

def audit_jsonld(out_dir, base_url):
    problems = []
    id_maps = {"Organization": {}, "WebSite": {}, "Person": {}}

    def has_type(node, T):
        tt = node.get("@type")
        return tt == T or (isinstance(tt, list) and T in tt)

    def is_absolute(v):
        return isinstance(v, str) and v.startswith(base_url)

    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith(".html"):
                fullpath = os.path.join(root, file)
                page = os.path.relpath(fullpath, out_dir).replace(os.sep, "/")
                with open(fullpath, "r", encoding="utf-8") as f:
                    content = f.read()
                matches = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
                nodes = []
                for match in matches:
                    try:
                        payload = json.loads(match)
                        if isinstance(payload, dict) and "@graph" in payload:
                            nodes.extend([n for n in payload["@graph"] if isinstance(n, dict)])
                        elif isinstance(payload, dict):
                            nodes.append(payload)
                        elif isinstance(payload, list):
                            nodes.extend([n for n in payload if isinstance(n, dict)])
                    except json.JSONDecodeError as e:
                        problems.append({"page": page, "kind": "invalid_json", "severity": "error", "detail": str(e)})
                if not nodes:
                    continue
                for node in nodes:
                    if node.get("@id") is not None and not is_absolute(node["@id"]):
                        problems.append({"page": page, "kind": "nonabsolute_id", "severity": "error", "detail": node["@id"]})
                    if node.get("url") is not None and not is_absolute(node["url"]):
                        problems.append({"page": page, "kind": "nonabsolute_url", "severity": "error", "detail": node["url"]})
                for T, kind in [("Organization", "missing_organization"), ("WebSite", "missing_website"), ("Person", "missing_person")]:
                    if not any(has_type(n, T) for n in nodes):
                        problems.append({"page": page, "kind": kind, "severity": "error", "detail": "missing " + T})
                for T in ["Organization", "WebSite", "Person"]:
                    for node in nodes:
                        if has_type(node, T) and isinstance(node.get("@id"), str) and is_absolute(node["@id"]):
                            id_maps[T][page] = node["@id"]
                            break
    for T in ["Organization", "WebSite", "Person"]:
        if len(id_maps[T]) > 1:
            canonical = Counter(id_maps[T].values()).most_common(1)[0][0]
            for page, idval in id_maps[T].items():
                if idval != canonical:
                    problems.append({"page": page, "kind": "inconsistent_" + T.lower() + "_id", "severity": "error", "detail": idval + " (expected " + canonical + ")"})
    return problems
