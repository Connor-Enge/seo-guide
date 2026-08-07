"""
Prefixes root-relative links with the deploy base path so project-subpath GitHub Pages links don't 404.
"""

def resolve_href(href, base_url):
    if href is None or href == '':
        return href
    if href.startswith(('#', 'http://', 'https://', '//', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return href
    if href.startswith('/'):
        return base_url.rstrip('/') + href
    return href
