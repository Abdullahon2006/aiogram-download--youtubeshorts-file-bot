import os
import asyncio
import pytube
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# Your Telegram bot token
API_TOKEN = 'YOUR_BOT_TOKEN'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Handler for the "/start" command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi there! Please send me a YouTube link and I'll download the video for you.")

# Handler for messages containing YouTube links
@dp.message_handler(regexp=r'(https?://[^\s]+)')
async def download_video(message: types.Message):
    # Get the YouTube link from the message
    url = message.text.strip()
    try:
        # Download the video
        youtube = pytube.YouTube(url)
        video = youtube.streams.get_highest_resolution()
        video_file = f"{youtube.title}.mp4"
        video.download(filename=video_file)
        # Send the video as a file
        with open(video_file, 'rb') as file:
            await bot.send_video(message.chat.id, file)
        # Delete the downloaded file
        os.remove(video_file)
        # Notify the user
        await message.reply("Download complete!")
    except Exception as e:
        print(e)
        await message.reply("Sorry, something went wrong while downloading the video.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
