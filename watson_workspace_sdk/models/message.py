import datetime
import requests
import logging
from watson_workspace_sdk.utilities import _http_status_handler

from watson_workspace_sdk.config import Config
from watson_workspace_sdk.models.person import Person
from watson_workspace_sdk.models.genericAnnotation import Annotation
from watson_workspace_sdk.models.card import Card
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Message:
    """
        Used for creating,updating and deleting Messages

        **Attributes**

        content : str
            Title/Heading of the Annotation
        content_type : str
            Message content type, appMessage by default
        annotations : Annotation
            List of annotations attributed to the message, usually created by Watson API
        created : datetime
            Message creation time
        updated : datetime
            Message modification time
        created_by : Person
            Message creator
        id : str
            Message Id
        updated_by : Person
            Person who last modified message
        version : str
            Message version

        **Methods**
    """

    def __init__(self, id: str = ""):  # content_type, version and annotations are required.
        self.content: str = ""
        self.content_type: str = "appMessage"
        self.annotations: List[Annotation] = []
        self.created: datetime = None
        self.updated: datetime = None
        self.created_by: Person = None
        self.id: str = id
        self.updated_by: Person = None
        self.version: str = "1"

    @classmethod
    def create(cls, space_id: str, title="title", text="text", color="#36a64f", actor="") -> 'Message':
        """
        Sends a message to Watson Workspace and then creates a Message object

        :param space_id: Target space Id
        :param title: Message Title
        :param text: Message body
        :param color: Border color for message
        :param actor: Message sender
        :return: Message object of sent message
        :rtype: Message
        :example:
        >>> my_message = Message.create(space_id=space_id, title="Today's Weather", text="Rain", actor="Rain App", color="blue")
        """
        message = cls()
        message.annotations.append(Annotation(title=title, text=text, actor=actor, color=color))
        message._annotation_to_json()
        response = requests.post(f"https://api.watsonwork.ibm.com/v1/spaces/{space_id}/messages",
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/json"}, data=message.to_json().encode("utf-8"))
        response_json = response.json()
        _http_status_handler(response.json(), response.status_code)
        message._parse_json(response_json)

        return message

    @classmethod
    def from_json(cls, response_json) -> 'Message':
        """
        Creates a Message object from JSON.
        Useful when retrieving a list of messages. Does not send a messsage to Watson Workspace
        :param response_json: JSON Message Object
        :return: Message
        :rtype: Message
        """
        message = cls()
        message._parse_json(response_json)  # gets extra details like Id, created, created by etc.
        return message

    @classmethod
    def get(cls, message_id: str) -> 'Message':
        """
        Retrieves existing message from Watson Workspace

        :param message_id: Message Id to retrieve
        :return: Message
        :rtype: Message

        >>> my_message = Message.get(message_id)
        """
        body = f"""
        query getMessage {{
          message(id: "{message_id}") {{
            id
            content
            contentType
            annotations
            created
            createdBy{{
              extId
              id
              displayName
            }}
            updated
            updatedBy{{
              extId
              id
              displayName
            }}
          }}
        }}
        
        """
        got_message = cls(message_id)
        response = requests.post(f"https://api.watsonwork.ibm.com/graphql",
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql"}, data=body)
        message = response.json().get("data").get("message")
        _http_status_handler(response.json(), response.status_code)
        got_message._parse_json(message)
        return got_message

    def __repr__(self) -> str:
        """
        String representation of the object
        :return: A summary of the message
        :rtype: str
        """
        return f"{{ Content: {self.content}, Content Type: {self.content_type}, Annotations: {self.annotations}, Created: {self.created}, " \
               f"Updated: {self.updated}, Created By: {self.created_by}, Id: {self.id}," \
               f"Updated By: {self.updated_by }, Version: {self.version}   }}"

    def _parse_json(self, json_body):
        self.id = json_body.get("id")
        self.version = json_body.get("version")
        self.type = json_body.get("type")
        self.created = json_body.get("created")
        try:
            self.created_by = json_body.get("createdBy").get("id")
        except Exception as e:
            self.created_by = json_body.get("createdBy")
        self.annotations = []  # clean
        annotation_string_array = json_body.get("annotations",[])
        for annotation_string in annotation_string_array:
            self.annotations.append(annotation_string)

    def _annotation_to_json(self) -> str:
        annotation_array_string: str = "[ "
        for annotation in self.annotations:
            annotation_array_string += annotation.to_json()
        annotation_array_string += " ]"
        return annotation_array_string

    def to_json(self) -> str:
        """
            Formats a message object into the format expect by watson  workspace.
        """
        return f"""
        {{
          "type": "{self.content_type}",
          "version": "{self.version}",
          "annotations": {self._annotation_to_json()}
        }}
          
          """

    def add_focus(self, phrase: str = "", *, lens: str = "Opportunity", category: str = "Inquiry", actions: str = '"test"',
                  confidence: float = 0.99, payload: str = "", start: int =0, end: int = 0,
                  version: int=1, hidden: str="false") -> None:
        """
        :param phrase: Subset of message to mark as focus topic
        :param lens: Lens to view request, options are ActionRequest, Question, and Commitment
        :param category:
        :param actions:  Watson Workspace Action to initiate when focus is triggered
        :param confidence: Confidence  level
        :param payload:
        :param start: inclusive index (including markdown) at which to start as the focus topic
        :param end: inclusive index (including markdown) at which to end as the focus topic
        :param version: Focus version
        :param hidden:  Is focus hidden

        :return: None

        >>> my_message.add_focus(start=55, end=67, actions='"check_weather"')
        """
        body = f"""
        mutation {{
            addMessageFocus(input: {{
                messageId: "{self.id}"
                messageFocus: {{
                    phrase: "{phrase}"
                    lens: "{lens}"
                    category: "{category}"
                    actions: [ {actions} ]
                    confidence: {confidence}
                    payload: "{payload}"
                    start: {start}
                    end: {end}
                    version: {version}
                    hidden: {hidden}
                }}
            }}){{
            message {{
            id
        annotations
        }}
        }}
        }}
        """
        response = requests.post("https://api.watsonwork.ibm.com/graphql",
                                 data=body,
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql",
                                          'x-graphql-view': 'BETA,PUBLIC'})
        _http_status_handler(response.json(), response.status_code)

    def add_reaction(self, reaction: str) -> None:
        """
         Adds a supported unicode character as a reaction to a message
         :param reaction: Unicode reaction to append to message
         :return: None
         >>> my_message.add_reaction("👍")
        """
        body = f"""
          mutation {{
            addReaction(input: {{targetId: "{self.id}", reaction: "{reaction}"}}) {{
              reaction {{
                reaction
                count
                viewerHasReacted
              }}
          }}
        }}
        """
        response = requests.post("https://api.watsonwork.ibm.com/graphql",
                                 data=body.encode("utf-8"),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql",
                                          'x-graphql-view': 'PUBLIC'})
        if response.json().get("data").get("addReaction").get("reaction").get("viewerHasReacted"):
            return None
        _http_status_handler(response.json(), response.status_code)

    def remove_reaction(self, reaction: str) -> None:
        """
        Removes a supported unicode character as a reaction to a message assuming user has added that character previously
        :param reaction: Reaction to remove
        :return: None

        >>> my_message.remove_reaction("👍")
        """
        body = f"""
        mutation {{
            removeReaction(input: {{targetId: "{self.id}", reaction: "{reaction}"}}) {{
                reaction {{
                    reaction
                    count
                    viewerHasReacted
                }}
            }}
        }}    
        """
        response = requests.post("https://api.watsonwork.ibm.com/graphql",
                                 data=body.encode("utf-8"),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql",
                                          'x-graphql-view': 'PUBLIC'})
        if not response.json().get("data").get("removeReaction").get("reaction").get("viewerHasReacted"):
            return None
        _http_status_handler(response.json(), response.status_code)

    @staticmethod
    def message_with_attachment(*, conversation_id: str, target_user_id: str, target_dialog_id: str,
                                cards: List[Card]) -> None:
        """
        https://developer.watsonwork.ibm.com/docs/tutorials/action-fulfillment
        :param conversation_id: Space Id
        :param target_user_id:  User Id
        :param target_dialog_id: Reference to the annotation event that initiated call, provided by webhook event
        :param cards: Cards to be added
        :return: None

        >>> new_card = Card("Here's test card 1 ", "A smaller title", "Body")
        >>> new_card.add_button("Test Button", "test_button_event")
        >>> attached_message = Message.message_with_attachment(conversation_id=webhook_event.space_id, target_dialog_id=annotation.get("targetDialogId"), target_user_id=annotation.get("targetDialogId"), cards=[new_card])
        """

        card_string = ""
        for card in cards:
            card_string += str(card)
        body = f"""
             mutation {{
                createTargetedMessage(input: {{
                  conversationId: "{conversation_id}"
                  targetUserId: "{target_user_id}"
                  targetDialogId: "{target_dialog_id}"
                  attachments: [
                    {card_string}
                  ]
                    }})
                        {{
                            successful
                        }}
                }}
            """
        response = requests.post("https://api.watsonwork.ibm.com/graphql",
                                 data=body.encode("utf-8"),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql",
                                          'x-graphql-view': 'PUBLIC, BETA'})
        _http_status_handler(response.json(), response.status_code)

    @staticmethod
    def message_with_annotation(*, conversation_id: str, target_user_id: str, target_dialog_id: str,
                                annotation: Annotation) -> None:
        """
        :param conversation_id: Space Id
        :param target_user_id:  User Id
        :param target_dialog_id: Reference to the annotation event that initiated call, provided by webhook event
        :param annotation: Annotation to send
        :return: None

        >>> test_annotation = Annotation("Test Annotation", "Here's a test annotation with a button")
        >>> test_annotation.add_button("Click here", "button_test_event")
        >>> Message.message_with_annotation(conversation_id=webhook_event.space_id, target_user_id=webhook_event.user_id,target_dialog_id=annotation.get("targetDialogId"), annotation=test_annotation)
        """
        body = f"""
             mutation {{
                createTargetedMessage(input: {{
                  conversationId: "{conversation_id}"
                  targetUserId: "{target_user_id}"
                  targetDialogId: "{target_dialog_id}"
                  annotations: [
                    {annotation}
                  ]
                    }})
                        {{
                            successful
                        }}
                }}
            """
        response = requests.post("https://api.watsonwork.ibm.com/graphql",
                                 data=body.encode("utf-8"),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql",
                                          'x-graphql-view': 'PUBLIC, BETA'})
        _http_status_handler(response.json(), response.status_code)

    def count_reaction(self, reaction: str) -> int:  # todo: build this out - Should check who reacted as well
        """

        :param reaction: Unicode reaction to verify e.g. 🌧️
        :return: Number of times reaction has been added to message
        :rtype: int
        """
        body = f"""
                    query 
                    {{
                         reactingUsers(targetId: "{self.id}", reaction: "{reaction}")
                         {{ 
                                totalCount 
                                items 
                                    {{
                                        user 
                                            {{ 
                                                email 
                                                displayName 
                                                id 
                                            }}
                                        reacted 
                                    }}
                            pageInfo 
                            {{ 
                                hasNextPage 
                                hasPreviousPage 
                                endCursor 
                                startCursor 
                            }}
                        }}
                    }}
                    """
        response = requests.post(f"https://api.watsonwork.ibm.com/graphql",
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql",
                                          "x-graphql-view": "PUBLIC"}, data=body.encode("utf-8"))

        return response.json().get("data").get("reactingUsers").get("totalCount")
        # response.json().get("data").get("reactingUsers").get("items", [{}])[0].get("")
        # print(response.content)

