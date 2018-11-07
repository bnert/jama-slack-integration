def help(command=""):
    """
    Return a help manual to slack, which helps the user understand how to use a command.
    @params:
        input -> A specific command that the user want to look for. Default is "",
                 which would lead to an explanation of all command.
    """
    command = command.lower()
    if command == "search":
        return "/jama search,keyword` search any item that has your given keyword."
    elif command == "create":
        return "`/jama create` create an item."
    elif command == "comment":
        return "By using `/jamaconnect comment` command, a dialog box would appear for for your input:\n" +\
               "`Project Reference` In case you do not remember the project id, you can check it here by " +\
               "typing the project name.\n" + \
               "`Input Project ID` The project id of the item you want to comment on. This is not required, " +\
               "but you can limit the item search result by typing the project ID. \n" +\
               "`Item ID or Keyword` The item you want to comment on, You can use the item id or any keyword " +\
               "to find the item you want.\n" + \
               "`Comment` The content you want to comment.\n\n" + \
               "If you already know the item id and want a simple fast comment method, you can use the inline " +\
               "commend `/jamaconnect comment:itemId,commentBody` to comment an item.\n" +\
               "`itemId` The id of the item you want to comment on.\n" +\
               "`commentBody` The content you want to put into the comment."
    elif command == "oauth":
        return "`/jamaconnect oauth,clientID,clientSecret` provides OAuth information to jamaconnect that allows it to act on jama on your behalf.\n" +\
               "A client ID and Secret can be obtained on your jama profile -> 'Set API Credentials' -> 'Create API Credentials'."
    elif command == "attach file" or command == "attach" or command == "attachment":
        return "By using the Slack Action `Attach file` (which can be found at the `...` sign of each Slack " +\
               "massage), a dialog box would appear for for your input.\n" +\
               "`Item ID` The id of the item you want to attach your file to.\n" +\
               "`Description` The description of the file."

    return "`/jamaconnect search,keyword` search any item that has your given keyword.\n" +\
           "`/jamaconnect create` create an item.\n" +\
           "`/jamaconnect comment` to comment an item.\n" +\
           "`/jamaconnect oauth,clientID,clientSecret` to provide OAuth information.\n" +\
           "`/jamaconnect help,command` to see the detail of a Jama's Slack command\n" +\
           "Slack Action `Attach file` to attach a file from Slack to Jama"
