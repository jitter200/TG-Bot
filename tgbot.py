import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log',
    filemode='a'
)

# Заметки
notes = {}

# API ключи
WEATHER_API_KEY = '***'
CURRENCY_API_KEY = '***'

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для заметок, погоды и курса валют. Введи /help, чтобы узнать команды.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Команды:
/note <текст> — сохранить заметку
/notes — показать все заметки
/weather <город> — погода
/rate <валюта> — курс к рублю (например, USD, EUR)
    """)

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = ' '.join(context.args)
    if text:
        notes.setdefault(user_id, []).append(text)
        await update.message.reply_text("Заметка сохранена!")
    else:
        await update.message.reply_text("Пожалуйста, укажи текст заметки после команды.")

async def show_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_notes = notes.get(user_id, [])
    if user_notes:
        await update.message.reply_text('\n'.join(user_notes))
    else:
        await update.message.reply_text("У вас нет заметок.")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи город после команды.")
        return
    city = ' '.join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url).json()
    if response.get('main'):
        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        await update.message.reply_text(f"Погода в {city}: {temp}°C, {desc}")
    else:
        await update.message.reply_text("Не удалось получить погоду. Проверь город.")

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи валюту, например USD или EUR.")
        return
    symbol = context.args[0].upper()
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{symbol}"
    response = requests.get(url).json()
    try:
        rub = response['conversion_rates']['RUB']
        await update.message.reply_text(f"1 {symbol} = {rub} RUB")
    except:
        await update.message.reply_text("Не удалось получить курс валюты. Проверь символ.")

# Запуск бота
if __name__ == '__main__':
    TOKEN = '***'
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("note", note))
    app.add_handler(CommandHandler("notes", show_notes))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("rate", rate))

    print("Бот запущен...")
    app.run_polling()
