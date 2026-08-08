import re
from urllib.parse import urlparse

def mark_external(html, site):
    site_host = urlparse(site).netloc
    
    def is_external(href, site_host):
        if href.startswith(('http://', 'https://')):
            return urlparse(href).netloc != site_host
        elif href.startswith('//'):
            return urlparse(f'https:{href}').netloc != site_host
        return False
    
    def mark_anchor(match):
        tag = match.group(0)
        href = re.search(r'href=["\'](.*?)["\']', tag, re.IGNORECASE).group(1)
        if is_external(href, site_host):
            rel = re.search(r'rel=["\'](.*?)["\']', tag, re.IGNORECASE)
            class_attr = re.search(r'class=["\'](.*?)["\']', tag, re.IGNORECASE)
            
            new_tag = tag
            if rel:
                rel_value = rel.group(1).strip()
                if 'noopener' not in rel_value.split():
                    new_tag = re.sub(r'rel=["\'][^"]*["\']', f'rel="{rel_value} noopener"', new_tag)
            else:
                new_tag = re.sub(r'<a ', r'<a rel="noopener" ', new_tag)
            
            if class_attr:
                class_value = class_attr.group(1).strip()
                if 'ext' not in class_value.split():
                    new_tag = re.sub(r'class=["\'][^"]*["\']', f'class="{class_value} ext"', new_tag)
            else:
                new_tag = re.sub(r'<a ', r'<a class="ext" ', new_tag)
            
            return new_tag
        return tag
    
    pattern = re.compile(r'<a [^>]*>', re.IGNORECASE)
    marked_html = pattern.sub(mark_anchor, html)
    
    return marked_html
