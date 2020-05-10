import base64
from googleapiclient.discovery import build
from modules.gmail import create_access_token, generate_service, query_messages, get_message
from modules.trello import create_board, create_list, create_card
from settings import email_address, scopes, subject, items_start, items_end


creds = create_access_token()
generate_service(creds, scopes)
service = build("gmail", "v1", credentials=creds)
messages = query_messages(service, email_address, subject)

for message in messages:
    body = get_message(service, email_address, message.get("id"))
    subject = next(header["value"] for header in body["payload"]["headers"] \
                   if header["name"] == "Subject")
    message = base64.b64decode([part["body"]["data"] for part in body["payload"]["parts"] \
                               if part["mimeType"] == "text/plain"][0]).decode("utf-8")
    message_split = message.split("\r\n")
    message_split = message_split[message_split.index(items_start): message_split.index(items_end)]
    list_id = create_list(create_board(subject), items_start)
    for msg in message_split[1:-1]:
        if msg.strip() != "":
            create_card(list_id, msg)
    break
