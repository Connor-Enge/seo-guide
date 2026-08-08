import os
import xml.etree.ElementTree as ET

def audit_lastmod_honesty(out_dir):
    sitemap_path = os.path.join(out_dir, 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        return []

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
    except (ET.ParseError, FileNotFoundError):
        return []

    present = []
    for elem in root.iter():
        if elem.tag.endswith('lastmod'):
            lastmod_text = elem.text.strip() if elem.text else ''
            if lastmod_text:
                present.append(lastmod_text)

    if len(present) >= 2 and len(set(present)) == 1:
        shared_date = present[0]
        return [{'kind': 'lastmod_all_identical', 'loc': '', 'detail': f"all {len(present)} <lastmod> values are identical ({shared_date}); Google discounts sitemaps whose lastmod is always the same/today", 'severity': 'warn'}]
    else:
        return []
