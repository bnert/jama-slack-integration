def display_dialog():
    """
    Function uses the following format:
    https://api.slack.com/dialogs
    Returns:
        (dict): A json object to Slack for opening the display dialog.
    """

    return {
        "title": "Display by ID",
        "submit_label": "Display",
        "callback_id": "display",
        "elements": [
            {
                "type": "text",
                "label": "Item ID",
                "name": "id",
                "min_length": 4,
                "max_length": 4
            }
        ]
    }
