Getting Started
===============

Installing package
    pip install https://github.com/cathaldi/watson-workspace-python-sdk

If you want to send messages from a client you just need import Message and create one after your `app has been created <https://watson-workspace-python-sdk.readthedocs.io/en/latest/making_a_bot.html>`_ .

.. code-block:: python

    from watson-workspace-sdk import Message
    import watson_workspace_sdk as ww

    WORKSPACE_ID = os.environ.get('WORKSPACE_ID')  # array of spaces
    APP_ID = os.environ.get('APP_ID')
    APP_SECRET = os.environ.get('APP_SECRET')

    workspace_connection = ww.Client(APP_ID, APP_SECRET)  # Authenticates and stores jwt token for requests

    Message.create(WORKSPACE_ID, "Hello World", "Some text here", 'green')


Client object can get a dict[space_id, Space] of spaces. Which returns a the spaces the bot has been added to. ( defaults to 10 )
.. code-block:: python

    import watson-workspace-sdk as ww

     workspace_connection = ww.Client(APP_ID, APP_SECRET
     spaces_list = workspace_connection.get_space_ids()