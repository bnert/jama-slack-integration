import os
import json
import requests
from jama import api_caller
from flask import make_response

"""Return dialog fields for Slack from Jama API

Purpose of this file is to format data in a JSON object that
Slack can handle. Each of the fucntion queries a different REST endpoint
on the Jama instance.

Attributes:
    None
"""

def create_fields(project_id, team_id, user_id):
    """Returns dialog box
    
    Args: 
        project_id (int): ID of the project that users will get
            from Jama instance
        
    Returns:
        dict

    Raies:
        AssertionException:
            If the GET requests sent to Jama return anything but a
            status of 200, then assertion error will be thrown. 
    """
    # Passes this object back to slack dialog
    return {
        "title": "JamaConnect - Create",
        "submit_label": "Submit",
        "callback_id": "jamaconnect_create_dialog",
        "elements": _fields_array(project_id, team_id, user_id)
        
    }

# Private helper functions to interface w/ Jama API
def _fields_array(project_id, team_id, user_id):
    """Creates an array from API data.

    FUNCTION IS PRIVATE

    Returns:
        Array: this array is an object of dicts

    Raises:
        None
    """
    prj_data = _get_jama_project_items(project_id, team_id, user_id)
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
            "label": "New Item Name",
            "type": "text",
            "name": "newItemName",
        },
        {
            "label": "Description",
            "type": "textarea",
            "name": "description"
        }
    ]


def _get_jama_project(project_id, team_id, user_id):
    """GETs project

    Args:
        project_id: id of the project the user wants to access
    """
    url = (os.environ['JAMA_URL'] + "/rest/latest/projects/{id}").format(id=project_id)
    resp = api_caller.get(
        team_id, 
        user_id,
        url)

    # handled in create_req 
    assert("OK" == resp["meta"]["status"])
    return resp


def _get_jama_project_items(project_id, team_id, user_id):
    """GETs root items of a project

    Args:
        project_id: id of the project the user wants to access
    """
    # Gets all items
    url = os.environ['JAMA_URL']

    project = _get_jama_project(project_id, team_id, user_id)
    get_url = "{url}/rest/latest/items?project={id}&rootOnly=true".format(
            url=url, id=project_id
        )
    items_resp = api_caller.get(
        team_id,
        user_id,
        get_url)

    assert("OK" == items_resp["meta"]["status"])
    project_items = items_resp

    # Checks to see if childItemType is valid, if so, adds to the options
    prj_items = []
    for item in project_items["data"]:
        if "childItemType" in item:
            prj_items.append(
                {
                    "label": item["fields"]["name"],
                    # value is "child.parent", similar to jwt
                    "value": "{item_id}.{project_id}.{item_type}".format(
                        item_id=item["id"], 
                        project_id=item["project"],
                        item_type=item["childItemType"]
                        ) 
                }
            )
        else:
            prj_items.append(
                {
                    "label": item["fields"]["name"],
                    "value": "{item_id}.{project_id}.{item_type}".format(
                        item_id=item["id"], 
                        project_id=item["project"],
                        item_type=item["itemType"]
                        ) 
                }
            )

    return {
    "label": project["data"]["fields"]["name"],
    "options": prj_items
    }

