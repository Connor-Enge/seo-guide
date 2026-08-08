from html import escape

def rank_related(current_slug, current_tags, posts, limit=3):
    """
    Rank related articles based on shared tags.
    
    :param current_slug: str, slug of the current post
    :param current_tags: list of str, tags of the current post
    :param posts: list of dicts, each with 'slug', 'title', 'description', and 'tags'
    :param limit: int, maximum number of related posts to return
    :return: list of dicts, top ranked related posts
    """
    current_tags_set = set(current_tags)
    related_posts = []
    
    for post in posts:
        if post['slug'] == current_slug:
            continue
        
        overlap = len(current_tags_set & set(post['tags']))
        if overlap > 0:
            related_posts.append((post, overlap))
    
    related_posts.sort(key=lambda x: (-x[1], posts.index(x[0])))
    return [post for post, _ in related_posts[:limit]]

def related_posts_block(current_slug, current_tags, posts, post_url, limit=3):
    """
    Generate an HTML block of related articles.
    
    :param current_slug: str, slug of the current post
    :param current_tags: list of str, tags of the current post
    :param posts: list of dicts, each with 'slug', 'title', 'description', and 'tags'
    :param post_url: callable, takes a slug and returns the URL
    :param limit: int, maximum number of related posts to return
    :return: str, HTML markup for the related articles block
    """
    related_posts = rank_related(current_slug, current_tags, posts, limit)
    
    if not related_posts:
        return ''
    
    lis = ''.join(
        f'<li><a href="{escape(post_url(post["slug"]))}">{escape(post["title"])}</a><p>{escape(post["description"])}</p></li>'
        for post in related_posts
    )
    
    return f'<nav class="related related-posts" aria-label="Related articles"><h2>Related articles</h2><ul class="related-list">{lis}</ul></nav>'
