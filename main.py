from aiogram import Bot, Dispatcher, executor, types
import logging as log
import os
from gtts import gTTS
from langdetect import detect
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()
log.basicConfig(level=log.INFO)

# Initialize bot and dispatcher
bot_token = os.getenv("BOT_TOKEN")
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Quick Settings
include_user = True


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI Stream Messages in Audio!")


@dp.message_handler()
async def echo(message: types.Message):
    if include_user == True:
        msg = f"{message.from_user.first_name} said {message.text}"
        log.info(tts(msg))
    else:
        log.warning(tts(message.text))


def tts(text):
    try:
        language = detect(text)
        myobj = gTTS(text=text, lang=language, slow=False)
        myobj.save("output.mp3")
        voice = AudioSegment.from_mp3("output.mp3")
        play(voice)
        return f"Played - {text}"
    except:
        return f"Failed - {text}"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
