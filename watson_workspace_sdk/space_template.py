# import requests
# from models.config import Config
# from client import Client
#
# APP_ID = "4fc075ec-781f-4999-a788-dd12e40912e5"
# APP_SECRET = "yw0hPXxrJoqtJ4LHYQpRVTgcAsew"
#
# ww = Client(APP_ID, APP_SECRET)
#
#
# def create_template():  # todo: seems to work
#     """
#     A simple method to create a space with a provided space title.
#
#     :param space_title: Title of the new workspace.
#     :returns: None
#     :raises keyError: raises an exception
#     """
#     body = f"""
#         mutation {{
#         createSpaceTemplate(input: {{
#             name: "Template 1"
#             description: "A test template."
#             spaceStatus: {{
#                 acceptableValues: [
#                     {{
#                         displayName: "Starting"
#                     }},
#                     {{
#                         displayName: "Ending"
#                     }}
#                     ,
#                     {{
#                         displayName: "Gathering Results"
#                     }}
#                     ,
#                     {{
#                         displayName: "Ending"
#                     }}
#                 ]
#             }}
#             properties: {{
#                 properties: [
#                     {{
#                         listProperty: {{
#                             displayName: "Area",
#                             acceptableValues: [
#                                 {{
#                                     displayName: "Supply",
#                                 }},
#                                 {{
#                                     displayName: "Inventory"
#                                 }}
#                             ]
#                         }}
#                     }}
#                 ]
#             }}
#             requiredApps: {{
#                 apps: [
#
#                 ]
#             }}
#         }}) {{
#         spaceTemplate {{
#         id
#     }}
#     }}
#     }}
#     """
#     response = requests.post("https://api.watsonwork.ibm.com/graphql",
#                              data=body,
#                              headers={"Authorization": "Bearer " + Config.access_token,
#                                       "Content-type": "application/graphql",
#                                       'x-graphql-view': 'BETA,EXPERIMENTAL'})
#
#     print(response.json().get("data").get("createSpaceTemplate").get("spaceTemplate").get("id"))
#
#
# def create():  # todo: seems to work
#     """
#     A simple method to create a space template with a provided space title.
#
#     :param space_title: Title of the new workspace.
#     :returns: None
#     :raises keyError: raises an exception
#     """
#     body = f"""
#         mutation {{
#         createSpaceTemplate(input: {{
#             name: "Template 1"
#             description: "A test template."
#             spaceStatus: {{
#                 acceptableValues: [
#                     {{
#                         displayName: "Starting"
#                     }},
#                     {{
#                         displayName: "Ending"
#                     }}
#                     ,
#                     {{
#                         displayName: "Gathering Results"
#                     }}
#                     ,
#                     {{
#                         displayName: "Ending"
#                     }}
#                 ]
#             }}
#             properties: {{
#                 properties: [
#                     {{
#                         listProperty: {{
#                             displayName: "Area",
#                             acceptableValues: [
#                                 {{
#                                     displayName: "Supply",
#                                 }},
#                                 {{
#                                     displayName: "Inventory"
#                                 }}
#                             ]
#                         }}
#                     }}
#                 ]
#             }}
#             requiredApps: {{
#                 apps: [
#
#                 ]
#             }}
#         }}) {{
#         spaceTemplate {{
#         id
#     }}
#     }}
#     }}
#     """
#     response = requests.post("https://api.watsonwork.ibm.com/graphql",
#                              data=body,
#                              headers={"Authorization": "Bearer " + Config.access_token,
#                                       "Content-type": "application/graphql",
#                                       'x-graphql-view': 'BETA,EXPERIMENTAL'})
#
#
#
#
#
# create_template()
#
# # {{
# #     id: "d0c246a0-bced-4bf4-a29d-99cc6ad1ad53"
# # }},
# # {{
# #     id: "e8c0e8ae-49cf-448d-a845-bb453f0bf94a"
# # }}