import os
import re
from html import unescape
from urllib.parse import unquote

def audit_fragments(out_dir, base_url):
    page_ids = {}
    
    # Step 1: Collect anchor ids for every page
    for root, _, files in os.walk(out_dir):
        for name in files:
            if name.endswith(".html"):
                full = os.path.join(root, name)
                rel = os.path.relpath(full, out_dir).replace("\\", "/")
                try:
                    text = open(full, encoding="utf-8").read()
                except Exception as e:
                    text = open(full, encoding="utf-8", errors="ignore").read()
                ids = set(re.findall(r'id=["\047]([^"\047]+)["\047]', text)) | set(re.findall(r'name=["\047]([^"\047]+)["\047]', text))
                page_ids[rel] = ids
    
    # Step 2: Check every link
    problems = []
    for root, _, files in os.walk(out_dir):
        for name in files:
            if name.endswith(".html"):
                full = os.path.join(root, name)
                rel = os.path.relpath(full, out_dir).replace("\\", "/")
                text = open(full, encoding="utf-8").read()
                for href in re.findall(r'href=["\047](.*?)["\047]', text):
                    h = unescape(href)  # the raw matched string
                    if h.startswith("#"):
                        target_rel = rel  # same page
                        fragment = h[1:]
                    elif h.startswith(base_url) and "#" in h:
                        remainder = h[len(base_url):]
                        path_part, fragment = remainder.split("#", 1)  # split ONCE
                        path_part = path_part.split("?")[0]
                        if path_part.endswith("/"):
                            path_part += "index.html"
                        target_rel = path_part.lstrip("/").replace("\\", "/")
                    else:
                        continue  # skip everything else
                    fragment = unquote(fragment)
                    if fragment == "" or fragment == "top":
                        continue  # browser-reserved, no element needed
                    if target_rel not in page_ids:
                        continue  # missing target page is a different audit's job
                    if fragment not in page_ids[target_rel]:
                        problems.append({
                            "page": rel,
                            "href": h,
                            "kind": "dangling-fragment",
                            "detail": "#" + fragment + " not found in " + target_rel,
                        })
    return problems
