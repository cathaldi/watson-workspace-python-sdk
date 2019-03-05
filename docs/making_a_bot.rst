Making an App/Bot
============

A bot will need to be hosted on a server that
 - has a domain name
 - supports HTTPS


Log into https://developer.watsonwork.ibm.com/apps and Create New App

An application Id and Secret will be generated.
Take note of the secret as it is only generated once but you can regenerate a new one whenever you want.

If you just want to use the app for one way communication to workspace, for instance sending messages you should be set as this can be achieved
through authorising with the APP_ID and APP_SECRET.

To react to events like new messages in a space, users being removed, reactions added etc. we'll need to set up
a bot that makes use of `Webhooks <https://watson-workspace-python-sdk.readthedocs.io/en/latest/webhooks.html>`_
