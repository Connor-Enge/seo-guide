import os
import re

META_RE = re.compile(r'<meta\b[^>]*>', re.IGNORECASE)
NAME_RE = re.compile(r'name\s*=\s*([\"\'])\s*twitter:card\s*\1', re.IGNORECASE)
CONTENT_RE = re.compile(r'content\s*=\s*([\"\'])(.*?)\1', re.IGNORECASE)
VALID = {'summary', 'summary_large_image', 'app', 'player'}

def audit_twitter_card(docs_dir):
    problems = []
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    html = f.read()
                for match in META_RE.finditer(html):
                    tag = match.group(0)
                    name_match = NAME_RE.search(tag)
                    if name_match:
                        content_match = CONTENT_RE.search(tag)
                        content = content_match.group(2) if content_match else ''
                        stripped_content = content.strip()
                        if stripped_content not in VALID:
                            problems.append({
                                'kind': 'twitter_card_invalid',
                                'page': os.path.relpath(path, docs_dir).replace(os.sep, '/'),
                                'detail': f"twitter:card='{stripped_content}' is not a valid card type (expected one of summary, summary_large_image, app, player)",
                                'severity': 'error'
                            })
    return problems

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python twittercardcheck.py <docs_dir>")
        sys.exit(1)
    docs_dir = sys.argv[1]
    problems = audit_twitter_card(docs_dir)
    for problem in problems:
        print(problem)
