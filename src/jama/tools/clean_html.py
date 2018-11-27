# from bs4 import BeautifulSoup
import re

def remove_tags(html):
    """
    Function will clean html by removing html tags leaving behind plainhtml.
    Args:
       html (string): The html to be cleaned 
    Returns:
       (string): The plainhtml 
    """
    # return BeautifulSoup(html, "lxml").text
    html = re.sub("<[^<]+?>", "", html)
    html = re.sub("&nbsp;", " ", html)
    html = re.sub("&quot;", "\"", html)
    html = re.sub("&apos;", "'", html)
    html = re.sub("&gt;", "<", html)
    return re.sub("&lt;", ">", html)
