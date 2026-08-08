import re
import os
from html import escape

MAX_LINKS = 10

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def load_terms():
    try:
        path = os.path.join(os.path.dirname(__file__), '..', 'content', 'glossary.md')
        with open(path, 'r') as f:
            lines = f.readlines()
        terms = []
        for line in lines:
            if line.startswith('## '):
                raw = line[3:].rstrip()
                term = re.sub(r'\s*\([^)]*\)', '', raw).strip()
                if term:
                    anchor = slugify(raw)
                    terms.append((term, anchor))
        return terms
    except Exception:
        return []

def annotate(content_html, current_slug, base_url, terms=None):
    if current_slug in {'glossary', 'index'}:
        return content_html
    
    if terms is None:
        terms = load_terms()
    if not terms:
        return content_html
    
    sorted_terms = sorted(terms, key=lambda x: len(x[0]), reverse=True)
    lower_to_term = {term.lower(): (anchor, term) for anchor, term in sorted_terms}
    
    pattern = re.compile(r'(?<![A-Za-z0-9])(' + '|'.join(re.escape(t) for t,_ in sorted_terms) + r')(?![A-Za-z0-9])', re.IGNORECASE)
    
    def replace(match):
        matched = match.group(1)
        key = matched.lower()
        if len(used) >= MAX_LINKS or key in used or key not in lower_to_term:
            return matched
        used.add(key)
        anchor, canonical_term = lower_to_term[key]
        href = base_url.rstrip('/') + '/glossary/#' + anchor
        return f'<a class="gloss" href="{href}" title="Glossary: {escape(canonical_term, quote=True)}">{matched}</a>'
    
    used = set()
    skip_depth = 0
    tokens = re.split(r'(<[^>]+>)', content_html)
    result = []
    for token in tokens:
        if token.startswith('<'):
            if token.lower().startswith('</'):
                skip_depth -= 1
            elif token.lower().startswith('<a') or token.lower().startswith('<code') or token.lower().startswith('<pre') or re.match(r'<h[1-6]', token, re.IGNORECASE):
                skip_depth += 1
        if skip_depth == 0 and not token.startswith('<'):
            result.append(pattern.sub(replace, token))
        else:
            result.append(token)
    
    return ''.join(result)
