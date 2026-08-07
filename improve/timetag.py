"""
Create a function to wrap a date string in an HTML <time> tag with a label.
"""

import datetime

def time_tag(date_str, label):
    """
    Wrap a date string in an HTML <time> tag if it's a valid YYYY-MM-DD date.

    :param date_str: The date string to validate and wrap.
    :param label: The text content for the <time> element.
    :return: A string with the date wrapped in <time> tags or the original label.
    """
    try:
        d = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        if d.strftime('%Y-%m-%d') == date_str:
            return f'<time datetime="{date_str}">{label}</time>'
    except (ValueError, TypeError):
        pass
    return label
