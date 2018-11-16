import json
import os
import requests


def get_email(slack_user_id):
    """
    Given a slack user id (which is not username!), return the related user email.
    Args:
        slack_user_id (string): slack user id, which is not the slack username!
    Returns:
        (True, string): If the user can be found from slack, return True and and the email
        (False, dict) : If the given user id is not valid, return False and the error massage from slack,
                        which can be found here: https://api.slack.com/methods/users.info
    """
    found, user = get_user_info(slack_user_id)
    if found:
        return True, user["email"]
    return False, user


def get_user_info(slack_user_id):
    """
    Given a slack user id (which is not username!), return a dictionary of the related user.
    Args:
        slack_user_id(string): slack user id, which is not the slack username!
    Returns:
        (bool, dict): If the user can be found from slack, return True and and the a dictionary of the user
                      If the given user id is not valid, return False and the error massage from slack,
                      which can be found here: https://api.slack.com/methods/users.info
    """

    url = "https://slack.com/api/users.info?token=" + os.environ["SLACK_OAUTH_TOKEN"] + "&user=" + slack_user_id
    response = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = json.loads(response.text)
    if data["ok"]:
        return True, data["user"]["profile"]
    print("slack_user.get_user_info() ERROR: " + data["error"])
    return False, data
