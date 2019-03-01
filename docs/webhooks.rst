Webhooks
========

Playing with Spaces
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
