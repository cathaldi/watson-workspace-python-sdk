Getting Started
===============

Installing package
    pip install https://github.com/cathaldi/watson-workspace-python-sdk

If you want to send messages from a client you just need to

.. code-block:: python

    from watson-workspace-sdk import Messages

    Message.create(WORKSPACE_ID, "Hello World", "Some text here", 'green')


Client object cam get a list of spaces it is a part of