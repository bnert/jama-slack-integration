# Working With Attachments:
# https://community.jamasoftware.com/browse/articles/blogviewer?BlogKey=2f27dffc-a6ef-4573-b895-cf644cdf3119

import json
import requests
from jama import api_caller
from jama.json_factories import attachment_factory
from slack.slack_json_factories.attachment_response_json import attachment_fail_response
from slack.slack_json_factories.attachment_response_json import attachment_success_response
from slack import tools

def dialog_attachment_thread(base_url, data):
    """
    From the dialog return data, put attachment to a Jama Item. This
    function is for threading, so that the dialog can close on time.
    @params:
        base_url -> jama base_url
        data -> slack dialog payload
    """
    requests.post(data["response_url"],
                  json=dialog_attachment(base_url, data),
                  headers={"Content-Type": "application/json"})

def dialog_attachment(base_url, data):
    """
    From the dialog return data, put attachment to Jama
    @params:
        base_url -> jama base_url
        data -> slack dialog payload
    """
    item_id = data["submission"]["id"]
    description = data["submission"]["description"]
    team_id = data["team"]["id"]
    user_id = data["user"]["id"]
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
                                            project_id, item_id, file["name"], description)
        if not good:
            return massage
    return attachment_success_response(item_id, description)

def put_attachment_jama(team_id, user_id, base_url, file_url, project_id, item_id, file_name, description):
    """
    put attachment to a Jama item
    @params:
        team_id -> Slack team id, which can be found in the payload or requests
        user_id -> Slack user id, which can be found in the payload or requests
        base_url -> Jama base_url
        file_url -> The slack file download url
        project_id -> The Jama project ID of the item location
        item_id -> The Jama item ID the user want to attach their file
        file_name -> The file name
        description -> The file description
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
    file = tools.get_file(file_url)

    # upload file
    url = base_url + "/rest/latest/attachments/" + str(attachment_id) + "/file"
    response = api_caller.put_file(team_id, user_id, url, file_name, file)
    if response is None or response != 200:
        return False, attachment_fail_response(item_id, description, response)

    # attach the attachment to an item
    url = base_url + "/rest/latest/items/" + item_id + "/attachments"
    response = api_caller.post(team_id, user_id, url, {"attachment": attachment_id})
    if response is None or response["meta"]["status"] != "Created":
        return False, attachment_fail_response(item_id, description, response)
    return True, None
