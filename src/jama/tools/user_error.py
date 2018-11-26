from flask import make_response
from datetime import datetime
from slack.tools import return_to_slack

def user_error(request):
    """Returns an error when users have erroneous syntax

    Args:
        request (Request object): used to pass to Slack response

    Raises:
        None
    """
    
    return_to_slack(request, {
                    "text": "Oh no, there was an error with your inputs!",
                    "attachments": [
                        {
                            "text": "example: /jamaconnect create \n\
                            - or to open a dialog -  \n\
                            /jamaconnect create: dialog | project=<id>"
                        }
                    ]
                })
    return make_response("", 400)