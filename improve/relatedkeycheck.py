def audit_related_keys(items, valid_keys):
    """
    Audit the 'related:' field in front-matter for unresolved keys.

    :param items: Iterable of (page_label, related_field) pairs.
    :param valid_keys: Iterable of strings representing valid registry keys.
    :return: List of dicts with unresolved key warnings.
    """
    valid_keys = set(valid_keys)
    results = []

    for page_label, related_field in items:
        if related_field is None or not related_field.strip():
            continue

        seen = set()
        for token in related_field.split(','):
            token = token.strip()
            if token and token not in valid_keys and token not in seen:
                results.append({
                    "kind": "related_key_unresolved",
                    "page": page_label,
                    "detail": f"related: key '{token}' resolves to no known page or post slug"
                })
                seen.add(token)

    return results
