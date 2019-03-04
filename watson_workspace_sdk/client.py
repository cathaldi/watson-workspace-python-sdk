
import requests
from requests.auth import HTTPBasicAuth
from watson_workspace_sdk.models.space import Space
import threading
import logging
from watson_workspace_sdk.config import Config
from typing import List, Optional

logging.basicConfig(level=Config.log_level)
logger = logging.getLogger(__name__)


class Client:
    """
    Basic class that handles Button settings for Annotations and Attachments

    Attributes
    ----------
    access_token : str
        JWT token
    app_id : str
        Application Id from Watson Workspace Dev UI
    app_secret : str
        App Secret generated on app creation
    id : str
        Id of bot
    display_name : str
        Name to be shown in Watson Workspace
    is_bot : str
        Whether the user is a bot or not
    """

    def __init__(self, app_id, app_secret):
        self.access_token: str = ""
        self.app_id: str = app_id
        self.app_secret: str = app_secret
        self.id: str = ""
        self.display_name: str = ""
        self.is_bot: bool = False
        self._authenticate()
        self._get_profile()

    def _authenticate(self) -> None:
        """
        Authenticates user and starts a thread to authenticate every hour in order to continue to use workspace.
        :return: None
        """
        body = {"grant_type": "client_credentials"}
        response = requests.post("https://api.watsonwork.ibm.com/oauth/token", data=body,
                                 auth=HTTPBasicAuth(self.app_id, self.app_secret))
        self.access_token = response.json().get("access_token")
        self.id = response.json().get("id")
        Config.access_token = self.access_token
        self._auth_thread = threading.Timer(3000, self._authenticate)
        self._auth_thread.start()  # reauth after 50 mins
        return response

    def __repr__(self) -> str:
        """
        Returns information about the current client
        """
        return f""""App Id : {self.app_id}
                    Id : {self.id}
                    Email Address : {self.email}
                    Display Name : {self.display_name}
                    Is Bot : {self.is_bot}"""

    def _refresh_access_token(self) -> None:
        """
        Refreshes access token for currently logged in user.
        :return: None
        """
        # todo: validate in case of bad creds.
        body = {"grant_type": f"refresh_token", "refresh_token": f"{self.access_token}"}  # , "refresh_token": f"{self.access_token}"}
        headers = {"Authorization": "Bearer " + Config.access_token}
        response = requests.post("https://api.watsonwork.ibm.com/oauth/token", data=body,
                                 headers=headers)

        self.access_token = response.json().get("access_token")
        self.id = response.json().get("id")
        Config.access_token = self.access_token

    def _get_profile(self) -> None:
        """
        Gets information about the currently logged in user.
        :return: None
        """
        body = f"""
        query getProfile {{
          person(id: "{self.id}") {{
            id
            displayName
            email
          }}
        }}
        """
        response_json = requests.post(f"https://api.watsonwork.ibm.com/graphql",
                                      headers={"Authorization": "Bearer " + Config.access_token,
                                               "Content-type": "application/graphql"}, data=body).json()
        self.display_name = response_json.get("id")
        self.email = response_json.get("email")
        self.is_bot = True if response_json.get("email") == None else False

    def get_spaces(self, max_number_of_spaces: Optional[int] = 10) -> List[Space]:
        """
        Gets a list of spaces the user is a member of
        :param: max_number_of_spaces : Max number of spaces to be returned, default is 10.
        :return: List of spaces
        :rtype: List['Spaces']
        """
        retrieved_spaces = {}
        body = "query getSpaces {spaces(first: {0}) {" \
               " items { id title description created updated membersUpdated members { items { email displayName }}}}}"
        response = requests.post("https://api.watsonwork.ibm.com/graphql?query={1}".format(body,max_number_of_spaces),
                                 headers={"Authorization": "Bearer " + self.access_token,
                                          "Content-type": "application/json"})
        for space_json_string in response.json().get("data").get("spaces").get("items"):
            new_space = Space.get_from_json(space_json_string)
            retrieved_spaces[new_space.id] = new_space
        return retrieved_spaces

    def stop(self):
        self._auth_thread.cancel()
