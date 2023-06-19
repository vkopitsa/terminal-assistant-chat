# TerminalAssistantChat

This project is a chatbot that uses OpenAI's GPT-3/4 model for generating responses. The model is capable of handling function calling and executing tasks based on instructions provided in the conversation. The chatbot can be run as a console-based chat application or as a Telegram bot.

[![asciicast](https://asciinema.org/a/B7OUsOfDIq1th9yGyu33dnG4j.svg)](https://asciinema.org/a/B7OUsOfDIq1th9yGyu33dnG4j)

## Features

- **Execute bash code or terminal command:** This allows the bot to execute bash commands and return the results directly in the chat.
- **Execute Python code or expressions:** The bot can execute Python expressions and return the result. This can be helpful for quick calculations or other operations.
    - **Can install missing Python modules:** If the bot requires a specific Python module that is not currently installed, it can handle the installation process.
- **Sends a file to/from a Telegram chat:** The bot can send and receive files to/from a Telegram chat, which can be useful for sharing resources.
- **Gets the content of a website:** The bot can fetch and display the content of a website or URI.
- **Can search queries using the `ddgr` command:** The bot can search the web (using Google) with the bash command: ddgr --json -n 3 [search keywords].


## Getting Started

### Prerequisites

- Python 3.10 or higher
- OpenAI Python package
- Telegram Python package
- Docker

### Environment Variables

Before running the application, you need to set the following environment variables:

- `OPENAI_API_KEY`: OpenAI API key
- `TG_API_KEY`: Telegram API key
- `TG_USER_ACCESS`: A comma-separated list of authorized user IDs
- `OPENAI_MODEL`: (Optional) A OpenAI model, default `gpt-3.5-turbo-0613`

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

- `OPENAI_API_KEY`: OpenAI API key
- `TG_API_KEY`: Telegram API key
- `TG_USER_ACCESS`: A comma-separated list of authorized user IDs
- `OPENAI_MODEL`: (Optional) A OpenAI model, default `gpt-3.5-turbo-0613`

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
