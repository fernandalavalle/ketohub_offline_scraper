import re


def canonicalize(title):
    canonicalized = title
    canonicalized = _remove_prefix(canonicalized)
    canonicalized = _remove_curly_brace_text(canonicalized)
    canonicalized = _remove_junk_words(canonicalized)
    canonicalized = _normalize_conventions(canonicalized)
    canonicalized = _collapse_whitespace(canonicalized)
    return canonicalized.strip()


def _remove_prefix(title):
    stripped = title
    prefixes = ['Keto Bites:', 'Keto Recipe:']
    for prefix in prefixes:
        stripped = stripped.replace(prefix, '').strip()
    return stripped


def _remove_curly_brace_text(title):
    return re.sub(r'{.*}', '', title)


def _remove_junk_words(title):
    return title.replace('Recipe', '')


def _normalize_conventions(title):
    normalized = title
    substitutions = [('Gluten Free', 'Gluten-Free'),
                     ('Guilt Free', 'Guilt-Free'), ('Sugar Free', 'Sugar-Free'),
                     (' & ', ' and '), ('Slow-Cooker', 'Slow Cooker')]
    for old, new in substitutions:
        normalized = normalized.replace(old, new)

    return normalized


def _collapse_whitespace(title):
    return re.sub(r'\s+', ' ', title)
