import re


def is_integer_string(s):
    """Checks if a string 's' can be converted to an integer."""
    if not isinstance(s, str):
        return False
    try:
        # This is the key part: it successfully converts "0", "1", etc., 
        # but fails on "<no-name>" or "filter_button".
        int(s)
        return True
    except ValueError:
        return False


def is_matching_pattern(string, pattern):
    """Check if string matches pattern"""
    return re.fullmatch(pattern, string) is not None
