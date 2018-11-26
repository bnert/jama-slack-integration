import json

"""Returns url to access created item

This function packages the response from Jama after and item
has either been created or attempted to be created. If there is an error
in the post request to the Jama instance, then this function will notify the
user. If the post request was successful, then the function will return the
newly created url to the user.

Attributes:
    None
"""


def resp_json(payload_to_format, project_id):
    """Packages a response to send to slack

    Function takes in a JSON object, and uses the following format at
    the following link:
        https://api.slack.com/docs/messages#composing_messages

    Returns: 
        created JSON object, then is sent back to Slack.
    
    Raises:
        Exception:
            If object was not created, then excpetion is raised and
            and error message is sent to the user
    """
    try:
        url_to_new_item = "https://capstone-test.jamacloud.com/perspective.req#/items/{item_id}?projectId={prj_id}".format(
            item_id=str(payload_to_format["meta"]["id"]), prj_id=project_id
        )

        return {
            "text": payload_to_format["meta"]["status"],
            "attachments": [
                {
                    "title": "New Item ID",
                    "text": payload_to_format["meta"]["id"]  # ID from Jama JSON
                },
                {
                    "title": "Url to new item",
                    "text": url_to_new_item
                }
            ]
        }

    except Exception as err:
        print(err)
        return {
            "text": "Oh no, there was an error creating the object",
            "attachments": [
                {
                    "text": """Example usage of `/jamaconnect create`:
\t`/jamaconnect create: <projectId>` brings up a dialog for
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
        }
