#!/usr/bin/env python3
"""
Unit tests for the Random Joke Generator
Tests API integration and joke display functionality
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from joke_generator import JokeGenerator


class TestJokeGenerator:
    """Test cases for JokeGenerator class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.generator = JokeGenerator()
    
    def test_init_default(self):
        """Test JokeGenerator initialization with default parameters"""
        assert self.generator.safe_mode == False
        assert self.generator.BASE_URL == "https://v2.jokeapi.dev/joke"
    
    def test_init_safe_mode(self):
        """Test JokeGenerator initialization with safe mode"""
        generator = JokeGenerator(safe_mode=True)
        assert generator.safe_mode == True
    
    @patch('requests.Session.get')
    def test_fetch_joke_single(self, mock_get):
        """Test fetching a single-type joke"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "single",
            "joke": "Why don't scientists trust atoms? Because they make up everything!",
            "error": False
        }
        mock_get.return_value = mock_response
        
        joke = self.generator.fetch_joke()
        
        assert joke is not None
        assert joke["type"] == "single"
        assert "joke" in joke
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_fetch_joke_twopart(self, mock_get):
        """Test fetching a two-part joke"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "twopart",
            "setup": "Why did the programmer quit his job?",
            "delivery": "Because he didn't get arrays!",
            "error": False
        }
        mock_get.return_value = mock_response
        
        joke = self.generator.fetch_joke(category="Programming", joke_type="twopart")
        
        assert joke is not None
        assert joke["type"] == "twopart"
        assert "setup" in joke
        assert "delivery" in joke
    
    @patch('requests.Session.get')
    def test_fetch_joke_with_safe_mode(self, mock_get):
        """Test fetching jokes with safe mode enabled"""
        generator = JokeGenerator(safe_mode=True)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "single",
            "joke": "A safe joke",
            "error": False
        }
        mock_get.return_value = mock_response
        
        joke = generator.fetch_joke()
        
        assert joke is not None
        # Check that safe-mode was passed in params
        call_args = mock_get.call_args
        assert call_args[1]["params"]["safe-mode"] == True
    
    @patch('requests.Session.get')
    def test_fetch_joke_api_error(self, mock_get):
        """Test handling of API errors"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "error": True,
            "message": "Invalid category"
        }
        mock_get.return_value = mock_response
        
        joke = self.generator.fetch_joke(category="Invalid")
        
        assert joke is None
    
    @patch('requests.Session.get')
    def test_fetch_joke_timeout(self, mock_get):
        """Test handling of request timeout"""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()
        
        joke = self.generator.fetch_joke()
        
        assert joke is None
    
    @patch('requests.Session.get')
    def test_fetch_joke_connection_error(self, mock_get):
        """Test handling of connection errors"""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        joke = self.generator.fetch_joke()
        
        assert joke is None
    
    @patch('builtins.print')
    def test_display_joke_single(self, mock_print):
        """Test displaying a single-type joke"""
        joke_data = {
            "type": "single",
            "joke": "Test joke"
        }
        
        self.generator.display_joke(joke_data)
        
        # Check that the joke was printed
        assert any("Test joke" in str(call) for call in mock_print.call_args_list)
    
    @patch('builtins.print')
    def test_display_joke_twopart(self, mock_print):
        """Test displaying a two-part joke"""
        joke_data = {
            "type": "twopart",
            "setup": "Setup text",
            "delivery": "Delivery text"
        }
        
        self.generator.display_joke(joke_data)
        
        # Check that both setup and delivery were printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Setup" in call for call in print_calls)
        assert any("Delivery" in call for call in print_calls)
    
    @patch('requests.Session.get')
    @patch('builtins.print')
    def test_get_random_joke_success(self, mock_print, mock_get):
        """Test getting and displaying a random joke successfully"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "type": "single",
            "joke": "Test joke",
            "error": False
        }
        mock_get.return_value = mock_response
        
        self.generator.get_random_joke()
        
        # Verify the joke was processed
        assert mock_get.called
    
    def test_valid_categories(self):
        """Test that valid categories are defined"""
        assert len(self.generator.VALID_CATEGORIES) > 0
        assert "Programming" in self.generator.VALID_CATEGORIES


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
