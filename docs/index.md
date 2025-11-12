# Welcome to the Discord Audio Transcription Bot Documentation

This is the official documentation for the Discord Audio Transcription Bot.

## Overview

This Discord bot transcribes audio files sent in DMs into text. It's built with Python using the `discord.py` library and is designed to be run in a Docker container.

## Features

- Transcribes `.mp3`, `.wav`, and `.ogg` audio files.
- Responds with the transcribed text in the same DM.
- Handles `.ogg` to `.wav` conversion using `ffmpeg`.
- Modular design using `discord.py` cogs.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11
- A Discord Bot Token

### Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **Create a `.env` file:**

    Create a `.env` file in the root of the project and add the following environment variables:

    ```
    DISCORD_TOKEN=your_discord_bot_token
    WELCOME_CHANNEL_ID=your_welcome_channel_id
    ```

3.  **Run with Docker:**

    ```bash
    docker-compose up -d
    ```

### Local Development

If you prefer to run the bot locally without Docker:

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Install ffmpeg:**

    Make sure you have `ffmpeg` installed on your system. You can download it from the [official website](https://ffmpeg.org/download.html).

3.  **Run the bot:**

    ```bash
    python main.py
    ```

## Configuration

-   `DISCORD_TOKEN`: Your Discord bot token.
-   `WELCOME_CHANNEL_ID`: The ID of the channel where welcome and goodbye messages will be sent.
