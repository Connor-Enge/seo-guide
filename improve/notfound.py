import html

NF_TITLE = 'Page not found'
NF_DESCRIPTION = 'The page you are looking for could not be found. Please search or pick a section.'
NF_H1 = 'Oops! Page Not Found'
NF_BYLINE = 'Don\'t worry, we can help you find what you need.'

def notfound_content(base_url, cards):
    intro_paragraphs = [
        '<p>The page you are looking for could not be found. Please search or pick a section.</p>',
        '<p>Use the search form below to find what you need.</p>'
    ]
    
    search_form = f'''
    <form class="searchform" role="search" method="get" action="{html.escape(base_url + '/search/', quote=True)}">
        <label class="visually-hidden" for="nf-q">Search the guide</label>
        <input type="search" id="nf-q" name="q" placeholder="Search the guide…" autocomplete="off" enterkeyhint="search">
        <button type="submit">Search</button>
    </form>
    '''
    
    related_pages = f'''
    <nav class="related" aria-label="Popular pages">
        <h2>Popular pages</h2>
        <ul class="related-list">
            {''.join(f'<li><a href="{html.escape(url, quote=True)}">{html.escape(title)}</a><p>{html.escape(description)}</p></li>' for title, description, url in cards)}
        </ul>
    </nav>
    '''
    
    return '\n'.join(intro_paragraphs + [search_form, related_pages])
