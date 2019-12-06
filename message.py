import base64
import pickle
import os.path
from settings import user_id, scopes, items_start, items_end
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors


# Create access token
creds = None
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)

# Generate service for credentials
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", scopes)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

service = build("gmail", "v1", credentials=creds)


############################################################################################
def ListMessagesMatchingQuery(service, user_id, query=""):
    try:
        response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
        messages = []
        if "messages" in response:
            messages.extend(response["messages"])
        while "nextPageToken" in response:
            page_token = response["nextPageToken"]
            response = service.users().messages().list(userId=user_id, q=query,
                                             pageToken=page_token).execute()
            messages.extend(response["messages"])
        return messages
    except errors.HttpError as error:
        print("An error occurred.", error)


def GetMessage(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except errors.HttpError as error:
        print("An error occurred.", error)
#############################################################################################

messages = ListMessagesMatchingQuery(service, user_id)
from trello import create_board, create_list, create_card

for message in messages:
    body = GetMessage(service, user_id, message.get("id"))
    message = base64.b64decode([part["body"]["data"] for part in body["payload"]["parts"] if part["mimeType"] == "text/plain"][0]).decode("utf-8")
    message_split = message.split("\r\n")
    message_split =  message_split[message_split.index(items_start): message_split.index(items_end)]
    list_id = create_list(create_board("12.02.2019"), "Action Items")
    for msg in message_split[1:-1]:
        if msg.strip() != "":
            create_card(list_id, msg)
    break
