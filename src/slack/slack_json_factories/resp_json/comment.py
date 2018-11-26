from slack import tools


def comment_response(item_id, comment, response=None):
    """
    Function takes in an item id, comment content, and a JSON object to create a message for slack user.
    json for slack:
    https://api.slack.com/docs/messages#composing_messages
    Args:
        item_id (string): A string format item id, which is the item user want to comment
        comment (string): the content user want to put into the comment
        response (dict): The response of jama API post /comment. This is not required if there is no response
                         from Jama. In this case, this function would assume the API calling process is stopped
                         because of invalid user input and create an error message.
    Returns:
        (dict): A JSon object of a slack message, which shows the status of the Jama comment.
    """
    # Base json for returning to slack
    resp = {
        "text": "",
        "attachments": [
            {
                "title": "Comment content",
                "text": comment
            },
            {
                "color": "danger",
                "title": "",
                "text": ""
            }
        ]
    }

    # No given response means no jama response, which means the posting process is stop by our code
    # because of the input. This function should check the input and give proper response.
    if response is None:
        resp["text"] = "Bad Request"
        resp["attachments"][1]["title"] = "Error Message"
        if tools.string_to_int(item_id) < 0:
            resp["attachments"][1]["text"] += "The item id `" + item_id + "` is invalid.\n"
        if comment is "":
            resp["attachments"][0]["text"] = "(Empty)"
            resp["attachments"][1]["text"] += "Comment text cannot be blank.\n"
        resp["attachments"][1]["text"] += "Please check your input again."
        if comment is not "" and tools.string_to_int(item_id) >= 0:
            resp["attachments"][1]["text"] += "User's Oauth token is invalid or server is down. Please check again."
        return resp

    # Base on the return data from Jama, give user some detail of the posting result.
    resp["text"] = response["meta"]["status"]
    if response["meta"]["status"] == "Created":
        resp["text"] = "Successfully created comment to item (id: " + item_id + ")"
        resp["attachments"][1]["color"] = "good"
        resp["attachments"][1]["title"] = "Url to commented item"
        resp["attachments"][1]["text"] = "https://capstone-test.jamacloud.com/perspective.req#/items/" + item_id
    elif response["meta"]["status"] == "Not Found":
        resp["attachments"][1]["title"] = "Error Message"
        resp["attachments"][1]["text"] = "The item id `" + item_id + "` is not found. Please check again."
    else:
        resp["attachments"][1]["title"] = "Error Message"
        resp["attachments"][1]["text"] = "Error message from Jama: " + response["meta"]["message"]
    return resp
