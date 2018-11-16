import json
from flask import make_response
from jama import create
from slack import tools
from jama.tools import make_dict
from jama.tools import user_error
from jama.tools import api_error
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

    if "dialog" in content:
        # Create dict w/ content
        # in format dialog | project=<id>
        try:
            arg = content.split("|")
            if arg[1] != None:
                args = make_dict(arg[1])

            if "project" not in args or args["project"] == "":
                return user_error(request)

            # opens dialog, pointless to have nested function
            slack_client.api_call(
                "dialog.open",
                trigger_id=request.form["trigger_id"],
                dialog = create_fields(int(args["project"]))
            )

        except AssertionError:
            return api_error(request, "create")
            
        except Exception as err:
            # Returns error message to user & 400 status
            return user_error(request)

    else:
        try:
            content_dict = make_dict(content)
            item_create_response = create.from_text(base_url, content_dict)
            tools.return_to_slack(request, item_create_response)
        except Exception as err:
            print(err)
            return user_error(request) # Server/parse error
        
    return make_response("", 200)