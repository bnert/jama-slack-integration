def make_dict(content):
    """Turns formatted string int o dict
    
    Args:
        content (string): request form data, in a string format like:
            <action>: <param1>:<data1>, <param2>:<data2>, ...
    Returns:
        dict object

    Raises:
        Exception
    """
    content_dict = {}
    try:
        kvpairs = content.split("|")
        for kvpair in kvpairs:
            kvpair = kvpair.split("=")

            key = kvpair[0].strip()
            value = kvpair[1].strip()

            content_dict[key] = value
    except:
        return {}

    return content_dict