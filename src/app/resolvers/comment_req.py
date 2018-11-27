from flask import make_response
from jama import comment
from slack import tools
from jama.tools import make_dict
from jama.tools import commands_info
from jama.tools import api_error
from slack.slack_json_factories.dialog_json import comment as dialog
from jama.comment.comment import user_project_id_list


def resolve(base_url, content, slack_client, request):
    """Resolves which comment functionality (text/dialog) to invoke.

    Args:
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
    global user_project_id_list
    try:
        slack_team_id = request.form["team_id"]
        slack_user_id = request.form["user_id"]
        if content == "":
            if (slack_team_id, slack_user_id) in user_project_id_list:
                del user_project_id_list[(slack_team_id, slack_user_id)]
            slack_client.api_call(
                "dialog.open",
                trigger_id=request.form["trigger_id"],
                dialog=dialog.comment_dialog()
            )
        else:
            args = make_dict(content)
            if "id" not in args or "comment" not in args:
                return commands_info.comment(request, "Oh no, there was an error with your inputs!")

            comment_create_response = comment.from_inline(slack_team_id,
                                                          slack_user_id,
                                                          base_url,
                                                          args
                                                          )
            tools.return_to_slack(request, comment_create_response)
        return make_response("", 200)

    except AssertionError:
        return api_error(request, "comment")

    except Exception as err:
        print(err)
        return commands_info.comment(request, "Oh no, there was an error with your inputs!")  # Server/parse error
