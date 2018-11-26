"""
This file contains Jama-side OAuth functions. You would use it to store a Slack
user's Jama OAuth credentials and retrieve the same.
"""
import requests
from flask import request, Response
import json
import os
import mysql.connector
from mysql.connector import errorcode
from slack import tools

def receive_dialog(payload):
    """
    Processes a submitted oauth dialog

    @params:
        payload -> The received json payload
    """
    try:
        teamID = payload["team"]["id"]
        userID = payload["user"]["id"]
        clientID = payload["submission"]["client_id"]
        client_secret = payload["submission"]["client_secret"]
    except err:
        print(err)
        return "Internal server error"
    return add_credentials(teamID, userID, clientID, client_secret)

def add_credentials(teamID, userID, clientID, client_secret):
    """
    Given a slack teamID and userID and a Jama client ID and secret, adds that
    information to the database for later use. Returns an message for the slack
    user detailing the success or failure of the operation.

    @params:
        teamID -> The user's Slack team ID
        userID -> The user's Slack user ID
        clientID -> The user's Jama client ID
        client_secret -> The user's Jama client secret
    """
    try:
        cnx = mysql.connector.connect(user=os.environ["DB_USER"],
                                      password=os.environ["DB_PASS"],
                                      host=os.environ["DB_HOST"],
                                      database=os.environ["DB_NAME"])
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        print("Could not make a connection to the database")
        return "Operation failed (internal server error)"
    except KeyError:
        print("No DB connection information was provided; aborting")
        return "Operation failed; OAuth is not enabled on this server"

    query_team = ("INSERT IGNORE INTO Team (team_id) "
                 "VALUES (%s)")
    query_user = ("INSERT INTO User (team_id, user_id, "
                 "                jama_client_id, jama_client_secret) "
                 "VALUES (%s, %s, %s, %s) "
                 "ON DUPLICATE KEY UPDATE jama_client_id = %s, "
                 "                        jama_client_secret = %s")
    try:
        cursor.execute(query_team, (teamID,))
        cursor.execute(query_user, (teamID, userID,
                                    clientID, client_secret,
                                    clientID, client_secret))
        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as e:
        print("Database error:")
        print(e)
        return "Operation failed (internal server error)"

    if get_access_token(teamID, userID) is None:
        return "Invalid Client ID and/or Client Secret (Jama rejected authentication)"

    return "Added/Replaced ID and Secret"

def get_access_token(teamID, userID):
    """
    Given a slack teamID and userID, returns (using OAuth) a temporary access
    token used for authentication with Jama. Returns None if the user does not
    have jama credentials stored with this application.
    Exceptions:
        Throws a RuntimeError exception if something goes wrong that should not
    in normal operation (DB problem, jama connection error).
        Throws a KeyError exception if a critical environment variable
    (JAMA_URL, any of the DB vars) could not be found.

    @params:
        teamID -> The user's Slack team ID
        userID -> The user's Slack user ID
    """
    creds = get_oauth_credentials(teamID, userID)
    if creds is None:
        return None
    (clientID, client_secret) = creds
    url = os.environ["JAMA_URL"] + "/rest/oauth/token"
    try:
        response = requests.post(url, auth=(clientID, client_secret),
                                 data={"grant_type": "client_credentials"})
    except:
        raise RuntimeError("Connection error with Jama")
    json_response = json.loads(response.text)
    return json_response.get("access_token", None)

def get_oauth_credentials(teamID, userID):
    """
    Note: This is intended for internal use by the OAuth module. I don't know
    how to express this in code.
    Given a slack teamID and userID, returns the user's Jama client ID and
    secret for use with OAuth. Returns None if the user's ID and secret do not
    exist in the database.
    Exceptions:
        Throws a RuntimeError exception if there is a problem that should not
    occur during normal operation (such as a failed DB connection, or multiple
    rows being returned (the latter would be a problem because the DB
    constraints should restrict such a thing from happening.))
        Throws a KeyError exception if database information has not been entered
    in the config file.

    @params:
        teamID -> The user's Slack team ID
        userID -> The user's Slack user ID
    """
    try:
        cnx = mysql.connector.connect(user=os.environ["DB_USER"],
                                      password=os.environ["DB_PASS"],
                                      host=os.environ["DB_HOST"],
                                      database=os.environ["DB_NAME"])
    except mysql.connector.Error as err:
        raise RuntimeError("Could not make a connection to the database")

    query = ("SELECT jama_client_id, jama_client_secret "
             "FROM User "
             "WHERE team_id = %s AND user_id = %s")
    cursor = cnx.cursor()
    cursor.execute(query, (teamID, userID))
    result = cursor.fetchone()
    second_result = cursor.fetchone()
    cursor.close()
    cnx.close()
    if result is None:
        return None
    elif second_result is not None:
        raise RuntimeError("mysql returned more than one row")
    return result
