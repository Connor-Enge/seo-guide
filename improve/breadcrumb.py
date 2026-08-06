import html

def breadcrumb_block(crumbs):
    if len(crumbs) < 2:
        return ''
    
    items = []
    for label, url in crumbs[:-1]:
        items.append('<li><a href="%s">%s</a></li>' % (html.escape(url, quote=True), html.escape(label)))
    
    last_label, _ = crumbs[-1]
    items.append('<li><span aria-current="page">%s</span></li>' % html.escape(last_label))
    
    return '<nav class="breadcrumb" aria-label="Breadcrumb"><ol>%s</ol></nav>' % ''.join(items)
