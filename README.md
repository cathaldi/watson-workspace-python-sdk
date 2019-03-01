"# watson-workspace-sdk" 


# Clients
Simple as Client("space_id) and you can access all elements within the chat.




# Servers + Webhooks
If you are trying to run a flask server for instance - at each entry point that a webhook points to
decorate the function with an @workspace_authenticate to verify that the message is from workspace.
additionally decorate the function with @workspace_authorize.

## Decorators

To make working with Workspace a bit easier the following decorators may be of use.

    @verify_workspace_origin("webhook-secret")
 Verifies that the message orinates from Watson Workspace.
 Workspace messages contain a checksum? generated from the webhook secret key

    @handle_verification("webhook-secret")
Workspace sends out a verification message when webhooks are enabled and every 5 minutes after that.

    @filter_users(whitelist=["internal-290e9aaf-d91b-4d88-9006-8986c4705852"])
Decorator only accepts messages from users one the whitelist

    @filter_workspace_annotations(whitelist=["actionSelected"], blacklist=[]):
Filters annotations types depending if they are on the whitelist.
For example action selected annotations are generated when a user clicks an action.
Ignoring any other annotations like for instance NLP and watson converastion events.

## Examples

Setting up a basic webhook in flask to respond to any message with "Hello"

    @app.route('/api/messages', methods=["POST"])
    @verify_workspace_origin("webhook-secret")
    @handle_verification("webhook-secret")
    def messages():
        return "Hello"
Sets up a webhook endpoint in Watson Workspace. Message integrity is handled through @verify_workspace_origin and @handle_verficiation handles verification messages periodically sent by watson workspace.

    @app.route('/api/annotations', methods=["POST"])
    @verify_workspace_origin("webhook-secret")
    @handle_verification("webhook-secret")
    @filter_workspace_annotations(whitelist=["actionSelected"]):
    def messages():
        return "Hello"
Filters annotations from this webhook to only forward actionSelected events ignoring all other annotations.




## So you want to make a Bot?


### App Permissions


### User Permissions



To set up a basic bot for Workspace you first need to [create an Application](https://developer.watsonwork.ibm.com/apps/).
We use the App Id and Secret to send messages as the bot.

We can set up Webhooks when certain events are triggered, for instance when a message created, edited or deleted.


    import watson-workspace-sdk as ww
    
    # Bots can't create spaces.
    space = ww.Space("space_id")
    
    
    space.sendMessage(Message("Test", "Let's try some math."))
    

Additionally Keyword commands can also be set up in actions.
For example : Lookup space attendees




Show a seperate project with a simple sample of cards, annotations etc.
What could a good project be though?    


Notice : This is mainly for reference. Watson Workspace has been sunset for February 28th, 2019.
