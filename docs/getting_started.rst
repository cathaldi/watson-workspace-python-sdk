Getting Started
===============

Installing package
    pip install https://github.com/cathaldi/watson-workspace-python-sdk

If you want to send messages from a client you just need import Message and create one.

.. code-block:: python

    from watson-workspace-sdk import Message

    Message.create(WORKSPACE_ID, "Hello World", "Some text here", 'green')


Client object can get a dict[space_id, Space] of spaces. Which returns a the spaces the bot has been added to. ( defaults to 10 )

