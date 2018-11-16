import os
import requests
import json
from flask import request, make_response
from app import app
from app import route_handler as rt_handle


"""
This module handles the "intake" of requests to the server.
The requests are then passed off the route_handler.py where arguments
are then parsed and passed off to other packages for the different
functionalities: comment, create, search.

All verification for reqets is made at this level.

Attributes:
    base_url (String): Module level variable pulls in environment
        variable (JAMA_URL). which is the url of the specified Jama
        instance.

    url_rule (String): Variable uses environment variable which stands
        for the main/base url slug.

        Example: URL_RULE="/jama"
"""

base_url = os.environ['JAMA_URL']
url_rule = os.environ['URL_RULE']


@app.route(url_rule + "/dialog", methods=['GET', 'PUT', 'POST'])
def jama_dialog():
    """API intake for dialog submissions from Slack.

    Passes json payload off to route_handler, otherwise an error is
    thrown.

    Args:
        None

    Returns:
        Response Class object
    """
    if not rt_handle.verify_req(request):
        return make_response("", 401)
    print("DIALOG")
    try:
        submit_payload = json.loads(request.form['payload'])
        return rt_handle.resolve_dialog_submit(base_url, submit_payload)

    except Exception as err:
        print(err)
        return make_response("", 500)

@app.route(url_rule + '/menu', methods=['GET', 'PUT', 'POST'])
def jama_menu():
    """API intake to pass off dynamic dialog data to Slack.

    Passes json payload off to route_handler, otherwise an error is
    thrown.

    Args:
        None

    Returns:
        Response Class object
    """
    if not rt_handle.verify_req(request):
        return make_response("", 401)
    print("MENU")
    try:
        submit_payload = json.loads(request.form["payload"])
        return rt_handle.resolve_menu_req(base_url, submit_payload)

    except Exception as err:
        print(err)
        return make_response("", 500)

@app.route(url_rule, methods=['GET', 'PUT', 'POST'])
def jama():
    """API intake to pass off dynamic dialog data to Slack.

    Passes json payload off to route_handler, otherwise an error is
    thrown.

    Args:
        None

    Returns:
        Response Class object
    """

    if not rt_handle.verify_req(request):
        return make_response("", 401)

    return rt_handle.resolve_jama_req(base_url, request)
