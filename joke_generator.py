#!/usr/bin/env python3
"""
Random Joke Generator using JokeAPI
Fetches and displays random jokes from an external API
"""

import requests
import argparse
import sys
from typing import Dict, Optional


class JokeGenerator:
    """A class to fetch and manage jokes from JokeAPI"""
    
    BASE_URL = "https://v2.jokeapi.dev/joke"
    VALID_CATEGORIES = ["General", "Programming", "Knock-Knock", "Science", "Christmas"]
    
    def __init__(self, safe_mode: bool = False):
        """
        Initialize the JokeGenerator
        
        Args:
            safe_mode (bool): If True, fetch only safe jokes
        """
        self.safe_mode = safe_mode
        self.session = requests.Session()
    
    def fetch_joke(self, category: str = "Any", joke_type: str = "any") -> Optional[Dict]:
        """
        Fetch a random joke from the API
        
        Args:
            category (str): Category of joke (Any, General, Programming, Knock-Knock, Science, Christmas)
            joke_type (str): Type of joke (any, single, twopart)
            
        Returns:
            Dict: Joke data or None if request fails
        """
        try:
            params = {
                "type": joke_type,
            }
            
            # Add safety filter if enabled
            if self.safe_mode:
                params["safe-mode"] = True
            
            url = f"{self.BASE_URL}/{category}"
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("error"):
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return None
            
            return data
            
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the API. Please check your internet connection.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
            return None
    
    def display_joke(self, joke_data: Dict) -> None:
        """
        Display the joke in a formatted way
        
        Args:
            joke_data (Dict): Joke data from the API
        """
        if not joke_data:
            return
        
        print("\n" + "="*50)
        
        if joke_data.get("type") == "single":
            print(joke_data.get("joke", "No joke found"))
        elif joke_data.get("type") == "twopart":
            print(f"Setup: {joke_data.get('setup', '')}")
            print(f"Delivery: {joke_data.get('delivery', '')}")
        
        print("="*50 + "\n")
    
    def get_random_joke(self, category: str = "Any", joke_type: str = "any") -> None:
        """
        Get and display a random joke
        
        Args:
            category (str): Category of joke
            joke_type (str): Type of joke
        """
        joke = self.fetch_joke(category, joke_type)
        if joke:
            self.display_joke(joke)
        else:
            print("Failed to fetch joke. Please try again.")


def main():
    """Main function to handle command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Fetch and display random jokes from JokeAPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python joke_generator.py                          # Get a random joke
  python joke_generator.py --category programming   # Get a programming joke
  python joke_generator.py --safe-mode              # Get a safe joke
  python joke_generator.py --type single            # Get a single-line joke
        """
    )
    
    parser.add_argument(
        "--category",
        type=str,
        default="Any",
        help="Category of joke: Any, General, Programming, Knock-Knock, Science, Christmas (default: Any)"
    )
    
    parser.add_argument(
        "--type",
        dest="joke_type",
        type=str,
        default="any",
        choices=["any", "single", "twopart"],
        help="Type of joke: any, single, twopart (default: any)"
    )
    
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="Enable safe mode to fetch only safe jokes"
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of jokes to fetch (default: 1)"
    )
    
    args = parser.parse_args()
    
    # Validate category
    if args.category not in JokeGenerator.VALID_CATEGORIES and args.category != "Any":
        print(f"Invalid category: {args.category}")
        print(f"Valid categories: {', '.join(JokeGenerator.VALID_CATEGORIES + ['Any'])}")
        sys.exit(1)
    
    # Validate count
    if args.count < 1:
        print("Count must be at least 1")
        sys.exit(1)
    
    # Create generator and fetch jokes
    generator = JokeGenerator(safe_mode=args.safe_mode)
    
    print(f"Fetching {args.count} joke(s)...")
    
    for i in range(args.count):
        generator.get_random_joke(args.category, args.joke_type)


if __name__ == "__main__":
    main()
