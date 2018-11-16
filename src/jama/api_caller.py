from jama import oauth
import os
import json
import requests


def is_using_oauth():
    return "DB_HOST" in os.environ


def post(team_id, user_id, url, payload):
    """
    Using post method to get data from given Jama url
    Args:
        team_id (string): Slack team ID
        user_id (string): Slack User ID
        url (string): Jama API url
        payload (dict): The dictionary of payload wants to be sent to the url
    Returns:
        (dict): Data get from Jama
        (None): If fail to get Jama OAuth, return None
    """
    if is_using_oauth():
        token = oauth.get_access_token(team_id, user_id)
        if token is None:
            return None
        header_list = {
            "content-type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = requests.post(url, json=payload, headers=header_list)
    else:
        response = requests.post(url, json=payload, auth=(os.environ["JAMA_USER"], os.environ["JAMA_PASS"]))
    return json.loads(response.text)


def get(team_id, user_id, url):
    """
    Using get method to get data from given Jama url
    Args:
        team_id (string): Slack team ID
        user_id (string): Slack User ID
        url (string): Jama API url
    Returns:
        (dict): Data get from Jama
        (None): If fail to get Jama OAuth, return None
    """
    if is_using_oauth():
        token = oauth.get_access_token(team_id, user_id)
        if token is None:
            return None
        header_list = {
            "content-type": "application/json",
            "Authorization": "Bearer " + token
        }
        response = requests.get(url, headers=header_list)
    else:
        response = requests.get(url, auth=(os.environ["JAMA_USER"], os.environ["JAMA_PASS"]))
    return json.loads(response.text)


def put_file(team_id, user_id, url, file_data):
    """
    Using put method to get data from given url
    Args:
        team_id (string): Slack team ID
        user_id (string): Slack User ID
        url (string): Jama API url
        file_data (dict): The file name and file data wants to be sent to the url
    Returns:
        (dict): Data get from Jama
        (None): If fail to get Jama OAuth, return None
    """
    if is_using_oauth():
        token = oauth.get_access_token(team_id, user_id)
        if token is None:
            return None
        response = requests.put(url, files=file_data, headers={"Authorization": "Bearer " + token})
    else:
        response = requests.put(url, files=file_data, auth=(os.environ["JAMA_USER"], os.environ["JAMA_PASS"]))
    return response.status_code
