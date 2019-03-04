import unittest
from watson_workspace_sdk import Card, Space, Message, Client, Annotation
from watson_workspace_sdk.models.webhook import Webhook
import os

#  This block ensures tests run in order.
def cmp(a, b):
    return (a > b) - (a < b)


unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: cmp(x, y)


APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ.get("APP_SECRET")

TEST_SPACE_ID = os.environ.get("TEST_SPACE_ID")

ww = Client(APP_ID, APP_SECRET)


class TestWorkspace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.message = None
        cls.test_space_id = TEST_SPACE_ID  # WW-PYTHON-SDK TEST SPACE
        cls.test_message = Message.create(space_id=cls.test_space_id, title="Today's Forecast", text="Rain", actor="Weather App", color="blue")

    def test_01_verify_client(self):
        assert(ww.id != "")
        assert(ww.email is None)
        assert(ww.display_name is None)
        assert ww.is_bot

    # def test_02_create_space(self):  Bots cant add spaces.
    #     self.test_org.suspend()
    #     assert(self.test_org.state == State.SUSPENDED.value)

    def test_03_create_space_forbidden_exception(self):
        with self.assertRaises(Exception):
            Space.create("My Test Space")

    def test_04_get_space(self):
        test_space = Space.get(self.test_space_id)
        assert(test_space.id == self.test_space_id)

    # def test_05_update_space(self): disabled space as it just updated title
    #     test_space = Space.get("5b086c7ee4b0aa8a21628846")
    #     test_space.update("Test Time")
    #     assert(test_space.title == "Test Time")

    def test_06_send_message(self):
        self.my_message = Message.create(space_id=self.test_space_id, title="Today's Forecast", text="Sun", actor="Weather App", color="blue")
        assert(self.my_message.annotations[0].get('text') == "Sun")

    def test_07_add_reaction(self):
        self.test_message.add_reaction('🌧️')
        assert(self.test_message.count_reaction('🌧️') > 0)

    def test_08_remove_reaction(self):
        self.test_message.remove_reaction('🌧️')
        assert(self.test_message.count_reaction('🌧️') == 0)

    def test_09_add_focus_and_get_message(self):
        self.test_message.add_focus("rain", start=0, end=4, actions='"test_intent"')
        verification_message = Message.get(self.test_message.id)
        assert("\"phrase\":\"rain\"," in verification_message.annotations[1])  # todo: annotations should parse each annotation.

    ww.stop()
