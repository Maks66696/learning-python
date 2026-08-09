import requests
from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

TOKEN = "..."
bot = TeleBot(TOKEN)


CITIES = {
    "Москва": {"lat": 55.7558, "lon": 37.6173},
    "Санкт-Петербург": {"lat": 59.9343, "lon": 30.3351},
    "Екатеринбург": {"lat": 56.8389, "lon": 60.6057},
    "Сосьва": {"lat": 59.174, "lon": 61.849},
    "Сочи": {"lat": 43.6028, "lon": 39.7342},
}

bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    for city in CITIES.keys():
        item_button = KeyboardButton(city)
        markup.add(item_button)
    bot.send_message(message.chat.id, "Выбери город", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CITIES.keys())
def send_weather(message):
    city_name = message.text
    lat=CITIES[city_name]["lat"]
    lon=CITIES[city_name]["lon"]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response=requests.get(url)
    data=response.json()
    temp=data["current_weather"]["temperature"]
    if temp < 0:
        advice = "На улице мороз! Надевай пуховик, шапку и шарф."
    elif temp < 15:
        advice = "Прохладно. Надевай куртку или тёплую худи."
    elif temp < 22:
        advice = "Приятная погода. Подойдёт кофта или ветровка."
    else:
        advice = " Жара! Надевай футболку и шорты."
    text= f"Погода в **{city_name}**: {temp}°C\n\n{advice}"

    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.infinity_polling()