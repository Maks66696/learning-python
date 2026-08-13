import io
import os
import csv
import datetime
import matplotlib
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import requests
import geopy
from geopy.geocoders import Nominatim
from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


matplotlib.use("Agg")  
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

WEATHER_CODES = {
    0: "☀️ Ясно",
    1: "🌤️ Малооблачно",
    2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно",
    45: "🌫️ Туман",
    51: "🌧️ Морось",
    61: "🌧️ Небольшой дождь",
    63: "🌧️ Умеренный дождь",
    65: "🌧️ Сильный дождь",
    71: "❄️ Небольшой снег",
    73: "❄️ Снегопад",
    80: "🌦️ Ливень",
    95: "🌩️ Гроза",
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
    city_name = str(city_name).split(',')[0].strip()
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m&forecast_days=1"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return "⚠️ Сервис погоды временно недоступен. Попробуйте позже!", None

    current = data["current_weather"]
    temp = current["temperature"]
    code = current["weathercode"]
    wind = current["windspeed"]

    temps= data["hourly"]["temperature_2m"][:24]
    raw_times = data["hourly"]["time"][:24]
    formatted_times = [
         datetime.datetime.fromisoformat(t).strftime("%H:%M") for t in 
         raw_times
    ]
    status = WEATHER_CODES.get(code, "🌈 Погода")

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
    chart_file = create_chart(formatted_times, temps, city_name)

    text = (
        f"Погода в **{city_name}**: {temp}°C\n{status}\n💨 Ветер:"
        f" {wind} км/ч\n\n{advice}"
    )
    log_request(city_name, temp)
    return text, chart_file


@bot.message_handler(func=lambda message: message.text in CITIES.keys())
def send_weather(message):
    city_name = message.text
    lat=CITIES[city_name]["lat"]
    lon=CITIES[city_name]["lon"]
    inline_markup = get_refresh_keyboard(lat, lon, city_name)
    text, chart_buf = get_weather_report(lat, lon, city_name)
    if chart_buf is None:
        bot.send_message(message.chat.id, text)
    else:
        bot.send_photo(
         message.chat.id, photo=chart_buf, caption=text, parse_mode="Markdown", reply_markup = inline_markup,
    )


@bot.message_handler(content_types=['text'])
def text_search(message):
    location = geolocator.geocode(message.text, language="ru")
    if location is None:
        bot.send_message(message.chat.id, "Город не найден!")
        return
    lat = location.latitude
    lon = location.longitude
    city_title = location.address.split(',')[0]
    inline_markup = get_refresh_keyboard(lat, lon, city_title)
    text, chart_buf = get_weather_report(lat, lon, city_title)
    if chart_buf is None:
        bot.send_message(message.chat.id, text)
    else:
        bot.send_photo(
        message.chat.id, photo=chart_buf, caption=text, parse_mode="Markdown", reply_markup = inline_markup,
    )


@bot.message_handler(content_types=["location"])
def handle_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    location = geolocator.reverse((lat, lon), language='ru')
    address = location.raw.get('address', {})
    city_name = address.get('city') or address.get('town') or address.get('village') or "вашей локации"

    text, chart_buf = get_weather_report(lat, lon, city_name)
    inline_markup = get_refresh_keyboard(lat, lon, city_name)

    if chart_buf is None:
        bot.send_message(message.chat.id, text)
    else:
        bot.send_photo(
        message.chat.id, photo=chart_buf, caption=text, parse_mode="Markdown", reply_markup = inline_markup,
    )

def get_refresh_keyboard(lat, lon, city_name):
    markup = InlineKeyboardMarkup()
    callback_string = f"refresh_{lat}_{lon}_{city_name}"
    btn_refresh = InlineKeyboardButton(
        "🔄 Обновить", callback_data = callback_string
    )
    markup.add(btn_refresh)
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswitch("refresh_"))
def handle_refresh(call):
    bot.answer_callback_query(call.id, "🔄 Обновляю данные погоды...")
    parts = call.data.split("_")
    lat = float(parts[1])
    lon = float(parts[2])
    city_name = parts[3]

    text , chart_buf = get_weather_report(lat,lon, city_name)

    if chart_buf:
        inline_markup = get_weather_report(lat, lon, city_name)
        bot.send_photo(
            call.message.chat.id,
            photo=chart_buf,
            caption=text,
            parse_mode="Markdown",
            reply_markup=inline_markup,
        )

def log_request(city_name, temp):
     current_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
     with open("logs.csv", "a", encoding="utf-8", newline="") as file:
          now = [current_date,temp,city_name]
          csv_writer = csv.writer(file)
          csv_writer.writerow(now)

def create_chart(times, temps, city_name):
     
     plt.figure(figsize= (10,5))
     plt.plot(times, temps, marker="o", color="#1E88E5", linewidth=2)
     plt.title(f"Прогноз погоды на 24 часа: {city_name}", fontsize=14)
     plt.xlabel("Время", fontsize=10)
     plt.ylabel("Температура (°C)", fontsize=10)
     plt.grid(True, linestyle="--", alpha=0.5)
     plt.xticks(rotation=45)
     buf = io.BytesIO()
     plt.savefig(buf, format="png", bbox_inches = "tight")
     buf.seek(0)
     plt.close()

     return buf
     
    
bot.infinity_polling()


