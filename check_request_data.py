"""this module contains function for checking request data"""

def check_attrs_in_json(jsonlike:dict,*args):
    """returns True if dict contains keys from args"""
    if not len(args):
        return False
    
    for attr in args:
        if attr not in jsonlike:
            return False

    return True