Examples
========

Authenticate with Watson Workspace
----------------------------------
.. code-block:: python

   import watson_workspace_sdk as ww

   WORKSPACE_ID = os.environ.get('WORKSPACE_ID')  # array of spaces
   APP_ID = os.environ.get('APP_ID')
   APP_SECRET = os.environ.get('APP_SECRET')

   workspace_connection = ww.Client(APP_ID, APP_SECRET)  # Authenticates and stores jwt token for requests

Sending Messages
----------------
.. code-block:: python

   from watson_workspace_sdk import Message

   my_first_message = ww.Message.create(WORKSPACE_ID, "Hello World", "Some text here", 'green')

Reacting to Messages
--------------------
Adding a reaction

.. code-block:: python

   my_first_message.add_reaction("👍")

Removing a reaction

.. code-block:: python

   my_first_message.remove_reaction("👍")

Sending messages with annotations/attachments
---------------------------------------------
Create message with attachment
.. code-block:: python

    from watson_workspace_sdk import card
        new_card = Card("Here's test card 1 ", "A smaller title", "Body")
        new_card.add_button("Test Button", "test_button_event")
        attached_message = Message.message_with_attachment(conversation_id=webhook_event.space_id, target_dialog_id=annotation.get("targetDialogId"), target_user_id=annotation.get("targetDialogId"), cards=[new_card])

Create message with annotation
.. code-block:: python

    test_annotation = Annotation("Test Annotation", "Here's a test annotation with a button")
    test_annotation.add_button("Click here", "button_test_event")
    Message.message_with_annotation(conversation_id=webhook_event.space_id, target_user_id=webhook_event.user_id,target_dialog_id=annotation.get("targetDialogId"), annotation=test_annotation)

Playing with Spaces
-------------------
Get a space
.. code-block:: python

    my_space = ww.Space.get(space_id)


Add members
.. code-block:: python

    my_space.add_members()

Remove members
.. code-block:: python

    my_space.remove_members()

Add File
.. code-block:: python

    # Work in progress

Webhooks
--------