import unittest
from watson_workspace_sdk.client import Client, Space
from watson_workspace_sdk.models.message import  Message
import os

#  This block ensures tests run in order.
def cmp(a, b):
    return (a > b) - (a < b)


unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: cmp(x, y)


APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ("APP_SECRET")

ww = Client(APP_ID, APP_SECRET)


class TestWorkspace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.message = None

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
        test_space = Space.get("5b086c7ee4b0aa8a21628846")
        assert(test_space.id == "5b086c7ee4b0aa8a21628846")

    # def test_05_update_space(self): disabled space as it just updated title
    #     test_space = Space.get("5b086c7ee4b0aa8a21628846")
    #     test_space.update("Test Time")
    #     assert(test_space.title == "Test Time")

    def test_06_send_message(self):
        self.my_message = Message.create(space_id="5b086c7ee4b0aa8a21628846", title="Today's Weather", text="Rain", actor="Rain App", color="blue")
        assert(self.my_message.id > 0)

    def test_07_add_reaction(self):
        self.my_message.add_reaction()
        assert(self.my_message.id > 0)

    def test_08_remove_reaction(self):
        self.my_message.add_reaction()
        assert(self.my_message.id > 0)

    def test_09_add_focus(self):
        self.my_message.add_reaction()
        assert(self.my_message.id > 0)