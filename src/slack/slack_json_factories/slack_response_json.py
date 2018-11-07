import json


def slack_resp_json(payload_to_format):
    """
    Function takes in a JSON object, and uses the following format:
      https://api.slack.com/docs/messages#composing_messages
    found in the above document.

    Returns created JSON object, then is sent back to Slack.
    """
    try:
        resp = {
            "text": "From jama:",
            "attachments": [
                {
                    "title": "Name",
                    # name from Jama JSON
                    "text": payload_to_format["data"][0]["fields"]["name"]
                },
                {
                    "title": "ID",
                    "text": payload_to_format["data"][0]["id"]
                },
                {
                    "title": "Project",
                    "text": payload_to_format["data"][0]["documentKey"]
                },
                {
                    "title": "Description",
                    "text": payload_to_format["data"][0]["fields"]["description"]
                },
                {
                    "title": "Url",
                    "text": payload_to_format["links"]["data.project"]["href"]
                }
            ]
        }

        print(json.dumps(resp, indent=4))

        return resp
    except Exception as err:
        print("ERROR IN: slack_repsonse_json.py")
        print(err)
        return {"text": ("Error in %s" % err)}
