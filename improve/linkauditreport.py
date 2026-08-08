import json
from collections import Counter

def write_link_audit(problems, dest_path):
    report = {
        'total_problems': len(problems),
        'ok': len(problems) == 0,
        'counts_by_kind': dict(Counter(problem['kind'] for problem in problems)),
        'problems': problems
    }
    with open(dest_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    return report
