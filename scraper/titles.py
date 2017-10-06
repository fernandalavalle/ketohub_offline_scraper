def canonicalize(title):
    canonicalized = title
    canonicalized = _remove_prefix(canonicalized)
    canonicalized = _normalize_conventions(canonicalized)
    return canonicalized


def _remove_prefix(title):
    stripped = title
    prefixes = ['Keto Bites:', 'Keto Recipe:']
    for prefix in prefixes:
        stripped = stripped.replace(prefix, '').strip()
    return stripped


def _normalize_conventions(title):
    normalized = title
    substitutions = [('Gluten Free', 'Gluten-Free'),
                     ('Guilt Free', 'Guilt-Free'), ('Sugar Free', 'Sugar-Free'),
                     (' & ', ' and '), ('Slow-Cooker', 'Slow Cooker')]
    for old, new in substitutions:
        normalized = normalized.replace(old, new)

    return normalized
