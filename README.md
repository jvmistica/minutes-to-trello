# Minutes to Trello
Reads minutes of the meeting emails from Gmail, retrieves the action items, and uploads them to Trello.

## Getting Started

Login to your Google account and download the credentials.json file from: https://developers.google.com/gmail/api/quickstart/python. Save the file to the same folder as the main.py script.

Install the required modules:
```
pip install -r requirements.txt
```

Get your key and token from https://trello.com/app-key and modify the settings.py file:
```
key = "your_key"
token = "your_token"
```

Run the main script:
```
python main.py
```
