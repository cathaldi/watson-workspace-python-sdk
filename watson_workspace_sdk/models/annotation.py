from watson_workspace_sdk.models.card import Button
import logging
from watson_workspace_sdk.config import Config
from typing import List, Optional

logging.basicConfig(level=Config.log_level)
logger = logging.getLogger(__name__)


class Annotation:
    """
    Annotations are ephemeral messages that are initiated by the requester.
    For example clicking on a focus annotation could initiate a call and display an annotation message only
    to the user that clicked it.

    Annotations typically have a Title, Body along with an optional sender name, buttons to trigger events and
    change display colour.

    **Attributes**

    title : str
        Title/Heading of the Annotation
    display_text : str
        Main body of the Annotation
    buttons : Optional[List[Button]]
        List of Buttons if any that the Annotation has

    **Methods**
    """

    def __init__(self, title: str, display_text: str):
        """
        Initialises an annotation with a title and text

        :param title: Title for the Annotation.
        :param display_text:  Body of the Annotation.

        >>> new_annotation = Annotation("Let me guess your number", "Is your number 7?")
        """
        self.title: str = title
        self.display_text: str = display_text
        self.buttons: List[Button] = []

    @property
    def _buttons_string(self) -> str:
        """
            Creates JSON object for all button objects belonging to this annotation.
            :return: String JSON object containing buttons for the annotation.
        """
        buttons_to_string = ""
        for button in self.buttons:
            buttons_to_string += f"""{{postbackButton: {{
                                        title: "{button.display_text}",
                                        id: "{button.action}",
                                        style: {button.style}
                                       }}}},"""
        return buttons_to_string[:-1]

    def add_button(self, display_text: str, action: str, style: str = "PRIMARY") -> None:
        """
        Adds a new button object to the Annotation

        :param display_text: Display text for button.
        :param action: Workspace action to be executed on click. Typically defined in Actions in Workspace Dev UI
        :param style: Visual style of the button. Primary or Secondary.
        :return: None

        >>> new_annotation.add_button("Yes","guessed_correct_event")
        >>> new_annotation.add_button("No","guessed_incorrect_event")
        """
        self.buttons.append(Button(display_text, action, style))

    def __repr__(self) -> str:
        """
        A summary of the annotation

        :return: Description of annotation
        :rtype: str
        """
        return f""" {{
                        genericAnnotation: {{
                            title: "{self.title}",
                            text: "{self.display_text}",
                            buttons: [
                                {self._buttons_string}
                            ]
                        }}
                    }}
                    """

