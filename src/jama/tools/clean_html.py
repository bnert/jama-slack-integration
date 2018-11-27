import re

def remove_tags(text):
    """
    Function will clean html by removing html tags leaving behind plaintext.
    Args:
       text (string): The html to be cleaned 
    Returns:
       (string): The plaintext 
    """
    text = re.sub("<[^<]+?>", "", text)
    text = re.sub("&nbsp;", " ", text)
    text = re.sub("&quot;", "\"", text)
    text = re.sub("&apos;", "'", text)
    text = re.sub("&gt;", "<", text)
    return re.sub("&lt;", ">", text)
