import os
import xml.etree.ElementTree as ET

def audit_sitemap(out_dir, base_url):
    problems = []
    sitemap_path = os.path.join(out_dir, 'sitemap.xml')
    
    try:
        tree = ET.parse(sitemap_path)
    except (ET.ParseError, OSError, FileNotFoundError) as err:
        return [{'kind': 'malformed_xml', 'loc': '', 'detail': str(err), 'severity': 'error'}]
    
    locs = set()
    for elem in tree.iter():
        if elem.tag.endswith('}loc'):
            loc_text = (elem.text or '').strip()
            if loc_text:
                if not loc_text.startswith(base_url):
                    problems.append({'kind': 'nonabsolute_loc', 'loc': loc_text, 'detail': loc_text, 'severity': 'error'})
                rel_path = loc_text[len(base_url):]
                if rel_path.startswith('/'):
                    rel_path = rel_path[1:]
                if rel_path == '' or rel_path.endswith('/'):
                    rel_path += 'index.html'
                file_path = os.path.join(out_dir, rel_path.replace('/', os.sep))
                if rel_path == '404.html' or rel_path.endswith('/404.html'):
                    problems.append({'kind': 'listed_404', 'loc': loc_text, 'detail': loc_text, 'severity': 'error'})
                elif not os.path.isfile(file_path):
                    problems.append({'kind': 'dangling_loc', 'loc': '', 'detail': file_path, 'severity': 'error'})
                if loc_text in locs:
                    problems.append({'kind': 'duplicate_loc', 'loc': loc_text, 'detail': loc_text, 'severity': 'error'})
                else:
                    locs.add(loc_text)
    
    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html') and file != '404.html':
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, out_dir).replace(os.sep, '/')
                b = base_url.rstrip('/')
                if os.path.basename(rel_path) == 'index.html':
                    d = os.path.dirname(rel_path).strip('/')
                    url = b + '/' if d == '' else b + '/' + d + '/'
                else:
                    url = b + '/' + rel_path
                if url not in locs:
                    problems.append({'kind': 'orphan_from_sitemap', 'loc': url, 'detail': 'indexable page absent from sitemap', 'severity': 'warn'})
    
    return problems
