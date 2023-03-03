import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
import config

# initialize the Pyrogram client
bot = Client("twvid", api_id=int(config.API_ID), api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start_command(bot, message):
    # send a welcome message to the user
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hi! I'm a bot that can help you download videos from Twitter. Just send me a Twitter URL and I'll do the rest! Please note that I can only download videos, not photos.",
        quote=True
    )

# define a filter to only allow messages containing a Twitter URL
@bot.on_message(filters.private & filters.regex(r"https?://twitter\.com/.*/status/\d+"))
async def process_tweet_url(bot, message):
    # show a chat action while the videos are being processed
    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)

    # get the tweet URL from the message
    tweet_url = message.text.strip()
    
    # create a new Firefox browser window using Selenium
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    
    try:
        # navigate to the website's homepage
        driver.get("https://twittervid.com/")

        # wait for the tweet URL input field to appear
        tweet_url_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tweetUrl"))
        )

        # enter the tweet URL into the input field
        tweet_url_input.send_keys(tweet_url)

        # find the "Load Videos" button and click it
        load_videos_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loadVideos"))
        )

        time.sleep(1)

        load_videos_button.click()

        # wait for the videos to load
        time.sleep(5)

        # get the page source after the videos have loaded
        page_source = driver.page_source

        # parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # find all div tags with class "thumbnail-div"
        thumbnail_divs = soup.find_all('div', {'class': 'thumbnail-div'})

        # loop through the list of thumbnail divs and extract the href attribute values from the a tags
        video_urls = []
        for thumbnail_div in thumbnail_divs:
            a_tag = thumbnail_div.find('a')
            href = a_tag['href']
            video_urls.append(href)

        # loop through the video URLs and download each video in chunks
        for i, url in enumerate(video_urls):
            response = requests.get(url, stream=True)
            with open(f"video{i+1}.mp4", "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            
            await bot.send_video(
                chat_id=message.chat.id,
                video=f"video{i+1}.mp4",
                caption=f"[Tweet]({tweet_url}) - Video {i+1} of {len(video_urls)}"
            )

            # delete the downloaded video file
            os.remove(f"video{i+1}.mp4")
    
    except Exception as e:
        # handle any errors that occur during processing
        await bot.send_message(
            chat_id=message.chat.id,
            text="An error occurred while processing the tweet. Please try again later."
        )
        print(e)
    
    finally:
        # close the browser window
        driver.quit()

# start the bot
if __name__=='__main__':
    bot.run()
