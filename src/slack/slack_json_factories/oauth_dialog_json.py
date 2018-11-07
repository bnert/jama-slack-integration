def oauth_dialog():
    """
    Returns JSON object for the oauth dialog then is sent to Slack.
    """
    return {
        "title": "OAuth registration",
        "submit_label": "Submit",
        "callback_id": "oauth",
        "elements": [
            {
                "type": "text",
                "label": "Client ID",
                "name": "client_id"
            },
            {
                "type": "text",
                "label": "Client Secret",
                "name": "client_secret"
            }
        ]
    }

