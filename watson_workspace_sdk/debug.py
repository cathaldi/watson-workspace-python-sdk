from watson_workspace_sdk.client import Client
from watson_workspace_sdk.models.space import Space
from watson_workspace_sdk.models.message import Message
from watson_workspace_sdk.models.card import Card
from watson_workspace_sdk.models.annotation import Annotation
from time import sleep
import threading

APP_ID = "4fc075ec-781f-4999-a788-dd12e40912e5"
APP_SECRET = "yw0hPXxrJoqtJ4LHYQpRVTgcAsew"

ww = Client(APP_ID, APP_SECRET)

message = Message.get("5bddfaf7f70ed60001f34480")
print(message.annotations)
#ww.get_spaces()

#my_space = Space.create("my new space")
# my_space= Space.get("5ba90597aff1e70001357505")
# my_space.share_file("")
# get a space
my_space = Space.get("5c77a77bbab80d0001fa6ea8")
#
# workspace = Client(APP_ID, APP_SECRET)
#
# # update a space.
#my_space.update(title="Riverbed")
#
my_message = Message.create(my_space.id, "Hello World", "Something went wrong", 'red', actor="Test Bot")

my_message.add_focus(start=0, end=9, actions='""')

# space_id: str, title="title", text="text", color="#36a64f", actor=""

# print("--")
# print(my_message.id)
# print("--")
# my_message.add_reaction("🕐")
#
#
# # my_message.remove_reaction("🎉")
# my_message.add_focus(start=10, end=20)

# new_card = Card("title", "subtitle", "text")
# new_card.add_button("test", "Sample_Button")
#
# print("here")
# attached_message = Message.message_with_attachment(conversation_id="5ba90597aff1e70001357505", target_dialog_id="test",
#                                                    target_user_id="internal-290e9aaf-d91b-4d88-9006-8986c4705852",
#                                                    cards=[new_card])
#
# new_annotation = Annotation("This is a test", "Did it work?")
# new_annotation.add_button("Yes","Yes")
# # new_annotation.add_button("No","No")
# annotated_message = Message.message_with_annotation(conversation_id="5ba90597aff1e70001357505", target_dialog_id="test", target_user_id="internal-290e9aaf-d91b-4d88-9006-8986c4705852",
#                                                     annotation=new_annotation)
#targetted_message(conversation_id: str, target_user_id: str, target_dialog_id: str, cards: []):


#created_message = Message.create(space_id="5ba90597aff1e70001357505", title="stuff")
# created_message = Message.create(space_id="5b086c7ee4b0aa8a21628846", title="Negative Feedback",
#                text="I was not accurate with my response - could you help me correct that?", actor="River", color="green")

#gotten_message = Message.get(message_id=created_message.id)
#gotten_message.remove_reaction("👍")
#new_message = Message.get("5ba90597aff1e70001357505")
#gotten_message.add_reaction("¸")
#gotten_message.remove_reaction("👎")

sleep(3600)


# one_card = Card("title", "subtitle", "text")
# one_card.add_button("time", "time", "PRIMARY")
# Message.targetted_message("5b086c7ee4b0aa8a21628846", "internal-290e9aaf-d91b-4d88-9006-8986c4705852",
#                           "Hello", [one_card])
