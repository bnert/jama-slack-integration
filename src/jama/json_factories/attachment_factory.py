def generate_attachment(name, description):
    """
    Purpose of file is to produce a JSON object for an attachment.
    Pulled JSON object from Jama SwaggeUI instance on creating an attachment.
    @params:
        name -> The name of the attachment.
        description -> The description of the attachment.
    """
    return {
        "fields": {
            "name": name,
            "description": description
        }
    }
