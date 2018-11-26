def comment_dialog(data=None):
    """
    Function takes in a JSON object, and uses the following format:
    https://api.slack.com/dialogs
    Returns created JSON object, then is sent back to Slack.
    """
    text = ""
    state = ""
    project_holder = None
    item_holder = None
    if data is not None:
        if data["type"] == "message_action":
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

        if data["type"] == "interactive_message":
            if data["callback_id"] == "bot_project":
                label = data["original_message"]["attachments"][0]["fallback"]
                project_holder = [
                    {
                        "label": label,
                        "value": data["actions"][0]["value"]
                    }
                ]
                state = data["actions"][0]["value"]
            elif data["callback_id"] == "bot_item":
                label = data["original_message"]["attachments"][0]["fallback"]
                item_holder = [
                    {
                        "label": label,
                        "value": data["actions"][0]["value"]
                    }
                ]
    return {
        "title": "JamaConnect - Comment",
        "submit_label": "Submit",
        "callback_id": "comment",
        "elements": [
            {
                "label": "Search Projects:",
                "type": "select",
                "name": "project",
                "optional": "true",
                "data_source": "external",
                "selected_options": project_holder
            },
            {
                "label": "Project ID:",
                "type": "select",
                "name": "project_id",
                "optional": "true",
                "data_source": "external",
                "selected_options": project_holder
            },
            {
                "label": "Item ID or Name:",
                "type": "select",
                "name": "item",
                "data_source": "external",
                "min_query_length": 0,
                "selected_options": item_holder
            },
            {
                "type": "textarea",
                "label": "Comment",
                "name": "comment",
                "value": text
            }

        ],
        "state": state
    }
