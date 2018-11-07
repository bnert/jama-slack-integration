from flask import make_response
from datetime import datetime
from slack.tools import return_to_slack

def user_error(request):
    """Returns an error when users have erranous syntax

    Args:
        request (Request object): used to pass to Slack response

    Raises:
        None
    """
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    print("{time}: Jama API ureachable.".format(
        time=now
    ))
    return_to_slack(request, {
                    "text": "Oh no, there was an error with your inputs!",
                    "attachments": [
                        {
                            "text": "example: /jamaconnect create: project=49 | name=project name | ...\n\
                            - or to open a dialog -  \n\
                            /jamaconnect create: dialog | project=<id>"
                        }
                    ]
                })
    return make_response("", 400)