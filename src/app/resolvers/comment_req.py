from flask import make_response
from jama import comment
from slack import tools
from jama.tools import user_error
from slack.slack_json_factories.dialog_json import comment as dialog


def resolve(base_url, content, slack_client, request):
    """Resolves which create functionality (text/dialog) to invoke.

    Args:
        base_url (string): The base a Jama URL
        content (JSON Object): Payload from dialog submission
        slack_client (SlackClient Object): to invoke slack dialog
        request (Request Object): Request object to pass down

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.

    Raises:
        Exception:
            On any error with parsing user data, we throw a general
            exception and return make_response() with either 400 or 500
    """
    try:
        if content == "":
            slack_client.api_call(
                "dialog.open",
                trigger_id=request.form["trigger_id"],
                dialog=dialog.comment_dialog()
            )
        else:
            comment_create_response = comment.from_inline(request.form['team_id'],
                                                          request.form['user_id'],
                                                          base_url,
                                                          content)
            tools.return_to_slack(request, comment_create_response)
        return make_response("", 200)
    except Exception as err:
        print(err)
        return user_error(request)  # Server/parse error
