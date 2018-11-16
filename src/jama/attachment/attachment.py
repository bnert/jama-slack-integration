# Working With Attachments:
# https://community.jamasoftware.com/browse/articles/blogviewer?BlogKey=2f27dffc-a6ef-4573-b895-cf644cdf3119

import json
import requests
from jama import api_caller
from jama.json_factories import attachment_factory
from slack.slack_json_factories.resp_json.attachment import attachment_fail_response
from slack.slack_json_factories.resp_json.attachment import attachment_success_response
from slack import tools
from jama import tools as jama_tools


def dialog_attachment_thread(base_url, data):
    """
    From the dialog return data, put attachment to a Jama Item. This
    function is for threading, so that the dialog can close on time.
    Args:
        base_url (string): jama base_url
        data (dict): slack dialog payload
    Returns:
        None
    """
    requests.post(data["response_url"],
                  json=dialog_attachment(base_url, data),
                  headers={"Content-Type": "application/json"})


def dialog_attachment(base_url, data):
    """
    From the dialog return data, put attachment to Jama
    Args:
        base_url (string): jama base_url
        data (dict): slack dialog payload
    Returns:
        (dict): A JSON object of the task's status for Slack User
    """
    item_id = data["submission"]["id"]
    description = data["submission"]["description"]
    team_id = data["team"]["id"]
    user_id = data["user"]["id"]
    if api_caller.is_using_oauth():
        header = ""
    else:
        header = jama_tools.prepare_writer_info(team_id, user_id, base_url, False)

    # get project id
    url = base_url + "/rest/latest/items/" + item_id
    response = api_caller.get(team_id, user_id, url)
    if response is None or response["meta"]["status"] != "OK":
        return attachment_fail_response(item_id, description, response)
    else:
        project_id = str(response["data"]["project"])

    # upload file
    file_list = json.loads(data["state"])
    for file in file_list:
        good, massage = put_attachment_jama(team_id, user_id, base_url, file["url"],
                                            project_id, item_id, file["name"], header + description)
        if not good:
            return massage
    return attachment_success_response(item_id, description)


def put_attachment_jama(team_id, user_id, base_url, file_url, project_id, item_id, file_name, description):
    """
    put attachment to a Jama item
    Args:
        team_id (string): Slack team id, which can be found in the payload or requests
        user_id (string):Slack user id, which can be found in the payload or requests
        base_url (string): Jama base_url
        file_url (string): The slack file download url
        project_id (string): The Jama project ID of the item location
        item_id (string): The Jama item ID the user want to attach their file
        file_name (string): The file name
        description (string): The file description
    Returns:
        (bool, dict): The put_attachment is success or not. and A JSON object of the task's status for Slack User
    """
    # create attachment slot and get a attachment id
    create_att_json = attachment_factory.generate_attachment(file_name, description)
    url = base_url + "/rest/latest/projects/" + project_id + "/attachments"
    response = api_caller.post(team_id, user_id, url, create_att_json)
    if response is None or response["meta"]["status"] != "Created":
        return False, attachment_fail_response(item_id, description, response)
    else:
        attachment_id = response["meta"]["id"]

    # download file
    file_data = tools.get_file(file_url)

    # upload file
    url = base_url + "/rest/latest/attachments/" + str(attachment_id) + "/file"
    file = {"file": (file_name, file_data)}
    response = api_caller.put_file(team_id, user_id, url, file)
    if response is None or response != 200:
        return False, attachment_fail_response(item_id, description, response)

    # attach the attachment to an item
    url = base_url + "/rest/latest/items/" + item_id + "/attachments"
    response = api_caller.post(team_id, user_id, url, {"attachment": attachment_id})
    if response is None or response["meta"]["status"] != "Created":
        return False, attachment_fail_response(item_id, description, response)
    return True, None
