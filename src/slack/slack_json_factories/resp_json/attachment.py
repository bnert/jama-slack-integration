def attachment_fail_response(item_id, description, response=None):
    """
    Function takes in an item id, comment content, and a JSON object to create a message for Slack user.
    See below link for documentation:
    https://api.slack.com/docs/messages#composing_messages
    Args:
        item_id (string): A string format item id, which is the item user want to attach file.
        description (string): The content user want to put into the attachment description.
        response (dict, None): The response of jama API. This is not required if everything run well In this case,
                               this function would assume the API calling process has an Oauth token error.
    Returns:
        (dict): A JSON obj to Slack, which expend the failure.
    """
    # Base json for returning to slack
    resp = {
        "text": "Can not upload attachment to item (id: " + item_id + ")",
        "attachments": [
            {
                "title": "Description content",
                "text": description
            },
            {
                "color": "danger",
                "title": "",
                "text": ""
            }
        ]
    }
    # Base on the return data from Jama, give user some detail of the posting result.
    if response is None:
        resp["attachments"][1]["title"] = "Error Message"
        resp["attachments"][1]["text"] = "User's Oauth token is invalid or server is down. Please check again."
    else:
        resp["text"] = "Error"
        resp["attachments"][1]["title"] = "Error Message from Jama"
        resp["attachments"][1]["text"] = "Status: " + response["meta"]["status"] +\
                                         "\nMessage: " + response["meta"]["message"]
    return resp


def attachment_success_response(item_id, description):
    """
    Function takes in an item id, comment content, and a JSON object to create a message for Slack user.
    See below link for documentation:
    https://api.slack.com/docs/messages#composing_messages
    Args:
        item_id (string): A string format item id, which is the item user want to attach file.
        description (string): The content user want to put into the attachment description.
    Returns:
        (dict): A JSON obj to Slack, which has the item URL and the information
    """
    return {
        "text": "Successfully upload attachment to item (id: " + item_id + ")",
        "attachments": [
            {
                "title": "Description content",
                "text": description
            },
            {
                "color": "good",
                "title": "Url to commented item",
                "text": "https://capstone-test.jamacloud.com/perspective.req#/items/" + item_id
            }
        ]
    } 


def file_failure_response():
    """
    An error message for Slack user to expand the message they choose
    contains file that cannot be uploaded. See below link for documentation:
    https://api.slack.com/docs/messages#composing_messages
    Returns:
        (dict): A JSON obj to Slack, which expend the failure.
    """
    return {
        "text": "Error",
        "attachments": [
            {
                "color": "danger",
                "title": "Error Message",
                "text": "The message you choose has no file or the file cannot be uploaded. Please check again."
            }
        ]
    }
