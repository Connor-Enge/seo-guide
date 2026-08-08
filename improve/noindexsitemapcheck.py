import os
import re
import xml.etree.ElementTree as ET
from tempfile import TemporaryDirectory

def audit_noindex_sitemap(out_dir, base_url):
    problems = []
    sitemap_path = os.path.join(out_dir, 'sitemap.xml')
    
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        loc_urls = {elem.text.strip() for elem in root.iter('*') if elem.tag.endswith('loc')}
    except (FileNotFoundError, PermissionError, ET.ParseError):
        return problems
    
    noindex_pattern = re.compile(r'<meta\s+[^>]*name=["\'](robots)["\']\s*[^>]*content=["\'](.*?)(["\'])', re.IGNORECASE)
    
    for dirpath, _, filenames in os.walk(out_dir):
        for filename in sorted(filenames):
            if filename == '404.html':
                continue
            if not filename.endswith('.html'):
                continue
            
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            noindex_match = noindex_pattern.search(content)
            if noindex_match and 'noindex' in noindex_match.group(2).lower():
                canonical_url = None
                link_pattern = re.compile(r'<link\s+[^>]*rel=["\'](canonical)["\']\s*href=["\'](.*?)(["\'])', re.IGNORECASE)
                link_match = link_pattern.search(content)
                if link_match:
                    canonical_url = link_match.group(2).strip('"\'')
                
                if canonical_url and canonical_url in loc_urls:
                    problems.append({
                        'kind': 'noindex_in_sitemap',
                        'page': os.path.relpath(file_path, out_dir).replace('\\', '/'),
                        'loc': canonical_url,
                        'detail': 'page emits meta robots noindex but its canonical URL is listed in sitemap.xml (contradictory index signal)',
                        'severity': 'error'
                    })
    
    return problems

if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, 'pages'))
        
        with open(os.path.join(temp_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
            f.write("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://example.com/index.html</loc></url>
    <url><loc>https://example.com/noindex.html</loc></url>
</urlset>""")
        
        with open(os.path.join(temp_dir, 'pages', 'index.html'), 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index Page</title>
</head>
<body>
    <h1>Welcome to the Index Page</h1>
</body>
</html>""")
        
        with open(os.path.join(temp_dir, 'pages', 'noindex.html'), 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Noindex Page</title>
    <meta name="robots" content="noindex, none">
    <link rel="canonical" href="https://example.com/noindex.html">
</head>
<body>
    <h1>Welcome to the Noindex Page</h1>
</body>
</html>""")
        
        with open(os.path.join(temp_dir, 'pages', 'not_in_sitemap.html'), 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Not in Sitemap Page</title>
    <meta name="robots" content="noindex, none">
    <link rel="canonical" href="https://example.com/not_in_sitemap.html">
</head>
<body>
    <h1>Welcome to the Not in Sitemap Page</h1>
</body>
</html>""")
        
        problems = audit_noindex_sitemap(temp_dir, 'https://example.com')
        
        assert len(problems) == 1
        assert problems[0]['kind'] == 'noindex_in_sitemap'
        assert problems[0]['page'] == 'pages/noindex.html'
        assert problems[0]['loc'] == 'https://example.com/noindex.html'
        assert problems[0]['detail'] == 'page emits meta robots noindex but its canonical URL is listed in sitemap.xml (contradictory index signal)'
        assert problems[0]['severity'] == 'error'
        
        print('noindexsitemapcheck self-test OK')
