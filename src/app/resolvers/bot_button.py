from flask import make_response
from slack.slack_json_factories.dialog_json import comment


def resolve_submit_project(payload, slack_client):
    """Resolves slack bot button submission for project.

    Arguments:
        payload (JSON Object): Payload from dialog submission
        slack_client (SlackClient Object): to invoke slack dialog

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """
    print(payload)
    if payload["actions"][0]["name"] == "comment":
        slack_client.api_call(
            "dialog.open",
            trigger_id=payload["trigger_id"],
            dialog=comment.comment_dialog(payload)
        )
    return make_response("", 200)


def resolve_submit_item(payload, slack_client):
    """Resolves slack bot button submission for item.

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
