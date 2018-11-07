# Purpose of this file is to format data in a JSON object that
# Slack can handle. Each of the fucntion queries a different REST endpoint
# on the Jama instance.

import os
import json
import requests
from pprint import pprint
from flask import make_response


def get_item_dialog_fields(project_id):
    """
    @param: 
        payload_to_format -> json data
        
        Formats passed in json to an object that
        can be used for a dialogue in Slack. 
    """
    # Passes this object back to slack dialog
    return {
        "title": "JamaConnect - Create",
        "submit_label": "Submit",
        "callback_id": "jamaconnect_create_dialog",
        "elements": item_create_array(project_id)
        
    }

def item_create_array(project_id):
    """
        Creates an array, with possible values for user.
    """
    prj_data = get_jama_project_items(project_id)
    item_types = get_jama_item_types()
    jama_users = get_jama_users()

    return [
        {
            "label": "Project Item",
            "type": "select",
            "name": "projectId",
            "option_groups": [
                prj_data
            ]
                  
        },
        {
            "label": "Item Type",
            "type": "select",
            "name": "itemType",
            "options": item_types
        },
        {
            "label": "New Item Name",
            "type": "text",
            "name": "newItemName",
        },
        {
            "label": "asignee",
            "type": "select",
            "name": "asignee",
            "options": jama_users
        },
        {
            "label": "Description",
            "type": "textarea",
            "name": "description"
        }

    ]


def get_jama_project(project_id):
    """
    @params:
        id: id of the project the user wants to access
    """
    url = (os.environ['JAMA_URL'] + "/rest/latest/projects/{id}").format(id=project_id)
    resp = requests.get(url, auth=(os.environ["JAMA_USER"], os.environ["JAMA_PASS"]))
    resp_json = json.loads(resp.text)

    return resp_json


def get_jama_projects():
    """
    @params:
        none
        
        Grabs project data from REST endpoint, and then filters to format
        to send to Slack
    """
    url = os.environ['JAMA_URL'] + "/rest/latest/projects"
    resp = requests.get(url, auth=(os.environ["JAMA_USER"], os.environ["JAMA_PASS"]))
    resp_json = json.loads(resp.text)

    # Returns array of objects
    return [{
        "label": (str(obj["id"]) + ": " + obj["fields"]["name"]),
        "value": obj["id"]
        }
        for obj in resp_json["data"]
    ]


def get_jama_project_items(project_id):
    # Gets all items
    url = os.environ['JAMA_URL']

    project = get_jama_project(project_id)
    pprint(project)
    get_url = "{url}/rest/latest/items?project={id}&rootOnly=true".format(
            url=url, id=project["data"]["id"]
        )

    items_resp = requests.get(get_url, auth=(os.environ["JAMA_USER"], os.environ["JAMA_PASS"]))
    project_items = json.loads(items_resp.text)

    tmp_obj = {
    "label": project["data"]["fields"]["name"],
    "options": []
    }

    for item in project_items["data"]:
        tmp_obj["options"].append({
            "label": item["fields"]["name"],
            # value is "child.parent", similar to jwt
            "value": "{item_id}.{project_id}".format(
                item_id=item["id"], project_id=item["project"]
            ) 
        })

    return tmp_obj


def get_jama_item_types():
    """
    @params:
        none

        Returns the item types that are in the Jama instance
    """
    url = os.environ['JAMA_URL'] + "/rest/latest/itemtypes"
    resp = requests.get(url, auth=(os.environ["JAMA_USER"], os.environ["JAMA_PASS"]))
    resp_json = json.loads(resp.text)
    
    # Returns an array of objects
    return [{
            "label": item["display"], 
            "value": item["id"] 
        } 
        for item in resp_json["data"] 
    ]


def get_jama_users():
    """
    @params:
        none

        Returns current usrs in the Jama instance
    """
    url = os.environ['JAMA_URL'] + "/rest/latest/users"
    resp = requests.get(url, auth=(os.environ["JAMA_USER"], os.environ["JAMA_PASS"]))
    resp_json = json.loads(resp.text)

    return [{
            "label": item["username"],
            "value": item["id"]
        } for item in resp_json["data"]
    ]


