from flask import make_response
from slack.slack_json_factories.dialog_json import comment
from slack.slack_json_factories import create_fields
from slack import tools
from jama.comment.comment import user_project_id_list


def resolve_submit_project(payload, slack_client):
    """Resolves slack bot button submission for project.

    Arguments:
        payload (JSON Object): Payload from dialog submission
        slack_client (SlackClient Object): to invoke slack dialog

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """

    global user_project_id_list
    if payload["actions"][0]["name"] == "comment":
        slack_team_id = payload["team"]["id"]
        slack_user_id = payload["user"]["id"]
        if (slack_team_id, slack_user_id) in user_project_id_list:
            del user_project_id_list[(slack_team_id, slack_user_id)]
        slack_client.api_call(
            "dialog.open",
            trigger_id=payload["trigger_id"],
            dialog=comment.comment_dialog(payload)
        )

    elif payload["actions"][0]["name"] == "create":
        content = payload["actions"][0]["value"]
        content = tools.string_to_int(content)
        slack_client.api_call(
            "dialog.open",
            trigger_id=payload["trigger_id"],
            dialog = create_fields(content)
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

    global user_project_id_list
    slack_team_id = payload["team"]["id"]
    slack_user_id = payload["user"]["id"]
    if (slack_team_id, slack_user_id) in user_project_id_list:
        del user_project_id_list[(slack_team_id, slack_user_id)]
    slack_client.api_call(
        "dialog.open",
        trigger_id=payload["trigger_id"],
        dialog=comment.comment_dialog(payload)
    )
    return make_response("", 200)
