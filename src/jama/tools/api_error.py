from flask import make_response
from datetime import datetime
from slack.tools import return_to_slack

"""
Function produces and sends error message to user.

Attributes:
    None
"""

def api_error(request, command):
    """Returns an error when having trouble querying Jama API

    Args:
        request (Request object): used to pass to Slack response
        command (string): The command user have trouble with

    Raises:
        None
    """
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    print("{time}: Jama API unreachable.".format(
        time=now
    ))

    return_to_slack(request, {
                "text": "Oh no, there was an issue on our end!",
                "attachments": [
                    {
                        "text": "Please try your " + command +
                        " command again.\nIf you keep having trouble please contact the service desk."
                    }
                ]
            })
    return make_response("", 500)
