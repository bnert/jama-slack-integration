from jama import oauth
import json
import requests

def post(team_id, user_id, url, payload):
    """
    Using post method to get data from given Jama url
    @param:
        team_id -> Slack team ID
        user_id -> Slack User ID
        url -> Jama API url
        payload -> The dictionary of payload wants to be sent to the url
    """
    token = oauth.get_access_token(team_id, user_id)
    if token is None:
        return None
    header_list = {
        "content-type": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.post(url, json=payload, headers=header_list)
    return json.loads(response.text)

def get(team_id, user_id, url):
    """
    Using get method to get data from given Jama url
    @param:
        team_id -> Slack team ID
        user_id -> Slack User ID
        url -> Jama API url
    """
    token = oauth.get_access_token(team_id, user_id)
    if token is None:
        return None
    header_list = {
        "content-type": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.get(url, headers=header_list)
    return json.loads(response.text)

def put_file(team_id, user_id, url, file_name, file_data):
    """
    Using put method to get data from given url
    @param:
        team_id -> Slack team ID
        user_id -> Slack User ID
        url -> Jama API url
        file_name -> The file name of the file
        file_data -> The file data wants to be sent to the url
    """
    token = oauth.get_access_token(team_id, user_id)
    if token is None:
        return None
    response = requests.put(url, files={"file": (file_name, file_data)}, headers={"Authorization": "Bearer " + token})
    return response.status_code
