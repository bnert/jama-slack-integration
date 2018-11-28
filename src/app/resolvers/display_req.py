from flask import make_response
from jama import display
from slack import tools
from jama.tools import commands_info
from jama.tools import api_error
from slack.slack_json_factories.dialog_json import display as dialog


def resolve(base_url, content, slack_client, request):
    """Resolves which display functionality (text/dialog) to invoke.

    Args:
        base_url (string): The base Jama URL
        content (string): The item id, empty in case of dialog
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
    try:
        if content == "":
            slack_client.api_call(
                "dialog.open",
                trigger_id=request.form["trigger_id"],
                dialog=dialog.display_dialog()
            )
        else:
            display_result = display.fetch_by_id(request.form["team_id"],
                                                          request.form["user_id"],
                                                          base_url,
                                                          content
                                                          )
            tools.return_to_slack(request, display_result)
        return make_response("", 200)

    except AssertionError:
        return api_error(request, "comment")

    except Exception as err:
        print(err)
        return commands_info.comment(request, "Oh no, there was an error with your inputs!")  # Server/parse error
