import os

def shared_tag_posts(posts):
    """
    Return a set of slugs that share at least one tag with at least one other post.
    """
    tag_to_slugs = {}
    for post in posts:
        if not post['tags']:
            continue
        for tag in post['tags']:
            if tag not in tag_to_slugs:
                tag_to_slugs[tag] = set()
            tag_to_slugs[tag].add(post['slug'])
    
    shared_slugs = set()
    for slugs in tag_to_slugs.values():
        if len(slugs) > 1:
            shared_slugs.update(slugs)
    
    return shared_slugs

def has_related_posts_block(html):
    """
    Return True if the HTML string contains the related-posts nav marker.
    """
    return 'related-posts' in html

def audit_related_posts_data(posts, rendered):
    """
    Audit the related posts data and return a list of problems.
    """
    shared_slugs = shared_tag_posts(posts)
    problems = []
    
    for post in posts:
        slug = post['slug']
        expected = slug in shared_slugs
        present = has_related_posts_block(rendered.get(slug, ''))
        
        if expected and not present:
            problems.append({
                'kind': 'related_posts_missing',
                'page': slug,
                'detail': 'shares a tag with another post but has no related-posts block'
            })
        elif (not expected) and present:
            problems.append({
                'kind': 'related_posts_unexpected',
                'page': slug,
                'detail': 'has a related-posts block but shares no tag with any other post'
            })
    
    return problems

def audit_related_posts(out_dir, posts, post_url):
    """
    Audit the related posts in the filesystem and return a list of problems.
    """
    rendered = {}
    for post in posts:
        slug = post['slug']
        file_path = os.path.join(out_dir, 'blog', slug, 'index.html')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                rendered[slug] = f.read()
        except FileNotFoundError:
            rendered[slug] = ''
    
    return audit_related_posts_data(posts, rendered)
