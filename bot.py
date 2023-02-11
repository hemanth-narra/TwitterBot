import config
import youtube_dl
from pyrogram import Client, filters
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Get api_id and api_hash from https://my.telegram.org
api_id = int(config.API_ID)
api_hash = config.API_HASH

app = Client('my_bot', api_id, api_hash)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! I am a bot that can download videos from Twitter and send them to you.")

@app.on_message(filters.text & filters.regex(r"^https://twitter.com.*"))
async def handle_twitter_url(app, message):
    try:
        logging.info(f'got the url: {message.text}')
        tweet_url = message.text
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            logging.info("Downloading video using youtube-dl")
            ydl.download([tweet_url])
        logging.info("Sending video to the user")
        # Send the video to the user
        await message.reply_video("video.mp4")
        logging.info("Deleting video from disk")
        # Delete the video from the computer
        os.remove("video.mp4")
    except Exception as e:
        logging.error(e)
        await message.reply_text(f'Unable to find the video for {message.text}')

if __name__=="__main__":
    app.run()