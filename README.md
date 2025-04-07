# Telegram Bot — Notes, Weather, Exchange Rates

📦 A Telegram bot that combines three simple but useful features:
- Personal notes
- Weather forecast by city
- Currency exchange rates (e.g., USD, EUR to RUB)

Built with Python and `python-telegram-bot`. Uses external APIs: OpenWeather and ExchangeRate.

---

## 🚀 Features

- `/note <text>` — Save a personal note
- `/notes` — View your saved notes
- `/weather <city>` — Get the current weather
- `/rate <currency>` — Get exchange rate to RUB

---

## 🧰 Tech Stack

- Python 3.10+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [OpenWeather API](https://openweathermap.org/api)
- [ExchangeRate API](https://www.exchangerate-api.com)
- Logging via Python's built-in `logging` module

---

## Logging
- All actions and errors are logged to bot.log.
