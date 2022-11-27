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
	'candidates': [{"formatted_address": '27 rue test_adresse', 'geometry':{'location':{'lat':30, 'lng':20}},}]
	}
	mock_requests.request.return_value = mock_response
	#mock_requests.get.return_value = mock_response
	result = search_google("paris")
	assert result == (30, 20, '27 rue test_adresse')


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


@patch('function.requests')
def test_search_wikipedia_1(mock_requests):
	mock_response = MagicMock()
	mock_response.json.return_value = {
	'query': {"pages" : {'11498241' : {'pageid': 11498241, 'ns': 0, 'title': 'Place Sébastopol', 'index': -1, 'extract': "Bonjour lille"}}}
	}
	mock_requests.request.return_value = mock_response
	result = search_wikipedia(10,20)
	assert result == "Bonjour lille"



@patch('function.requests')
def test_search_wikipedia_2(mock_requests):
	mock_response = MagicMock()
	mock_response.json.return_value = {'query' :{}}
	mock_requests.request.return_value = mock_response
	result = search_wikipedia(10,20)
	assert result == "Oups !.. Je n'ai aucune information à ce sujet essayez autres choses !"


@patch('function.requests')
def test_search_wikipedia_3(mock_requests):
	mock_response = MagicMock()
	mock_response.ok = False
	mock_requests.request.return_value = mock_response
	result = search_wikipedia(10,20)
	assert result == "Oups !.. Je n'ai aucune information à ce sujet essayez autres choses !"