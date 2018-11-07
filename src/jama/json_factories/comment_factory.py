def generate_comment(stored_location, comment_body):
    """
    Purpose of file is to produce a JSON object for an comment.
    Pulled JSON object from Jama SwaggeUI instance on creating an comment.
    @params:
        stored_location: The item id which should be comment
        comment_body -> The contain of the comment
    """
    return {
        "body": {
            "text": comment_body,
        },
        "commentType": "GENERAL",
        "location": {
            "item": stored_location
        }
    }