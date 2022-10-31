# -*- coding: utf-8 -*-

import requests
from unittest.mock import patch, MagicMock
from function import clean_search
from function import search_google
from function import search_wikipedia


def test_clean_search():
	assert clean_search("salut paris") == "paris"
	assert clean_search('&&&& je veux !$paris') == "paris"
	assert clean_search('@@-* je veux !$paris') == "paris"
	assert clean_search("Bonjou'r à une information sur paris") =="Bonjour information paris"


@patch('function.requests')
def test_search_google(mock_requests):
	mock_response = MagicMock()
	mock_response.json.return_value = {
	'candidates': [{"formatted_address": '27 rue test_adresse', 'geometry':{'location':{'lat':10, 'lng':20}},}]
	}
	mock_requests.request.return_value = mock_response
	#mock_requests.get.return_value = mock_response
	result = search_google("paris")
	assert result == (10, 20, '27 rue test_adresse')


@patch('function.requests')
def test_search_google_empty_response(mock_requests):
	mock_response = MagicMock()
	mock_response.json.return_value = {
	'candidates': []
	}
	mock_requests.request.return_value = mock_response
	#mock_requests.get.return_value = mock_response
	result = search_google("paris")
	assert result is None


@patch('function.requests')
def test_search_google_unavailable(mock_requests):
	mock_response = MagicMock()
	mock_response.ok = False
	mock_requests.request.return_value = mock_response
	#mock_requests.get.return_value = mock_response
	result = search_google("paris")
	assert result is None


# def test_search_wikipedia():
# assert search_wikipedia()