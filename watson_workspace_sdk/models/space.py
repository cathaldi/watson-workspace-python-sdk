import datetime
import requests
import json

from watson_workspace_sdk.models.person import Person
# from watson_workspace_sdk.models.conversation import Conversation
from watson_workspace_sdk.models.message import Message
from watson_workspace_sdk.utilities import _http_status_handler
from typing import List

import logging
from watson_workspace_sdk.config import Config

logging.basicConfig(level=Config.log_level)
logger = logging.getLogger(__name__)


def parse_members(members_json) -> List[Person]:
    """
    Takes in a JSON Array of members and converts it to a list of Person objects
    :param members_json: JSON Object
    :return: A list of Members of a workspace
    :rtype: List[Person]
    """
    member_list = []
    for member_json in members_json.get("items"):
        member = Person.from_json(member_json)
        member_list.append(member)
    return member_list


class Space:
    """
    Basic class that Space functionality.

    **Attributes**

    id : str
        Space Id
    created : datetime
        Space creation date
    created_by : Person
        Person that created the space
    updated : datetime
        Space modification date
    updated_by : Person
        Person who last updated the space
    description : str
        Space description string
    members : List[Person]
        List of space members
    members_updated : datetime
        Memberlist update timestamp
    conversation : str
        Conversation object - may be removed

    **Methods**
    """

    def __init__(self, id: str="", created: datetime = datetime.time(0, 0), created_by=None,
                 updated: datetime =datetime.time(0, 0),
                 updated_by=None, title="", description="", members=[],
                 members_updated=datetime.time(0, 0), conversation=None) -> 'Space':
        self.id: str = id
        self.created: datetime = created
        self.created_by: Person = created_by
        self.updated: datetime = updated
        self.updated_by: [Person] = updated_by
        self.title: str = title
        self.description: str = description
        self.members: [Person] = members
        self.members_updated: datetime = members_updated
        self.conversation: str = ""

    def __repr__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return f"{{ Id: {self.id}, Created: {self.created}, Created By: {self.created_by}, Updated: {self.updated}, " \
               f"Updated By: {self.updated_by}, Title: {self.title}, Description: {self.description}," \
               f"Members: {self.members }, Members Updated: {self.members_updated}, Conversation: {self.conversation}"

    def _clear(self):
        self.id: str = None
        self.created: datetime = None
        self.created_by: Person = None
        self.updated: datetime = None
        self.updated_by: [Person] = None
        self.title: str = None
        self.description: str = None
        self.members: [Person] = None
        self.members_updated: datetime = None
        self.conversation: str = ""

    @classmethod
    def get_from_json(cls, json_body) -> 'Space':
        """
        Gets a Space object from JSON
        :param json_body:
        :return: Space
        :rtype: Space
        """
        _id: str = json_body.get("id", "")
        created = json_body.get("created", datetime.time(0, 0))
        created_by = json_body.get("createdBy", None)
        updated: datetime = json_body.get("updated", datetime.time(0, 0))
        updated_by: [Person] = json_body.get("updatedBy", [])
        title: str = json_body.get("title", "")
        description: str = json_body.get("description", "")
        members: [Person] = parse_members(json_body.get("members"))
        members_updated: datetime = json_body.get("membersUpdated", datetime.time(0, 0))
        # conversation: Conversation = json_body.get("conversation", None)  # [Conversation]
        return cls(_id, created, created_by, updated, updated_by, title, description, members, members_updated,
                   "")

    @classmethod
    def create(cls, space_title) -> 'Space':
        """
        A simple method to create a space with a provided space title.

        :param space_title: Title of the new workspace.
        :returns: Space
        :rtype: Space
        """
        body = f"""mutation createSpace {{ createSpace( input: {{ title: "{space_title}" }})
        {{ space {{id title}} }} }}"""
        response = requests.post("https://api.watsonwork.ibm.com/graphql?query={0}".format(body),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/json"})
        _http_status_handler(response.json().get("message"), response.json().get("errors"))
        return cls.get_from_json(response.json())

    @classmethod
    def get(cls, space_id) -> 'Space':
        """
        A simple method to populate Conversation object from a space_id

        :param space_id: the id of the space to retrieve
        :returns: Space
        :rtype: Space
        """
        body = f"""query getSpace {{space(id: "{space_id}") {{ id title description membersUpdated members 
        {{ items {{ id email displayName }} }} conversation{{ messages{{ items {{ content }} }} }} }} }}"""
        response = requests.post("https://api.watsonwork.ibm.com/graphql?query={0}".format(body),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/json"})
        _http_status_handler(response.json(), response.status_code)
        return cls.get_from_json(response.json().get("data").get("space"))

    def _update(self, title)-> None:  # todo: Not implemented fully
        body = f"""mutation updateSpaceTitle {{ updateSpace(input: {{ id: "{self.id}", title: "{title}"}})
        {{space{{title}}}}}}"""
        response = requests.post("https://api.watsonwork.ibm.com/graphql?query={0}".format(body),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/json"})
        _http_status_handler(response.json(), response.status_code)

    def send_message(self, message_to_send: Message) -> None:
        """
        Sends a message to a Space
        :param message_to_send: Message object to send
        :return: None
        """
        response = requests.post(f"https://api.watsonwork.ibm.com/v1/spaces/{self.id}/messages",
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/json"}, data=message_to_send.to_json())
        _http_status_handler(response.json(), response.status_code)

    def delete(self) -> None:
        """
        A simple method to delete the space.

        :returns: None
        """
        body = f"""mutation deleteSpace {{ deleteSpace(input: {{ id: "{self.id}"}}){{ successful }} }}"""
        response = requests.post("https://api.watsonwork.ibm.com/graphql?query={0}".format(body),
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/json"})
        json_response = response.json()
        _http_status_handler(response.json(), response.status_code)
        if "errors" not in json_response:
            self._clear()
        return None

    def add_members(self, list_of_members_to_add: [str]) -> None:
        """
        Adds a  list of members to a Space
        :param: list_of_members_to_add
        :return: None
        """
        body = f"""mutation updateSpaceAddMembers {{updateSpace(input: {{ id: "{self.id}",
         members: {json.dumps(list_of_members_to_add)}, memberOperation: ADD}})
         {{ memberIdsChanged space {{ title membersUpdated }}}}}}"""
        response = requests.post("https://api.watsonwork.ibm.com/graphql",
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql"}, data=body)
        _http_status_handler(response.json(), response.status_code)

    def remove_members(self, list_of_members_to_delete: [str]) -> None:
        """
        Removes a  list of members to a Space
        :param: list_of_members_to_remove
        :return: None
        """
        body = f"""mutation updateSpaceRemoveMembers{{updateSpace(input:{{id:"{self.id}", 
        members:{json.dumps(list_of_members_to_delete)}, memberOperation: REMOVE}})
        {{ memberIdsChanged space {{title membersUpdated }}}}}}}}}}"""
        response = requests.post("https://api.watsonwork.ibm.com/graphql",
                                 headers={"Authorization": "Bearer " + Config.access_token,
                                          "Content-type": "application/graphql"}, data=body)
        _http_status_handler(response.json(), response.status_code)

    # def share_file(self, file):  # Possible WW defect here.
    #     files = {'12312321_prv_1231232.csv': open('test.txt', 'rb')}
    #     response = requests.post(f"https://api.watsonwork.ibm.com/v1/spaces/{self.id}/files",
    #                              headers={"Authorization": "Bearer " + Config.access_token},
    #                              files=files)
    #     _http_status_handler(response.json(), response.status_code)
    #     print(response.request.headers)
    #     print(response.status_code)
    #     print(response.content)
