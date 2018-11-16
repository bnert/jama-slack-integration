import requests
from flask import make_response
from jama import comment


def resolve_submit(base_url, payload):
    """Resolves dialog submission for creating an item in Jama.

    Arguments:
        base_url (string): The base a Jama URL
        payload (JSON Object): Payload from dialog submission

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """

    requests.post(payload["response_url"],
                  json=comment.from_dialog(base_url, payload),
                  headers={"Content-Type": "application/json"})
    return make_response("", 200)
