# import datetime
# import logging
# from watson_workspace_sdk.config import Config
#
# logging.basicConfig(level=Config.log_level)
# logger = logging.getLogger(__name__)
#
# # make these dataclasses
#
# # MessageCreated = namedtuple("MessageCreated", "spaceName spaceId messageId time userName userId type contentType"
# #                                               " content")
#
#
# class MessageCreated:
#     """ hey """
#     def __init__(self, json_payload):
#         self.space_name: str = json_payload.get("spaceName")
#         self.space_id: str = json_payload.get("spaceId")
#         self.message_id: str = json_payload.get("messageId")
#         self.time: datetime = json_payload.get("time")
#         self.user_name: str = json_payload.get("userName")
#         self.user_id: str = json_payload.get("userId")
#         self.type: str = json_payload.get("type")
#         self.content_type: str = json_payload.get("contentType")
#         self.content: str = json_payload.get("content")
#
# # MessageAnnotationAdded = namedtuple("MessageAnnotationAdded", "spaceName spaceId annotationPayload messageId"
# #                                     " annotationType annotationId time type userName userId")
#
#
# class MessageAnnotationAdded:
#     """" hey """
#
#     def __init__(self, json_payload):
#         self.space_name = json_payload.get("spaceName")
#         self.space_id = json_payload.get("spaceId")
#         # self.annotation_payload = json_payload.get("annotation")
#         self.message_id = json_payload.get("messageId")
#         self.annotation_type = json_payload.get("annotationType")
#         self.annotation_id = json_payload.get("annotationId")
#         self.time = json_payload.get("time")
#         self.type = json_payload.get("type")
#         self.user_name = json_payload.get("userName")
#         self.user_id = json_payload.get("userId")
#
# # ReactionAdded = namedtuple("ReactionAdded", "spaceId reaction time type userId objectId objectType")
#
#
# class ReactionAdded:
#     """" hey """
#
#     def __init__(self, json_payload):
#         self.space_id = json_payload.get("spaceId")
#         self.reaction = json_payload.get("reaction")
#         self.time = json_payload.get("time")
#         self.type = json_payload.get("type")
#         self.user_id = json_payload.get("userId")
#         self.object_id = json_payload.get("objectId")
#         self.object_type = json_payload.get("objectType")
#
# # Verification = namedtuple("Verification", "type challenge")
#
#
# class Verification:
#     """" hey """
#     def __init__(self, json_payload):
#         self.type: str = json_payload.get("type")
#         self.challenge: str = json_payload.get("challenge")
#
#
# # message-created
# # message-deleted
# # message-edited
# #
# # space-members-added
# # space-members-removed
#
# # space-updated
# # space-deleted
# #
# # message-annotation-added
# # message-annotation-edited
# # message-annotation-removed
# #
# # reaction-aded
# # reaction-removed
