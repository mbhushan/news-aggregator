'''
Created on Nov 26, 2014

@author: rsingh
'''
import cgi
import re

def is_int(val):
    if isinstance(val, int):
        return True
    else:
        try:
            if isinstance(val, str) or isinstance(val, unicode):
                if len(val) > 18:
                    return False

            val = int(val)
            return True
        except:
            return False

def is_float(val):
    if isinstance(val, float):
        return True
    else:
        try:
            if isinstance(val, str) or isinstance(val, unicode):
                if len(val) > 18:
                    return False

            val = float(val)
            return True
        except:
            return False


def escape_html(val):
    return cgi.escape(val)

def is_alnum(val):
    return unicode(val).isalnum()

def check_bool(val):
    '''checks for and/or'''
    if val == 'and' or val == 'or':
        return True

    return False

def is_latitude(val):
    try:
        lat = float(val)
        if -90.0 <= lat <= 90.0:
            return True
        else:
            return False
    except:
        return False

def is_longitude(val):
    try:
        lat = float(val)
        if -180.0 <= lat <= 180.0:
            return True
        else:
            return False
    except:
        return False

def is_hashtag_valid(val):
    if re.search("[!$%^&*<>{}()+.'\", ]", val):
        return False

    return True

def is_url_valid(val):
    if re.search("^(https?://)", val):
        return True
    return False

def is_string_safe(val, length=1000):
    if len(val) > length:
        return False

    if re.search("([<>&])", val):
        return False

    return  True

def is_empty_string(val):
    if val is None or val.strip() == '':
        return True
    return False

def is_empty_list(val):
    if val and isinstance(val, list):
        return False
    return True



