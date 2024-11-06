import telebot
import requests
from pytube import YouTube
import re

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot('8106073578:AAGKWjDEc3m6d3KlsTLoRdnztDH5Zqe7BTI')

# Функция для загрузки видео с YouTube
def download_youtube_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download()
        return file_path
    except Exception as e:
        print(f"Ошибка загрузки видео с YouTube: {e}")
        return None

# Функция для загрузки видео с TikTok без водяного знака
def download_tiktok_video(url):
    try:
        api_url = f"https://api.tiktokv.com/redirect/?link={url}"
        response = requests.get(api_url)
        video_url = re.search(r'https://[^\s]+', response.text)
        if video_url:
            video_data = requests.get(video_url.group(), stream=True)
            file_path = 'tiktok_video.mp4'
            with open(file_path, 'wb') as file:
                for chunk in video_data.iter_content(chunk_size=1024):
                    file.write(chunk)
            return file_path
        return None
    except Exception as e:
        print(f"Ошибка загрузки видео с TikTok: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на YouTube, YouTube Shorts или TikTok видео.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text

    # Проверка ссылки и загрузка видео
    if "youtube.com" in url or "youtu.be" in url:
        bot.reply_to(message, "Скачиваю видео с YouTube...")
        video_path = download_youtube_video(url)
    elif "tiktok.com" in url:
        bot.reply_to(message, "Скачиваю видео с TikTok без водяного знака...")
        video_path = download_tiktok_video(url)
    else:
        bot.reply_to(message, "Неизвестный формат ссылки. Поддерживаются только YouTube и TikTok.")
        return

    # Отправка видео пользователю
    if video_path:
        with open(video_path, 'rb') as video:
            bot.send_video(message.chat.id, video)
    else:
        bot.reply_to(message, "Не удалось скачать видео. Попробуйте другую ссылку.")

bot.polling()
