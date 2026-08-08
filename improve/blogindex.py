"""
Tiny helper module for a static-site generator to render one list item for the blog index listing.
"""

import html

def post_list_item(url, title, date_html, description, minutes):
    escaped_title = html.escape(title)
    escaped_description = html.escape(description)
    
    meta_line = f'Published {date_html}'
    if minutes and minutes > 0:
        meta_line += f' \u00b7 {minutes} min read'
    
    return f'<li><h2><a href="{url}">{escaped_title}</a></h2><p class="meta">{meta_line}</p><p>{escaped_description}</p></li>'
