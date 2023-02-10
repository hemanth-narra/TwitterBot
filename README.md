# Telegram Bot for Downloading Twitter Videos

A simple telegram bot that can download videos from Twitter and send them to you.

## Getting Started

These instructions will get you a copy of the bot up and running on your Ubuntu machine for development and testing purposes.

### Prerequisites

- A telegram account and bot token
- Python 3.10 installed on your system

## Deployment on Ubuntu VPS

These steps will guide you to deploy the bot on an Ubuntu VPS

1. Update the system
`sudo apt-get update`

2. Install python and pip
`sudo apt-get install python3 python3-pip`
### Installing

3. Clone the repository
`https://github.com/hemanth-narra/TwitterBot.git`

4. Install the required packages
`pip3 install -r requirements.txt`

5. Edit sample_config.py with your values and save as config.py

6. Finally run the bot
`python3 bot.py`


## Built With

- [Pyrogram](https://docs.pyrogram.org/intro/quickstart) - The MTProto API framework for Telegram
- [youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html) - A command-line program to download videos from YouTube.com and a few more sites

## Contributing

Feel free to create a pull request or issue if you have any suggestions or bugs to report.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



