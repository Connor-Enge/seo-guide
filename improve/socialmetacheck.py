import os
from html.parser import HTMLParser

class MetaTagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_tags = {}
        self.link_tags = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'link':
            for name, value in attrs:
                if name == 'rel' and value == 'canonical':
                    for attr_name, attr_value in attrs:
                        if attr_name == 'href':
                            self.link_tags['canonical'] = attr_value
        elif tag == 'meta':
            for name, value in attrs:
                if name == 'property':
                    property_parts = value.split(':')
                    if len(property_parts) == 2:
                        namespace, key = property_parts
                        for attr_name, attr_value in attrs:
                            if attr_name == 'content':
                                self.meta_tags[f'{namespace}:{key}'] = attr_value.strip()
                elif name == 'name':
                    if value == 'twitter:card':
                        for attr_name, attr_value in attrs:
                            if attr_name == 'content':
                                self.meta_tags['twitter:card'] = attr_value.strip()

def audit_social_meta(out_dir):
    problems = []
    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                parser = MetaTagParser()
                parser.feed(content)
                
                canonical_url = parser.link_tags.get('canonical')
                og_title = parser.meta_tags.get('og:title')
                og_description = parser.meta_tags.get('og:description')
                og_url = parser.meta_tags.get('og:url')
                twitter_card = parser.meta_tags.get('twitter:card')

                if canonical_url:
                    if not og_url:
                        problems.append({
                            'kind': 'og_url_missing',
                            'page': file_path,
                            'detail': 'rel=canonical is present but og:url is missing.',
                            'severity': 'error'
                        })
                    elif og_url.startswith('/'):
                        problems.append({
                            'kind': 'og_url_relative',
                            'page': file_path,
                            'detail': 'og:url is root-relative.',
                            'severity': 'error'
                        })
                    else:
                        if canonical_url != og_url:
                            problems.append({
                                'kind': 'og_url_canonical_mismatch',
                                'page': file_path,
                                'detail': f'og:url {og_url} does not match canonical URL {canonical_url}.',
                                'severity': 'error'
                            })

                if not og_title:
                    problems.append({
                        'kind': 'missing_og_title',
                        'page': file_path,
                        'detail': 'og:title is missing.',
                        'severity': 'warn'
                    })

                if not og_description:
                    problems.append({
                        'kind': 'missing_og_description',
                        'page': file_path,
                        'detail': 'og:description is missing.',
                        'severity': 'warn'
                    })

                if not twitter_card:
                    problems.append({
                        'kind': 'missing_twitter_card',
                        'page': file_path,
                        'detail': 'twitter:card is missing.',
                        'severity': 'warn'
                    })

    return problems
