# Random Joke Generator

A simple random joke generator using the JokeAPI external service.

## Features
- Fetch random jokes from an external API
- Support for different joke types and categories
- Simple command-line interface
- Error handling for API failures
- Option to filter by safety rating

## Installation

```bash
git clone https://github.com/Sujay1709/Random_joke_generator.git
cd Random_joke_generator
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python joke_generator.py
```

### With Specific Category
```bash
python joke_generator.py --category programming
```

### With Safety Filter
```bash
python joke_generator.py --safe-mode
```

### Get Multiple Jokes
```bash
python joke_generator.py --count 5
```

## API Used
- **JokeAPI**: https://jokeapi.dev/

## Supported Categories
- General
- Programming
- Knock-Knock
- Science
- Christmas
- Random (default - Any)

## Joke Types
- Single (one-liner jokes)
- Two-part (setup and delivery)
- Both

## License
MIT

## Contributing
Feel free to fork this repository and submit pull requests for any improvements!