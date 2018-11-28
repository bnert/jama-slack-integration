def search_dialog():
    """
    Function uses the following format:
    https://api.slack.com/dialogs
    Returns:
        (dict): A json object to Slack for opening the search dialog.
    """

    return {
        "title": "Search by phrase",
        "submit_label": "Search",
        "callback_id": "search",
        "elements": [
            {
                "type": "text",
                "label": "Search phrase",
                "name": "key",
                "min_length": 3,
                "max_length": 50
            }
        ]
    }
