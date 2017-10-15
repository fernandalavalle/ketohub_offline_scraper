import re


class Error(Exception):
    pass


class UnexpectedCharacterError(Error):
    pass


def parse(ingredient_raw):
    canonicalized = ingredient_raw
    # Canonicalize apostrophes.
    canonicalized = re.sub(u'\u2019', '\'', canonicalized)
    # Canonicalize quotes.
    canonicalized = re.sub(u'[\u201c-\u201d]', '"', canonicalized)
    # Canonicalize spaces.
    canonicalized = re.sub(u'\u00a0', ' ', canonicalized)

    # Replace n-tilde character with normal n.
    canonicalized = re.sub(u'\u00f1', 'n', canonicalized)

    # Remove text in parentheses.
    canonicalized = re.sub('\(.*\)', '', canonicalized)
    # Remove "Optional:" prefix.
    canonicalized = re.sub(
        '^optional:\s*', '', canonicalized, flags=re.IGNORECASE)

    canonicalized = re.sub(r'~?\d+-\d+', '', canonicalized)
    canonicalized = re.sub(r'~?((\d+/\d+)|(\d+(\.\d+)?))( ?(g|(lbs?\.?)))?', '',
                           canonicalized)
    # Replace vulgar fraction characters
    canonicalized = re.sub(u'[\u00bc-\u00be]+', '', canonicalized)
    canonicalized = re.sub(u'[\u2150-\u215f]+', '', canonicalized)
    # Remove units of measure.
    canonicalized = re.sub(
        (r'\b((ounce)|(pound)|(tablespoo+n)|(teaspoo+n\.?)|(cup)|'
         r'(inche?))s?\.?\s?\b'),
        '',
        canonicalized,
        flags=re.IGNORECASE)
    canonicalized = re.sub(
        r'((oz)|(lb)|(tbsp)|(tsp))(\.|\b)',
        '',
        canonicalized,
        flags=re.IGNORECASE)
    # Remove other units of measure
    canonicalized = re.sub(
        r'\b((can)|(bar)|(clove)|(drop))s?\b',
        '',
        canonicalized,
        flags=re.IGNORECASE)
    canonicalized = re.sub(
        r'\bpinch( of)?', '', canonicalized, flags=re.IGNORECASE)
    # Replace slice or slices, but not sliced. Cube or cubes, but not cubed.
    canonicalized = re.sub(
        r'((slice)|(cube))s?\b', '', canonicalized, flags=re.IGNORECASE)
    canonicalized = re.sub(r',? ?peeled', '', canonicalized)
    canonicalized = re.sub(r',? ?seeded( and grated)?', '', canonicalized)
    canonicalized = re.sub(
        (r',? ?((if needed)|(to garnish)|(for greasing the pan)|'
         r'(room temperature)|(to taste))'),
        '',
        canonicalized,
        flags=re.IGNORECASE)
    #canonicalized = re.sub(r'\( ?((total)|(whole))\)', '', canonicalized)
    # Remove asterisks.
    canonicalized = re.sub(r'\*$', '', canonicalized)
    # Remove empty parentheses.
    canonicalized = re.sub(r'\([\s\-]*\)', '', canonicalized)
    # Hack to remove all the stray leading characters we missed earlier.
    canonicalized = re.sub(r'^\s*[\-+,%]', '', canonicalized)
    canonicalized = re.sub(r'^\s*of', '', canonicalized)
    # Collapse repeated whitespaces to single spaces.
    canonicalized = re.sub(r'\s+', ' ', canonicalized)

    canonicalized = canonicalized.strip()

    if re.search(r'[^\x00-\x7F]', canonicalized):
        raise UnexpectedCharacterError(
            'Unexpected character in string: %s' % ingredient_raw)

    return canonicalized.strip()
