import os
from dotenv import load_dotenv
import requests
import geopy
from geopy.geocoders import Nominatim
from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

geolocator = Nominatim(user_agent="my_weather_bot")
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(TOKEN)
CITIES = {
    "Москва": {"lat": 55.7558, "lon": 37.6173},
    "Санкт-Петербург": {"lat": 59.9343, "lon": 30.3351},
    "Екатеринбург": {"lat": 56.8389, "lon": 60.6057},
    "Сочи": {"lat": 43.6028, "lon": 39.7342},
}

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    btn_location = KeyboardButton("Отправить геолокацию", request_location=True)
    markup.add(btn_location)
    for city in CITIES.keys():
        item_button = KeyboardButton(city)
        markup.add(item_button)
    bot.send_message(message.chat.id, "Выбери город", reply_markup=markup)

def get_weather_report(lat, lon, city_name):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    temp = data["current_weather"]["temperature"]
    advice = "Одевайся по погоде!"
    if temp <= 0:
        advice = "На улице мороз! Надевай пуховик, шапку и шарф."
    elif temp <= 15:
        advice = "Прохладно. Надевай куртку или тёплую худи."
    elif temp <= 22:
        advice = "Приятная погода. Подойдёт кофта или ветровка."
    elif temp < 35:
        advice = "Жара! Надевай футболку и шорты."
    else:
        advice = "Экстремальная жара! Не выходи на солнце без кепки и пей больше воды!"

    
    return f"Погода в **{city_name}**: {temp}°C\n\n{advice}"

@bot.message_handler(func=lambda message: message.text in CITIES.keys())
def send_weather(message):
    city_name = message.text
    lat=CITIES[city_name]["lat"]
    lon=CITIES[city_name]["lon"]
    text = get_weather_report(lat, lon, city_name)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(content_types=['text'])
def text_search(message):
    location = geolocator.geocode(message.text, language="ru")
    if location is None:
        bot.send_message(message.chat.id, "Город не найден!")
        return
    lat = location.latitude
    lon = location.longitude
    city_title = location.address.split(',')[0]
    text = get_weather_report(lat, lon, city_title)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(content_types=["location"])
def handle_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    location = geolocator.reverse((lat, lon), language='ru')
    address = location.raw.get('address', {})
    city_name = address.get('city') or address.get('town') or address.get('village') or "вашей локации"
    text = get_weather_report(lat, lon, city_name)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
bot.infinity_polling()
