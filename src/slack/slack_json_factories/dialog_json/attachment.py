import json


def attachment_dialog(payload):
    """
    Create a dialog json to get more required data from user.
    https://api.slack.com/dialogs
    @params:
        payload: Slack action payload
    """
    description = payload["message"]["text"]
    files = []
    if "files" in payload["message"]:
        for file in payload["message"]["files"]:
            if file["mode"] != "tombstone" and "url_private_download" in file:
                files.append({"name": file["name"], "url": file["url_private_download"]})
    if len(files) == 0:
        return None
    return {
        "title": "Attach file",
        "submit_label": "Submit",
        "callback_id": "attachment",
        "elements": [
            {
                "type": "text",
                "label": "Item ID",
                "name": "id"
            },
            {
                "type": "textarea",
                "label": "Description",
                "name": "description",
                "value": description
            }
        ],
        "state": json.dumps(files)
    }
