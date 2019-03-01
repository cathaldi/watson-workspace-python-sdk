Making A Bot
============

An endpoint with a hostname ( ip won't suffice ) and a valid HTTPS cert

Log into https://developer.watsonwork.ibm.com/apps and Create New App

If you just want to use the bot as a client to send messages periodically you should be set as this can be achieved
through authorising with the APP_ID and APP_SECRET.


To react to events like new messages in a space, users being removed, reactions added etc. we'll need to set up
a bot that makes use of Webhooks.


We'll be given a webhook secret in order to authenticate events coming from Watson Workspace.

