import json
import logging
from watson_workspace_sdk.config import Config

logging.basicConfig(level=Config.log_level)
logger = logging.getLogger(__name__)


class Webhook:
    """
    Webhook object.

    **Attributes**

    space_name : str
        Space Name
    space_id : str
        Space Id
    annotation_payload : str
        JSON Annotation Payload - use property annotation below to get an annotation dict
    message_id : str
        Message id that triggered the webhook
    annotation_id : str
        Annotation id
    time : str
        Webhook execution time
    type : str
        Webhook type
    user_name : str
        User that triggered webhook
    user_id : str
        User id that triggered webhook
    """

    def __init__(self):
        self.space_name: str = ""
        self.space_id: str = ""
        self.annotation_payload: str = ""  # maybe annotation string and then a property that' a dict?
        self.message_id: str = ""
        self.annotation_type = ""
        self.annotation_id = ""
        self.time = ""
        self.type = ""
        self.user_name: str = ""
        self.user_id: str = ""

    @classmethod
    def from_json(cls, json_payload) -> 'Webhook':
        """
        Creates a webhook object from JSON payload ( Workspace webhook event )
        :param json_payload:
        :return: Webhook
        :rtype: Webhook
        """
        new_webhook = Webhook()

        new_webhook.space_name = json_payload.get("spaceName", "")
        new_webhook.space_id = json_payload.get("spaceId", "")
        new_webhook.annotation_payload = json_payload.get("annotationPayload", "")
        new_webhook.message_id = json_payload.get("messageId", "")
        new_webhook.annotation_type = json_payload.get("annotationType", "")
        new_webhook.annotation_id = json_payload.get("annotationId", "")
        new_webhook.time = json_payload.get("time", "")
        new_webhook.type = json_payload.get("type", "")
        new_webhook.user_name = json_payload.get("userName", "")
        new_webhook.user_id = json_payload.get("userId", "")
        logger.info(f" {new_webhook.type} event triggered for message {new_webhook.message_id} in space {new_webhook.space_id}")

        return new_webhook

    @property
    def annotation(self):
        """
        Parses annotation_payload and returns an annotation dict
        :return:
        """
        if not self.annotation_payload:
            return ""
        annotation = self.annotation_payload
        annotation.replace("'", "")
        return json.loads(annotation)

    def __repr__(self) -> str:
        """
        :return: Summary of the object
        :rtype: str
        """
        return f"""
                Space Name = {self.space_name}
                Space Id = {self.space_id}
                Annotation Payload = {self.annotation_payload}
                Annotation = {self.annotation}
                Message Id = {self.message_id}
                Annotation Type = {self.annotation_type}
                Annotation Id = {self.annotation_id}
                Time = {self.time}
                Type = {self.type}
                User Name = {self.user_name}
                User Id = {self.user_id}
                """
