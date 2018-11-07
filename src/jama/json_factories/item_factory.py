"""Purpose of file is to prodcue a JSON object for an item.

Pulled JSON object from Jama SwaggeUI instance on creating an item.
"""

def generate_item():
    """Generates a JSON object to then manipulate
    Args:
        None

    Returns: 
        Object: to create an item
    """
    return {
        "project": -1,
        "itemType": 33, # Default is a text item
        "childItemType": 0,
        "location": {
        "parent": {
            "item": 0
            }
        },
        "fields": {},
        "setGlobalIdManually": False
    }
