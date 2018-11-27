import requests
from jama import search


def resolve_submit(base_url, payload):
    """Resolves dialog submission for creating an item in Jama.

    Arguments:
        base_url (string): The base a Jama URL
        payload (JSON Object): Payload from dialog submission

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """

    requests.get(payload["response_url"],
                  json=search.from_dialog(base_url, payload),
                  headers={"Content-Type": "application/json"})
    return make_response("", 200)
