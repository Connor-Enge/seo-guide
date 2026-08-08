import html
import re

"""
Static-site generator functions for HTML headings and subheadings.
"""

def heading_html(slug, inner_html):
    escaped_slug = html.escape(slug, quote=True)
    return f'<h2 id="{escaped_slug}">{inner_html}<a class="hanchor" href="#{escaped_slug}" aria-label="Permalink to this section"><span aria-hidden="true">¶</span></a></h2>'

def subheading_html(text, inner_html, seen):
    base = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    if not base:
        base = 'section'
    
    n = 1
    while True:
        id = f'{base}-{n}' if n > 1 else base
        if id not in seen:
            break
        n += 1
    
    seen.add(id)
    escaped_id = html.escape(id, quote=True)
    return f'<h3 id="{escaped_id}">{inner_html}<a class="hanchor" href="#{escaped_id}" aria-label="Permalink to this section"><span aria-hidden="true">¶</span></a></h3>'
