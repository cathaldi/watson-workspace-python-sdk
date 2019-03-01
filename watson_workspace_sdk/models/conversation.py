# import datetime
# from watson_workspace_sdk.models.person import Person
# from watson_workspace_sdk.models.message import Message
# import logging
# from watson_workspace_sdk.config import Config
#
# logging.basicConfig(level=Config.log_level)
# logger = logging.getLogger(__name__)
#
# import logging
# from watson_workspace_sdk.config import Config
#
# logging.basicConfig(level=Config.log_level)
# logger = logging.getLogger(__name__)
#
#
# class Conversation:  # todo: seems the same as a space - does it need an object?
#
#     def __init__(self):
#         self.created: datetime = None
#         self.updated: datetime = None
#         self.createdBy: Person = None
#         self.messages: [Message] = None
#         self.updated_by: datetime = None
#
#     def get(self, conversation_id: str):
#         """
#         A simple method to populate Conversation object from a conversation_id
#
#         :param conversation_id: the conversation to retrieve from Watson Workspace
#         :returns: None
#         :raises keyError: raises an exception
#         """
#
#         "query getConversation { conversation(id: {0}) { id created updated messages(first: 50)" \
#         " { items { content contentType annotations }}}}".format(conversation_id)
#
