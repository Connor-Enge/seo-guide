import html

def heading_html(slug, inner_html):
    escaped_slug = html.escape(slug, quote=True)
    return f'<h2 id="{escaped_slug}">{inner_html}<a class="hanchor" href="#{escaped_slug}" aria-label="Permalink to this section"><span aria-hidden="true">¶</span></a></h2>'
