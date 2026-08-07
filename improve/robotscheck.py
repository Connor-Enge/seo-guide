import os

def audit_robots(out_dir, base_url):
    problems = []
    sitemaps = []
    saw_rule_anywhere = False
    star_group = False
    seen_rule_in_group = False
    blanket = False

    robots_path = os.path.join(out_dir, 'robots.txt')
    try:
        with open(robots_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' not in line:
                    continue
                field, value = line.split(':', 1)
                field = field.strip().lower()
                value = value.strip()

                if field == 'sitemap':
                    sitemaps.append(value)
                elif field == 'user-agent':
                    if seen_rule_in_group:
                        star_group = False
                        seen_rule_in_group = False
                    if value == '*':
                        star_group = True
                elif field == 'allow' or field == 'disallow':
                    seen_rule_in_group = True
                    saw_rule_anywhere = True
                    if field == 'disallow' and value == '/' and star_group:
                        blanket = True

    except (OSError, FileNotFoundError):
        return [{'kind': 'missing_file', 'loc': '', 'detail': 'docs/robots.txt not found', 'severity': 'error'}]

    if not sitemaps:
        problems.append({'kind': 'missing_sitemap', 'loc': '', 'detail': 'no Sitemap: directive', 'severity': 'error'})
    for s in sitemaps:
        if not (s.startswith('http://') or s.startswith('https://')):
            problems.append({'kind': 'relative_sitemap', 'loc': s, 'detail': 'Sitemap URL must be absolute', 'severity': 'error'})
    expected = base_url.rstrip('/') + '/sitemap.xml'
    if sitemaps and expected not in sitemaps:
        problems.append({'kind': 'sitemap_mismatch', 'loc': sitemaps[0], 'detail': 'expected ' + expected, 'severity': 'error'})
    if blanket:
        problems.append({'kind': 'blanket_disallow', 'loc': 'User-agent: *', 'detail': 'Disallow: / would deindex the whole site', 'severity': 'error'})
    if not saw_rule_anywhere:
        problems.append({'kind': 'no_rules', 'loc': '', 'detail': 'no Allow/Disallow directives present', 'severity': 'warn'})

    return problems
