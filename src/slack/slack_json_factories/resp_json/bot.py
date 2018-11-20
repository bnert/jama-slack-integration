import json

def project_response(projectID, project_name):
    """Packages a response attachments to send to slack

    Function takes in a projectID, and uses the following format at
    the following links:
        https://api.slack.com/docs/messages#composing_messages
        https://api.slack.com/docs/message-attachments

    Returns:
        created JSON object, then is sent back to Slack.

    Raises:
        Exception:
            If object was not created, then excpetion is raised and
            and error message is sent to the user
    """
    return json.dumps([
        {
            "fallback": str(projectID) + ": " + project_name,
            "callback_id": "bot_project",
            "fields": [
                {
                    "title": "Project",
                    "value": str(projectID) + ": " + project_name + " :smiley:",
                    "short": False
                }
            ],
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "create",
                    "text": "Create",
                    "type": "button",
                    "value": projectID
                },
                {
                    "name": "comment",
                    "text": "Comment",
                    "type": "button",
                    "value": projectID
                },
            ]
        }
    ])


def item_response(itemID, item_name):
    """Packages a response attachments to send to slack

    Function takes in a itemID, and uses the following format at
    the following links:
        https://api.slack.com/docs/messages#composing_messages
        https://api.slack.com/docs/message-attachments

    Returns:
        created JSON object, then is sent back to Slack.

    Raises:
        Exception:
            If object was not created, then excpetion is raised and
            and error message is sent to the user
    """
    return json.dumps([
        {
            "fallback": str(itemID) + ": " + item_name,
            "callback_id": "bot_item",
            "color": "#3AA3E3",
            "fields": [
                {
                    "title": "Item",
                    "value": str(itemID) + ": " + item_name + " :simple_smile:",
                    "short": False
                }
            ],
            "attachment_type": "default",
            "actions": [
                {
                    "name": "comment",
                    "text": "Comment",
                    "type": "button",
                    "value": itemID
                },
            ]
        }
    ])
