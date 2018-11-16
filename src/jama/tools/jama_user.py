from jama import api_caller


def get_user_by_email(base_url, slack_team_id, slack_user_id, email):
    """
    Using given email address to fin a Jama user information
    Args:
        base_url (string): The Jama workspace base_url
        email (string): email of the user
        slack_team_id (string): The slack team ID
        slack_user_id (string): The slack User ID, which is not the username!
        Returns:
             (bool, dict): If user is found, return true and a dictionary of data the Jama user.
                           If user is not found, return false and a dictionary of error massage.
    """
    response = api_caller.get(slack_team_id, slack_user_id, base_url + "/rest/latest/users?email=" + email)
    if response["meta"]["pageInfo"]["totalResults"] == 0:
        return False, {"error": "NO_SUCH_USER"}
    elif response["meta"]["pageInfo"]["totalResults"] >= 2:
        return False, {"error": "ERROR_MORE_THEN_ONE_USER"}
    return True, response["data"][0]
