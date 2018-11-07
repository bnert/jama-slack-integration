# Jama Slack Integration Tools

This git repository contains a suite of Slack™ integration tools to be used for interfacing with Jama Connect™ software.

# License

This work is licensed under the MIT license. See the file LICENSE in this distribution for license terms.

Copyright © 2018 Jingyu Ye, Aleena Watson, Brent Soles, Bonden Lyons, Taisheng Guo & Lance Booth

# Build Instructions

## Server Side
* Pull down code
* (optional) Create a virtual environment 
  * `pip install virtualenv`, probably
* Install the python dependencies:
  * flask
  * requests
  * websockets
  * slackclient
  * mysql-connector (Even if you don't use a database. You'll run into problems otherwise.)
* (optional) For extra functionality (e.g. Jama-side OAuth), import "schema.sql" into a new database
  * This application was developed on and tested with a MariaDB server, but either that or MySQL should be fine.
  * The import command should be something like `mysql -u <DB username> -p <DB name> < shema.sql` from the command line, or importing schema.sql from your GUI if you have one.
* For instructions on running the server, see src/run.sh.template

## Slack Side
To activate the functionality in Slack, you must first create a Slack app. In order to do this, you will need the following:
* A Slack workspace
* A Slack user, who is a member of the Slack workspace
* The URL of the server on which this code will run

1. To create a new app, you need to log into your target workspace. Then you should go
to the [Slack Application Page](https://api.slack.com/apps) and click on
  Create New App . Here you can edit the app name and the related 
workspace. You can type any app name you want; However, for the purpose of 
managing your Slack app, we recommend you to name this app "Jama Connect".

**IMPORTANT** By default, the app creator would be the only author of the app. 
You can go to your app's `Settings > Collaborators `page and add other Slack 
users in your workspace as authors. Be careful because a collaborator can change any of the app's settings, add more 
collaborators, or even delete the app.

2. For our Jama Slack Integration to work properly, you need to turn on some 
Slack features and functionality, which are in the `Features` section on your 
left-hand side of your Slack app's homepage.

### Features > Interactive Components
In this page, you need to turn on the feature, fill in URLs, and create
actions.
1. Click to set the `On/Off` toggle button to `On`.
2. Fill in the `Request URL` as `your-hosting-url/SERVER_ADDRESS/dialog`.
For example, if the URL of your hosting server is `https://www.jama.com` and 
the `URL_RULE` section in `src/run.sh` is `"/jamaconnect"`, the 
`Request URL` should be `https://www.jama.com/jamaconnect/dialog`.
Note: the URL should not have a trailing slash.
3. In the `Actions` section, click `Create New Action` to add new actions.
There are two actions required for this integration and their fields are shown
belows:

| Field | Value | Note |
-|-|-
|Action Name: | Add comment |This can be change if you want.|
|Short Description: | Adding comment to Jama item|This can be change if you want.|
|Callback ID: | comment||

| Field | Value | Note |
-|-|-
|Action Name: | Attach file |This can be change if you want.|
|Short Description: | Attach file to Jama item|This can be change if you want.|
|Callback ID: | attachment||

4. In the `Message Menus` section, fill in the `Request URL` as 
`your-hosting-url/URL_RULE/menu`.For example, if the url of your 
hosting server is `https://www.jama.com` and the `URL_RULE` section in 
`src/run.sh` is `"/jamaconnect"`, the `Request URL` should be 
`https://www.jama.com/jamaconnect/menu`.
Note: the URL should not have a trailing slash.

### Features > Slash Commands
On this page, you need to click the `Create New Command` button to add a new 
command. There is one command required for this integration and its fields 
are shown below:

| Field | Value | Note |
-|-|-
|Command: | /jamaconnect |You can use another command. For the purpose of managing your Slack app, we recommend you to use `/jamaconnect`.|
|Request URL: | your-hosting-url/URLRULE | For example, if the url of your hosting server is `https://www.jama.com` and the `URL_RULE` section in `src/run.sh` is `"/jamaconnect"`, the `Request URL` should be `https://www.jama.com/jamaconnect`. Note: the URL should not have a trailing slash.|
|Short Description: | Jama Connect commands||
|Usage Hint|[help\|search\|create\|comment]||

### Features > Bot User
On this page, you need to turn on the Slack Bot User.
1. Click the `Add A Bot User` button.
2. Click the `Add Bot User` button to save the change.

### Features > OAuth & Permissions
On this page, you will need to add tokens to the `src/run.sh` (which you will have created earlier using `src/run.sh.template`) and also select permission scopes for this Slack app.

1. In the `Scopes > Select Permission Scopes` section, add the
following permission scopes by typing them into `Add permission by scope or API method` search box:

|**Permission Scopes**|
-|
|incoming-webhook|
|files:read|
|bot|
|commands|

After you add all of the above scopes, click `Save Changes`.

2. Click the `Reinstall App` button to add the bot user.
3. In `src/run.sh`, store the `OAuth Access Token` (the token begins with
`xoxp-`) to the environment variable `SLACK_OAUTH_TOKEN`.
4. In `src/run.sh`, store the `Bot User OAuth Access Token` (the token begins
with `xoxb-`) to the environment variable `SLACK_BOT_TOKEN`. If you can not find this token, please make
sure that you already added a bot user in the `Features > Bot User` section,
added the `bot` permission scopes in Step 1, and clicked `Reinstall App`.


### Features > User ID Translation
On this page, you need to turn on the Translate Global IDs feature by clicking to set the `On/Off` toggle button to `On`.

### Settings > Basic Information
On this page, copy the `Signing Secret` token found in the `App Credentials` section 
and store it in the environment variable `SLACK_SIGNING_SECRET` in `src/run.sh`.
