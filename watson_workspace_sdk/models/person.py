import datetime
import requests
from watson_workspace_sdk.utilities import _http_status_handler
import logging
from watson_workspace_sdk.config import Config

logging.basicConfig(level=Config.log_level)
logger = logging.getLogger(__name__)


class Person:
    """
    Object for Watson Workspace Users

    **Attributes**

    display_name : str
        Title/Heading of the Annotation
    ext_id : str
        Message content type, appMessage by default
    email : str
        List of annotations attributed to the message, usually created by Watson API
    photo_url : str
        Message creation time
    customer_id : str
        Message modification time
    ibm_unique_id : str
        Message creator
    created : str
        Message Id
    updated : datetime
        Person who last modified message
    created_by : datetime
        Message version
    presence : str
        Message version
    updated_by : Person
        Message version
    id : str
        Message version
    is_bot : str
        Message version

    **Methods**
    """

    def __init__(self):
        self.display_name: str = None
        self.ext_id: str = None
        self.email: str = None
        self.photo_url: str = None
        self.customer_id: str = None
        self.ibm_unique_id: str = None
        self.created: datetime = None
        self.updated: datetime = None
        self.created_by: Person = None
        self.presence: str = None  # todo: this should be of type PresenceStatus
        self.updated_by: Person = None
        self.id: str = None

        self.is_bot: bool = None  # useful for spaces possibly.

    def __repr__(self) -> str:
        """
        String representation of the user
        :return: User information
        :rtype: str
        """
        return f""" {self.display_name}  {self.email}   {self.customer_id}  {self.id}  """

    @classmethod
    def get(cls, user_id: str) -> 'Person':
        """
        A simple method to populate Conversation object from a conversation_id

        :param user_id: the person id to retrieve from Watson Workspace
        :returns: Person
        :raises keyError: raises an exception
        """
        body = f"""query getProfile {{ person(id: "{user_id}") {{ id displayName email }}}}"""
        response = requests.post("https://api.watsonwork.ibm.com/graphql?query={0}".format(body),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/json"}).json()
        _http_status_handler(response.json())
        return cls.from_json(response.get("data").get("person"))

    @classmethod
    def from_json(cls, json_body: {}) -> 'Person': # todo: add in type hint
        """
        Creates a Person user from a JSON object containing Person data
        :param json_body: JSON Person Object
        :return: Person
        :rtype: Person
        """
        person = cls()
        person.display_name: str = json_body.get("displayName", "default")
        person.ext_id: str = json_body.get("extId", "default")
        person.email: str = json_body.get("email", "default")
        person.photo_url: str = json_body.get("photoUrl", "default")
        person.customer_id: str = json_body.get("customerid", "default")
        person.ibm_unique_id: str = json_body.get("ibmUniqueID", "default")
        person.created: datetime = json_body.get("created", "default")
        person.updated: datetime = json_body.get("updatedBy", "default")
        person.created_by: Person = json_body.get("createdBy", "default")
        person.presence: str = json_body.get("PresenceStatus", "default")
        person.updated_by: Person = json_body.get("Person", "default")
        person.id: str = json_body.get("ID", "default")
        return person
