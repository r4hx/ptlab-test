#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import random
from datetime import datetime

import telebot
from PIL import Image, ImageDraw, ImageFont
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

text_file = os.getenv('TEXT_FILE')
images_dir = os.getenv('IMAGE_DIR')
font_file = os.getenv('FONT_FILE')
repost_channel = os.getenv('REPOST_CHANNEL')
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


def gen_markup() -> object:
    '''generate inline keyboard for share pic'''
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Поделиться", callback_data="share_this"))
    return markup


def get_random_text(text_file=text_file) -> str:
    '''get one random line from text file'''
    text_list = [i.strip() for i in open(text_file).readlines()]
    return random.choice(text_list)


def write_text_photo(filepath, text) -> None:
    '''draw text to received photo'''
    image = Image.open(filepath)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file, size=40, encoding="utf-8")
    width_image, height_image = image.size
    width_text, height_text = draw.textsize(text, font=font)
    draw.text(
        ((width_image - width_text) / 2 + 1, ((height_image / 10) * 9) + 1),
        text,
        font=font,
        fill=(0, 0, 0, 0)
    )
    draw.text(
        ((width_image - width_text) / 2, ((height_image / 10) * 9)),
        text,
        font=font,
        fill=(255, 0, 0, 0)
    )
    image.save(filepath)


@bot.message_handler(commands=['start'])
def welcome(message):
    '''welcome msg'''
    bot.send_message(message.chat.id, "Здарова, бродяга! Ты мне фотку, я тебе мем.")


@bot.message_handler(content_types=['photo'])
def image(message) -> None:
    '''processing incoming image'''
    bot.reply_to(message, "Сейчас наколдую")
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    file_downloaded = bot.download_file(file_info.file_path)
    file_name = "{}_{}.jpg".format(datetime.now().strftime("%Y-%m-%d_%H:%M"), message.from_user.id)
    file_path = "{}/{}".format(images_dir, file_name)
    with open(file_path, 'wb') as file_new:
        file_new.write(file_downloaded)
    text = get_random_text()
    write_text_photo(file_path, text)
    with open(file_path, 'rb') as f:
        bot.send_photo(message.chat.id, f, reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call) -> None:
    '''grab callback from inline keyboard'''
    if call.data == "share_this":
        bot.answer_callback_query(call.id, "Окей!")
        bot.forward_message(repost_channel, call.from_user.id, call.message.message_id)


# start bot
bot.polling()
