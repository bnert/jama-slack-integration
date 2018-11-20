from jama import api_caller

def get_projectID(base_url, start, teamID, userID):
    """
    Get all the project from jama

    Args:
        base_url (string): jama instance base url
        start (int): start at a specific location
        teamID (string): user team ID, for OAuth
        userID (string): user ID, for OAuth
    Returns:
        (dict): Returns JSON object of the Jama API /projects
    """
    url = base_url + "/rest/latest/projects?startAt=" +\
          str(start) + "&maxResults=50"
    return api_caller.get(teamID, userID, url)


def get_project_by_ID(base_url, projectID, teamID, userID):
    """
    Get the project from jama by project id

    Args:
        base_url (string): jama instance base url
        projectID (string): project id
        teamID (string): user team ID, for OAuth
        userID (string): user ID, for OAuth
    Returns:
        (dict): Returns JSON object of the Jama API /projects/{id}
    """
    url = base_url + "/rest/latest/projects/" + projectID
    return api_caller.get(teamID, userID, url)


def get_item_by_ID(base_url, itemID, teamID, userID):
    """
    Get the item from jama by item id

    Args:
        base_url (string): jama instance base url
        itemID (string): item id
        teamID (string): user team ID, for OAuth
        userID (string): user ID, for OAuth
    Returns:
        (dict): Returns JSON object of the Jama API /abstractitems
    """
    url = base_url + "/rest/latest/abstractitems/" + itemID
    return api_caller.get(teamID, userID, url)


def get_item(base_url, projectID, start, teamID, userID):
    """
    Get all the item from a project

    Args:
        base_url (string): jama instance base url
        projectID (int): project id
        start (int): start at a specific index
        teamID (string): user team ID, for OAuth
        userID (string): user ID, for OAuth
    Returns:
        (dict): Returns JSON object of the Jama API /items
    """
    url = base_url + "/rest/latest/items?project=" + str(projectID) +\
        "&startAt=" + str(start) + "&maxResults=50"
    return api_caller.get(teamID, userID, url)


def search_item(base_url, projectID, start, contains, teamID, userID):
    """
    Search a item from a project

    Args:
        base_url (string): jama instance base url
        projectID (int): project id
        start (int): start at a specific index
        contains (string): the keyword
        teamID (string): user team ID, for OAuth
        userID (string): user ID, for OAuth
    Returns:
        (dict): Returns JSON object of the Jama API /abstractitems
    """
    url = base_url + "/rest/latest/abstractitems?project=" +\
          str(projectID) + "&contains=" + contains + "&startAt=" + str(start) + "&maxResults=50"
    return api_caller.get(teamID, userID, url)
