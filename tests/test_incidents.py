import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from health_check import check_health

def test_health_check_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200)
        result = check_health("https://example.com")
        assert result == True

def test_health_check_failure():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=500)
        result = check_health("https://example.com")
        assert result == False

def test_health_check_timeout():
    import requests
    with patch('requests.get', side_effect=requests.exceptions.Timeout):
        result = check_health("https://example.com")
        assert result == False
