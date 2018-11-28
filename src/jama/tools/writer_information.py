from jama import tools
from slack import slack_user


def prepare_writer_info(slack_team_id, slack_user_id, jama_base_url, use_at_user):
    """
    Using the requester's Slack email to find the Jama information of the requester. Then prepare
    a piece of html code that we can post on Jama to reflect the requester.
    Args:
        slack_team_id (string): Slack team id
        slack_user_id (string): Slack user id, which is NOT the Slack username!
        jama_base_url (string): The Jama workspace base_url
        use_at_user (bool): The Jama workspace base_url
    Returns:
        (string): A piece of html code, which should be use at the head of a created item or comment.
    """

    # to find the user's Jama user
    found, slack_user_info = slack_user.get_user_info(slack_user_id)
    if found:
        found, jama_user_info = tools.get_user_by_email(jama_base_url,
                                                        slack_team_id,
                                                        slack_user_id,
                                                        slack_user_info["email"]
                                                        )
        if found:
            # prepare a html code for posting on Jama
            if use_at_user:
                return "Jama user " + prepare_jama_mention(jama_user_info) + " post:\n"
            else:
                return "Jama user @" + jama_user_info["username"] + " post:\n"
        # prepare a html code for posting on Jama
        return "Slack user @" + slack_user_info["display_name"] + " ( " + slack_user_info["email"] + " ) post:\n"
    return "Unknown Slack user id " + slack_user_id + " post:\n"


def prepare_jama_mention(jama_user_info):
    """
    Make a html block of jama's @mention functionality
    Args:
        jama_user_info(dict): The user data get from jama's REST API /users
    Returns:
        (string): A piece of html code for @user
    """
    full_name = jama_user_info["firstName"] + " " + jama_user_info["lastName"]
    user_id = str(jama_user_info["id"])
    return "<span contenteditable='false' data-j-object='User:" + user_id + "' data-j-type='User' data-j-name='" +\
           full_name + "' data-j-key='" + jama_user_info["username"] + "' data-j-id='" + user_id +\
           "' class='js-at-mention-key at-mention-key js-at-mention-user at-mention-user'>" + full_name + "</span>"
