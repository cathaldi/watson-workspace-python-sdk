import logging
from watson_workspace_sdk.config import Config

logging.basicConfig(level=Config.log_level)
logger = logging.getLogger(__name__)


class Button:
    """
        Basic class that handles Button settings for Annotations and Attachments

        **Attributes**

        display_text : str
            Button text
        action : str
            Watson Workspace action to execute when button is clicked
        style : str
            Button style : Primary/Secondary
            Default is Primary
    """
    def __init__(self, display_text: str, action: str, style: str = "Primary"):
        self.display_text = display_text
        self.action = action
        self.style = style

    def __repr__(self):
        return ""


class Card:  # Element to be included in a card.
    """
    Cards are used as part of Action Fulfillment to present multiple options to the user.
    Each option is displayed as a card. Cards are similar to Annotations in that they have a title, body
    and optional buttons but also have a subtitle field.

    **Attributes**

    type : str
        Card type
    title : str
        Card Title
    subtitle : str
        Card subtitle
    display_text : str
        Main body of Card
    date : Long
        Epoch timestamp in milliseconds
    buttons : List[Buttons]
        List of buttons for the Card

    **Methods**
    """

    def __init__(self, title: str, subtitle: str, display_text: str):
        self.type = "INFORMATION"   # INFORMATION
        self.title = title
        self.subtitle = subtitle
        self.display_text = display_text
        self.date = "1540940716000"   # todo: add dynamic date
        self.buttons = []

    @property
    def _button_string(self):  # todo: move this to button class?
        buttons_to_string = ""
        for button in self.buttons:
            buttons_to_string += f"""  {{
                                        text: "{button.display_text}",
                                        payload: "{button.action}",
                                        style: {button.style}
                                       }}"""
        return buttons_to_string

    def add_button(self, display_text, action, style="PRIMARY") -> None:
        """
        Adds a button to the card
        :param display_text: Button label text
        :param action:  Watson Workspace action to execute
        :param style: Button UI Style, default Primary
        :return: None
        """
        self.buttons.append(Button(display_text, action, style))

    def __repr__(self):
        return f""" {{ type: CARD,
                       cardInput: {{
                            type: {self.type},
                            informationCardInput: {{
                                title: "{self.title}",
                                subtitle: "{self.subtitle}",
                                text: "{self.display_text}",
                                date: "{self.date}",
                                buttons: [
                                    {self._button_string}
                                ]
                            }}
                        }}
                    }}"""

