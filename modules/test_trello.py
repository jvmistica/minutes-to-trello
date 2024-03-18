import unittest
from modules.trello import create_board, create_list, create_card
from unittest.mock import Mock, patch

class TestTrello(unittest.TestCase):

    def test_create_board(self):
        with patch('modules.trello.requests.request') as mock_request:
            response_mock = Mock(status_code=201)
            response_mock.json.return_value = {'shortUrl': 'etc/test_board_id'}
    
            mock_request.return_value = response_mock
            result = create_board('a new board')
    
            mock_request.assert_called_with('POST', 'https://api.trello.com/1/boards/', params={'name': 'a new board', 'key': 'key', 'token': 'token'})
            self.assertEqual(result, 'test_board_id')

    def test_create_list(self):
        with patch('modules.trello.requests.request') as mock_request:
            response_mock = Mock(status_code=201)
            response_mock.json.return_value = {'id': 'test_list_id'}
    
            mock_request.return_value = response_mock
            result = create_list('test_board_id', 'a new list')
    
            mock_request.assert_called_with('POST', 'https://api.trello.com/1/boards/test_board_id/lists', params={'name': 'a new list', 'key': 'key', 'token': 'token'})
            self.assertEqual(result, 'test_list_id')

    def test_create_card(self):
        with patch('modules.trello.requests.request') as mock_request:
            response_mock = Mock(status_code=201)
            response_mock.json.return_value = {'id': 'test_card_id'}
    
            mock_request.return_value = response_mock
            result = create_card('test_list_id', 'a new card')
    
            mock_request.assert_called_with('POST', 'https://api.trello.com/1/cards', params={'name': 'a new card', 'idList': 'test_list_id', 'key': 'key', 'token': 'token'})
            self.assertEqual(result, 'test_card_id')

if __name__ == '__main__':
    unittest.main()
