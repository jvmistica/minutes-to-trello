import requests
from settings import key, token


def create_board(board_name):
    url = "https://api.trello.com/1/boards/"
    querystring = {"name": board_name, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    board_id = response.json()["shortUrl"].split("/")[-1].strip()
    return board_id


def create_list(board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    querystring = {"name": list_name, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    list_id = response.json()["id"]
    return list_id


def create_card(list_id, card_name):
    url = f"https://api.trello.com/1/cards"
    querystring = {"name": card_name, "idList": list_id, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    card_id = response.json()["id"]
    return card_id
