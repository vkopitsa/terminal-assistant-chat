# TerminalAssistantChat

This project is a chatbot that uses OpenAI's GPT-3/4 model for generating responses. The model is capable of handling function calling and executing tasks based on instructions provided in the conversation. The chatbot can be run as a console-based chat application or as a Telegram bot.

[![asciicast](https://asciinema.org/a/B7OUsOfDIq1th9yGyu33dnG4j.svg)](https://asciinema.org/a/B7OUsOfDIq1th9yGyu33dnG4j)

## Getting Started

### Prerequisites

- Python 3.7 or higher
- OpenAI Python package
- Telegram Python package
- Docker

### Environment Variables

Before running the application, you need to set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `TG_API_KEY`: Your Telegram API key
- `TG_ADMIN_CHAT_ID`: The chat ID of the Telegram admin
- `TG_USER_ACCESS`: A comma-separated list of authorized user IDs

## Usage

### Running as a Console-based Chat

To run the application as a console-based chat, execute the script with no arguments:

```bash
python main.py
```

### Running as a Telegram Bot

To run the application as a Telegram bot, execute the script with the "telegram" argument:

```bash
python main.py telegram
```

### Running the app in a Docker Container

Before you run the Docker container, you need to ensure that you have set the necessary environment variables in your .env file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `TG_API_KEY`: Your Telegram API key
- `TG_ADMIN_CHAT_ID`: The chat ID of the Telegram admin
- `TG_USER_ACCESS`: A comma-separated list of authorized user IDs

Once the environment variables are set, you can run the application inside a Docker container using the following command:

```bash
docker-compose up -d
```

If you want to run the script as Console-based Chat inside the Docker container:

```bash
docker-compose run bot python3 main.py
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- OpenAI for the GPT-3/4 model
- Python-Telegram-Bot developers for the Telegram Bot wrapper
