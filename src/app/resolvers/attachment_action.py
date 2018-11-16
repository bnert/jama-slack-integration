import requests
from flask import make_response
from slack.slack_json_factories.dialog_json import attachment as attach_dialog
from slack.slack_json_factories.resp_json import attachment as attach_resp


def resolve_submit(payload, slack_client):
    """Resolves dialog submission for creating an item in Jama.

    Arguments:
        payload (JSON Object): Payload from dialog submission
        slack_client (SlackClient Object): to invoke slack dialog

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """

    dialog = attach_dialog.attachment_dialog(payload)
    if dialog is None:
        requests.post(payload["response_url"],
                      json=attach_resp.file_failure_response(),
                      headers={"Content-Type": "application/json"})
        return make_response("", 200)
    else:
        slack_client.api_call(
            "dialog.open",
            trigger_id=payload["trigger_id"],
            dialog=dialog
        )
    return make_response("", 200)
