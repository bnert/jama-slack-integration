import json
from flask import make_response
from jama import create
from slack import tools
from jama.tools import make_dict
from jama.tools import commands_info
from jama.tools import user_error
from slack.slack_json_factories import create_fields
from slack.slack_json_factories import created_item


def resolve(base_url, content, slack_client, request):
    """Resolves which create functionality (text/dialog) to invoke.

    Arguments:
        base_url (string): The base a Jama URL
        content (JSON Object): Payload from dialog submission
        slack_client (SlackClient Object): to invoke slack dialog
        request (Request Object): Request object to pass down

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.

    Raises:
        AssertionError:
            This type of exception happens when trying to gather data from
            the Jama API to return to the Slack dialog API call.
        Exception:
            On any error with parsing user data, we throw a general
            exception and return make_response() with either 400 or 500
    """
    
    if isinstance(content, int):
        # Makes sure content is an int
        # content is the projectID
        try:
            # opens dialog, pointless to have nested function
            slack_client.api_call(
                "dialog.open",
                trigger_id=request.form["trigger_id"],
                dialog = create_fields(content)
            )

        except AssertionError as err:
            print(err)
            return commands_info.create(request,
            headline="Oh no, there was an issue locating your project")
            
        except Exception as err:
            # Returns error message to user & 400 status
            print(err)
            return user_error(request)

    else:
        try:
            content_dict = make_dict(content)
            team_user_ids = {
                "team": {
                    "id": request.form["team_id"]
                },
                "user": {
                    "id": request.form["user_id"]
                }
            }
            content_dict.update(team_user_ids)
            item_create_response = create.from_text(base_url, content_dict)
            tools.return_to_slack(request, item_create_response)
        except Exception as err:
            print(err)
            return commands_info.create(request,
            headline="Oh no, we had trouble handling your data!") # Server/parse error
        
    return make_response("", 200)