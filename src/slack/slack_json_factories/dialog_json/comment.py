def comment_dialog(data=None):
    """
    Function takes in a JSON object, and uses the following format:
    https://api.slack.com/dialogs
    Args:
        data(dict): Slack action payload
    Returns:
        (dict): A json object to Slack for opening the dialog.
    """
    text = ""
    if data is not None:
        text = data["message"]["text"] + "\n"

        # get attachment images from the massage
        if "attachments" in data["message"]:
            text += "Attachments:\n"
            for att in data["message"]["attachments"]:
                text += att["title"] + ":\n"
                if "image_url" in att:
                    text += att["image_url"] + "\n"

        # get files from the massage
        if "files" in data["message"]:
            text += "Attach files:\n"
            for file in data["message"]["files"]:
                text += file["title"] + ":\n"
                text += file["url_private"] + "\n"
    return {
        "title": "Add comment",
        "submit_label": "Submit",
        "callback_id": "comment",
        "elements": [
            {
                "label": "Project Reference ONLY:",
                "type": "select",
                "name": "project",
                "optional": "true",
                "data_source": "external"
            },
            {
                "label": "Project ID:",
                "type": "select",
                "name": "project_id",
                "optional": "true",
                "data_source": "external"
            },
            {
                "label": "Item ID or keyword:",
                "type": "select",
                "name": "item",
                "data_source": "external",
                "min_query_length": 0,
            },
            {
                "type": "textarea",
                "label": "Comment",
                "name": "comment",
                "value": text
            }

        ]
    }
