import threading
from flask import make_response
from jama import attachment


def resolve_submit(base_url, payload):
    """Resolves dialog submission for creating an item in Jama.

    Arguments:
        base_url (string): The base a Jama URL
        payload (JSON Object): Payload from dialog submission

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """

    thread = threading.Thread(target=attachment.dialog_attachment_thread,
                              kwargs={"base_url": base_url, "data": payload})
    thread.start()
    return make_response("", 200)
