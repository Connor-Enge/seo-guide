from html import escape

def rank_related(current_slug, current_tags, posts, limit=3):
    related_posts = []
    for post in posts:
        if post['slug'] != current_slug and len(set(current_tags) & set(post['tags'])) > 0:
            related_posts.append((post, len(set(current_tags) & set(post['tags']))))
    related_posts.sort(key=lambda x: (-x[1], posts.index(x[0])))
    return [post for post, _ in related_posts[:limit]]

def related_posts_block(current_slug, current_tags, posts, post_url, limit=3):
    related_posts = rank_related(current_slug, current_tags, posts, limit)
    if not related_posts:
        return ''
    
    lis = []
    for post in related_posts:
        title = escape(post['title'])
        description = escape(post.get('description', ''))
        url = escape(post_url(post['slug']))
        minutes = post.get('minutes')
        
        if minutes and minutes > 0:
            reading_time_token = f'<p class="meta">{minutes} min read</p>'
        else:
            reading_time_token = ''
        
        li = f'<li><a href="{url}">{title}</a>{reading_time_token}<p>{description}</p></li>'
        lis.append(li)
    
    return f'<nav class="related related-posts" aria-label="Related articles"><h2>Related articles</h2><ul class="related-list">{"".join(lis)}</ul></nav>'
