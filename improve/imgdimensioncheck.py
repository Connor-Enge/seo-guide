"""
Images without intrinsic width/height cause cumulative layout shift (CLS), a page-experience signal.
"""

import os
import re

def audit_img_dimensions(out_dir: str) -> list[dict]:
    problems = []
    img_tag_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
    width_attr_re = re.compile(r'(?i)\bwidth\s*=', re.IGNORECASE)
    height_attr_re = re.compile(r'(?i)\bheight\s*=', re.IGNORECASE)

    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    img_tags = img_tag_re.findall(content)
                    for tag in img_tags:
                        if not width_attr_re.search(tag) or not height_attr_re.search(tag):
                            problem = {
                                'page': os.path.relpath(full_path, out_dir).replace('\\', '/'),
                                'kind': 'img_missing_dimensions',
                                'detail': f"missing {'width' if not width_attr_re.search(tag) else 'height'}, {'height' if not height_attr_re.search(tag) else 'width'} (layout shift / CLS risk): {tag[:120]}",
                                'severity': 'warn'
                            }
                            problems.append(problem)

    return problems
