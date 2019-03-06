Webhooks
========

Adding webhooks to your application
-----------------------------------
After creating your application navigate to **Listen to events** and click **Add an outbound webhook**
In the image below we have added an endpoint and we are watching for the event **message-annotation-added** which will
be triggered when any annotation is added for any message. So if we were to add a focus annotation or click an annotation.
It also triggers when Watson Workspace adds `Watson API annotations  <https://watson-workspace-python-sdk.readthedocs.io/en/latest/watson_annotations.html#>`_

![alt text](docs/images/ww_add_listener.png "Image showing the result of clicking a Watson Workspace event")




Example
-------------------
Get a space

.. code-block:: python

    @app.route('/messages', methods=["POST"])
    @verify_workspace_origin(os.environ.get("app_secret"))
    @handle_verification(os.environ.get("app_secret"))
    def message_webhook(*args, **kwargs):
        webhook_event = Webhook.from_json(request.json)

        if webhook_event.user_id == workspace_connection.id:
            return "" # if this bot sent the message, ignore

        Message.create(space_id=webhook_event.space_id, title="", text=request.json().get("content"), actor="Echo Bot", color="blue")
