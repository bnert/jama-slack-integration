from flask import make_response
from slack.slack_json_factories.dialog_json import comment


def resolve_submit(payload, slack_client):
    """Resolves dialog submission for creating an item in Jama.

    Arguments:
        payload (JSON Object): Payload from dialog submission
        slack_client (SlackClient Object): to invoke slack dialog

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """

    slack_client.api_call(
        "dialog.open",
        trigger_id=payload["trigger_id"],
        dialog=comment.comment_dialog(payload)
    )
    return make_response("", 200)
