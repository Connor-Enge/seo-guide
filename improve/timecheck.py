import os
import re

def audit_time(root):
    """
    Audit all <time> elements in HTML files within a directory for valid datetime attributes.

    :param root: The filesystem directory path to audit (e.g., 'docs/').
    :return: A list of problem dicts, each with keys 'kind', 'page', and 'detail'.
    """
    problems = []
    date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    time_tags = re.findall(r'<time[^>]*>', content, re.IGNORECASE)
                    for tag in time_tags:
                        match = re.search(r'datetime=["\']([^"\']+)["\']', tag)
                        if not match:
                            problems.append({
                                'kind': 'time_datetime_missing',
                                'page': os.path.relpath(filepath, root).replace(os.sep, '/'),
                                'detail': '<time> element is missing a datetime attribute'
                            })
                        else:
                            dt_value = match.group(1)
                            if not dt_value or not date_regex.match(dt_value):
                                problems.append({
                                    'kind': 'time_datetime_invalid',
                                    'page': os.path.relpath(filepath, root).replace(os.sep, '/'),
                                    'detail': f'<time> datetime=\'{dt_value}\' is not a zero-padded ISO date (YYYY-MM-DD)'
                                })

    return problems
