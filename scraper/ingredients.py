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
    # Canonicalize dashes.
    canonicalized = re.sub(u'[\u2010-\u2015]', '-', canonicalized)
    # Canonicalize spaces.
    canonicalized = re.sub(u'\u00a0', ' ', canonicalized)

    # Replace n-tilde character with normal n.
    canonicalized = re.sub(u'\u00f1', 'n', canonicalized)
    # Replace accented e with simple e.
    canonicalized = re.sub(u'[\u00e8-\u00eb]', 'e', canonicalized)

    # Remove registered and copyright symbols.
    canonicalized = re.sub(u'[\u00a9\u00ae]', '', canonicalized)

    # Remove text in parentheses.
    canonicalized = re.sub('\(.*\)', '', canonicalized)
    # Remove "Optional:" prefix.
    canonicalized = re.sub(
        '^optional:\s*', '', canonicalized, flags=re.IGNORECASE)

    # Remove brand names.
    canonicalized = canonicalized.replace('NatureRaised Farms', '')

    # Remove number ranges.
    canonicalized = re.sub(r'~?\d+-\d+', '', canonicalized)
    # Remove numbers, fractions, and decimals.
    #canonicalized = re.sub(r'\d+([\.\/\s\-]+\d+)?', '', canonicalized)
    # Replace vulgar fraction characters with dummy fraction (will be removed
    # later).
    canonicalized = re.sub(u'[\u00bc-\u00be]+', '1/2', canonicalized)
    canonicalized = re.sub(u'[\u2150-\u215f]+', '1/2', canonicalized)
    # Remove non-abbreviated units of measure.
    canonicalized = re.sub(
        (r'~?\d+([\.\/\s\-]+\d+)?\s*((ounce)|(pound)|(tablespoo+n)|'
         r'(teaspoo+n\.?)|(cup)|(scoop)|(inche?)|(can)|(cup)|(pint)|(container)|(bar)|'
         r'(clove)|(sprig)|(head)|(drop)|(stalk)|(piece))s?\.?\s?\b'),
        '',
        canonicalized,
        flags=re.IGNORECASE)
    # Remove abbreviated units of measure.
    canonicalized = re.sub(
        r'~?\d+([\.\/\s\-]+\d+)?\s*((fl\.? oz)|(g)|(lbs?)|(oz)|(tbsp)|(tsp)|'
        r'(pint))(\.|\b)',
        '',
        canonicalized,
        flags=re.IGNORECASE)
    # Remove remaining numbers.
    canonicalized = re.sub(r'\d+([\.\/\s\-]+\d+)?[^\d%]', '', canonicalized)
    canonicalized = re.sub(
        r'\bpinch( of)?', '', canonicalized, flags=re.IGNORECASE)
    # Replace slice or slices, but not sliced. Cube or cubes, but not cubed.
    canonicalized = re.sub(
        r'((slice)|(cube))s?\b', '', canonicalized, flags=re.IGNORECASE)
    canonicalized = re.sub(r',? ?peeled', '', canonicalized)
    canonicalized = re.sub(r',? ?seeded( and grated)?', '', canonicalized)
    canonicalized = re.sub(r'(chopped and )?separated in', '', canonicalized)
    canonicalized = re.sub(
        (r',? ?((if needed)|(to garnish)|(for greasing the pan)|'
         r'(room temperature)|(to taste)|(if desired))'),
        '',
        canonicalized,
        flags=re.IGNORECASE)

    # Fix misspelling of xanthan gum.
    canonicalized = re.sub(
        'xantham', 'xanthan', canonicalized, flags=re.IGNORECASE)

    # Remove leading 'can'.
    canonicalized = re.sub('^\s*can', '', canonicalized)

    # Hack to remove all the stray leading characters we missed earlier.
    canonicalized = re.sub(r'^\s*([\-/+,%]\s*)+', '', canonicalized)
    canonicalized = re.sub(r'^\s*of', '', canonicalized)
    # Hack to remove all the stray trailing characters we missed earlier.
    canonicalized = re.sub(r'\s*[\-,]\s*$', '', canonicalized)
    # Remove asterisks.
    canonicalized = re.sub(r'\*\s*$', '', canonicalized)
    # Collapse repeated whitespaces to single spaces.
    canonicalized = re.sub(r'\s+', ' ', canonicalized)
    # Remove whitespace in front of commas.
    canonicalized = re.sub(r'\s+,', ',', canonicalized)

    canonicalized = canonicalized.strip()

    if re.search(r'[^\x00-\x7F]', canonicalized):
        raise UnexpectedCharacterError(
            'Unexpected character in string: %s' % ingredient_raw)

    return canonicalized.strip()
