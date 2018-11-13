from flask import make_response
from datetime import datetime
from slack.tools import return_to_slack

"""Return basic info about command invocation
"""

def all(req):
    """all: show info for all the commands


    Arguments:
        req (Request object): Passed down to return to slack

    Returns:
        Response (object): Returned up to called funciton in route_handler
    """
    return_to_slack(req, {
                    "text": "Hey! Here is a quick guide to using `/jamaconnect`:",
                    "attachments": [
                        {
                            "text": """
1. Comment:
    \t`/jamaconnect comment` brings up a dialog to comment on an item.
    \t---- or -----
    \t`/jamaconnect comment: <itemID>, <commentBody>` will also work.

2. Create:
    \t`/jamaconnect create: dialog | project=<projectId>` brings up a dialog for
    \t\t\tthe top level items for the specified project, given the id.
    \t---- or -----
    \t`/jamaconnect create: project=<projectID> | name=project name | ...` will
    \t\t\talso work, where `...` is other arguments, such as: `item=<itemID>`, or
    \t\t\t`description=your item description`.

3. Search:
    \t`/jamaconnect search: key=<your search phrase>` will return relevant items
    \t---- or -----
    \t`/jamaconnect display: id=<itemID>` will return details of the specified item,
    \t\t\tgiven the item ID.

*Note: all fields with `<...>` around them are places you need to provide input. 
If a field is an ID (e.g. projectID), it needs to be a number. Otherwise, it can be text.*
                            """
                        }
                    ]
                })
    return make_response("", 200)

def comment(req, headline="Hey! Here is a quick guide to using `/jamaconnect comment`:"):
    """comment: show info for comment slash command


    Arguments:
        req (Request object): Passed down to return to slack

    Returns:
        Response (object): Returned up to called funciton in route_handler
    """
    return_to_slack(req, {
                    "text": headline,
                    "attachments": [
                        {
                            "text": """
Comment usage:
    \t`/jamaconnect comment` brings up a dialog to comment on an item.
    \t---- or -----
    \t`/jamaconnect comment: <itemID>, <commentBody>` will also work.

*Note: all fields with `<...>` around them are places you need to provide input. 
If a field is an ID (e.g. projectID), it needs to be a number. Otherwise, it can be text.*
                            """
                        }
                    ]
                })
    return make_response("", 200)

def create(req, headline="Hey! Here is a quick guide to using `/jamaconnect create`:"):
    """create: show info for create slash command


    Arguments:
        req (Request object): Passed down to return to slack

    Returns:
        Response (object): Returned up to called funciton in route_handler
    """
    return_to_slack(req, {
                    "text": headline,
                    "attachments": [
                        {
                            "text": """
Create usage:
    \t`/jamaconnect create: dialog | project=<projectId>` brings up a dialog for
    \t\t\tthe top level items for the specified project, given the project's ID.
    \t---- or -----
    \t`/jamaconnect create: project=<projectID> | name=project name | ...` will
    \t\t\talso work, where `...` is other arguments, such as: `item=<itemID>`, or
    \t\t\t`description=your item description`.

*Note: all fields with `<...>` around them are places you need to provide input. 
If a field is an ID (e.g. projectID), it needs to be a number. Otherwise, it can be text.*
                            """
                        }
                    ]
                })
    return make_response("", 200)

def search(req, headline="Hey! Here is a quick guide to using `/jamaconnect search`:"):
    """search: show info for search slash command


    Arguments:
        req (Request object): Passed down to return to slack

    Returns:
        Response (object): Returned up to called funciton in route_handler
    """
    return_to_slack(req, {
                    "text": headline,
                    "attachments": [
                        {
                            "text": """
Search usage:
    \t`/jamaconnect search: key=<your search phrase>` will return relevant items
    \t---- or -----
    \t`/jamaconnect display: id=<itemID>` will return details of the specified item,
    \t\t\tgiven the item ID.

*Note: all fields with `<...>` around them are places you need to provide input. 
If a field is an ID (e.g. projectID), it needs to be a number. Otherwise, it can be text.*
                            """
                        }
                    ]
                })
    return make_response("", 200)