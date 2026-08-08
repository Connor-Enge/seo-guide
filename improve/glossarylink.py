import re
import os
from html import escape

MAX_LINKS = 10

def slugify(s):
    return '-'.join(re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower().split())

def load_terms():
    terms = []
    try:
        with open(os.path.join(os.path.dirname(__file__), '../content/glossary.md'), 'r') as f:
            for line in f:
                if line.startswith('## '):
                    raw = line[3:].rstrip()
                    anchor = slugify(raw)
                    term = re.sub(r'\s*\([^)]+\)\s*', '', raw)
                    if term:
                        terms.append((term, anchor))
    except Exception:
        pass
    return terms

def annotate(content_html, current_slug, base_url, terms=None):
    if current_slug in {'glossary', 'index'}:
        return content_html
    
    if terms is None:
        terms = load_terms()
    if not terms:
        return content_html
    
    terms.sort(key=lambda x: len(x[0]), reverse=True)
    
    depth = 0
    skip = False
    result = []
    tag_stack = []
    
    for token in re.split(r'(<[^>]+>)', content_html):
        if token.startswith('<'):
            match = re.match(r'</?\s*([a-zA-Z0-9]+)', token)
            if match:
                tag_name = match.group(1).lower()
                if tag_name in {'a', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
                    if token.startswith('</'):
                        depth = max(0, depth - 1)
                    else:
                        depth += 1
                skip = tag_name in {'a', 'code', 'pre'}
            elif token.startswith('<!--'):
                skip = True
        elif not skip and depth == 0:
            for term, anchor in terms:
                pattern = re.compile(r'(?<![A-Za-z0-9])\b{}\b(?![A-Za-z0-9])'.format(re.escape(term)), re.IGNORECASE)
                if pattern.search(token):
                    replacement = '<a class="gloss" href="{}#{}" title="Glossary: {}">{}</a>'.format(base_url.rstrip('/'), anchor, escape(term), token)
                    token = pattern.sub(lambda m: replacement, token, count=1)
                    terms.remove((term, anchor))
                    if len(terms) == 0 or len(result) >= MAX_LINKS:
                        break
        
        result.append(token)
    
    return ''.join(result)
