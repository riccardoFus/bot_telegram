import os

import telebot

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy_random import get_random

import numpy as np

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
URI_CANTAUTORATO = os.environ.get("URI_CANTAUTORATO")
URI_RAP_ITA_UNO = os.environ.get("URI_RAP_ITA_UNO")
URI_RAP_ITA_DUE = os.environ.get("URI_RAP_ITA_DUE")
URI_ROCK = os.environ.get("URI_ROCK")
URI_RAP_FR_UNO = os.environ.get("URI_RAP_FR_UNO")
URI_RAP_FR_DUE = os.environ.get("URI_RAP_FR_DUE")
URI_INDIE = os.environ.get("URI_INDIE")
URI_STUDY = os.environ.get("URI_STUDY")
URI_LATIN = os.environ.get("URI_LATIN")
URI_ELECTRONIC = os.environ.get("URI_ELECTRONIC")
URI_CLASSICS = os.environ.get("URI_CLASSICS")

bot = telebot.TeleBot(BOT_TOKEN)
bot.parse_mode = "html"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
))
sp.trace = False

def create_answer(bot, message, it, URI):
    tracks = []
    bot.reply_to(message, "Ok, fammi pensare un pochino...")
    for offset in range(it):
        if offset == int(it/2):
            bot.send_message(message.chat.id, "Madonna, quanta musica 🙃")
        for track in sp.playlist_tracks(URI, offset=100*offset)["items"]:
            tracks.append(track['track'])
    random = np.random.random()*len(tracks)
    track = tracks[int(random)]
    output = "" + "<a href='" + track['album']['images'][0]['url'] + "'>&#8288</a>"
    output = output + track['name'] + "\n"
    output = output + "<b>"
    for artist in track['artists']:
        if(artist == track['artists'][-1]):
            output = output + "" + artist['name'] + "\n"
        else:
            output = output + artist['name'] + ", "
    output = output + "</b>"
    output = output + track['external_urls']['spotify'] + "\n"
    return output

def send_love(bot, message):
    bot.send_message(message.chat.id, "Spero questa canzone ti piaccia ❤️")

@bot.message_handler(commands=[
    'start',
    'help'
    ])
def send_welcome(message):
    output = "Ciao!\nPer usufruire dei miei consigli, usa uno di questi comandi:\n"
    output += "<b>/cantautorato : per musica cantautoriale italiana</b>\n"
    output += "<b>/rock : per musica rock</b>\n"
    output += "<b>/rap_ita : per musica rap italiana</b>\n"
    output += "<b>/rap_foreign : per musica rap straniera</b>\n"
    output += "<b>/electronic : per musica elettronica</b>\n"
    output += "<b>/latin : per musica latina</b>\n"
    output += "<b>/indie_ita : per musica indie pop italiana</b>\n"
    output += "<b>/study : per musica da studio</b>\n"
    output += "<b>/classics : per musica intramontabile</b>\n"
    output += "<b>/start o /help : in qualsiasi momento per ricordare la lista di comandi</b>\n"
    # TO-DO : TUTTA LA PARTE ALBUM + FARE PER TUTTE LE PLAYLIST
    # output += "<b>/album_rap : to-do/</b>\n"
    bot.reply_to(message, output)

@bot.message_handler(commands=[
    'cantautorato'
    ])
def echo_cantautorato(message):
    output = create_answer(bot, message, it=18, URI=URI_CANTAUTORATO)
    bot.send_message(message.chat.id, output)
    send_love(bot, message)

@bot.message_handler(commands=[
    'rock'
    ])
def echo_rock(message):
    output = create_answer(bot, message, it=12, URI=URI_ROCK)
    bot.send_message(message.chat.id, output)
    send_love(bot, message)

@bot.message_handler(commands=[
    'rap_ita'
    ])
def echo_rap_ita(message):
    choice = int(np.random.random() * 2)
    if choice == 0:
        output = create_answer(bot, message, it=7, URI=URI_RAP_ITA_UNO)
        bot.send_message(message.chat.id, output)
        send_love(bot, message)
    else:
        output = create_answer(bot, message, it=7, URI=URI_RAP_ITA_DUE)
        bot.send_message(message.chat.id, output)
        send_love(bot, message)

@bot.message_handler(commands=[
    'rap_foreign'
    ])
def echo_rap_foreign(message):
    choice = int(np.random.random() * 2)
    if choice == 0:
        output = create_answer(bot, message, it=5, URI=URI_RAP_FR_UNO)
        bot.send_message(message.chat.id, output)
        send_love(bot, message)
    else:
        output = create_answer(bot, message, it=5, URI=URI_RAP_FR_DUE)
        bot.send_message(message.chat.id, output)
        send_love(bot, message)

@bot.message_handler(commands=[
    'electronic'
    ])
def echo_electronic(message):
    output = create_answer(bot, message, it=7, URI=URI_ELECTRONIC)
    bot.send_message(message.chat.id, output)
    send_love(bot, message)

@bot.message_handler(commands=[
    'latin'
    ])
def echo_latin(message):
    output = create_answer(bot, message, it=4, URI=URI_LATIN)
    bot.send_message(message.chat.id, output)
    send_love(bot, message)

@bot.message_handler(commands=[
    'indie_ita'
    ])
def echo_indie(message):
    output = create_answer(bot, message, it=15, URI=URI_INDIE)
    bot.send_message(message.chat.id, output)
    send_love(bot, message)

@bot.message_handler(commands=[
    'study'
    ])
def echo_study(message):
    output = create_answer(bot, message, it=12, URI=URI_STUDY)
    bot.send_message(message.chat.id, output)
    send_love(bot, message)

@bot.message_handler(commands=[
    'classics'
    ])
def echo_classics(message):
    output = create_answer(bot, message, it=14, URI=URI_CLASSICS)
    bot.send_message(message.chat.id, output)
    send_love(bot, message)

bot.infinity_polling()