import telebot
from fluent import sender
from fluent import event
from prometheus_client import start_http_server, Counter, Gauge
import time
import random

# Ініціалізація метрик
REQUEST_COUNT = Counter('request_count', 'Total request count')

# Create a gauge metric to measure system memory usage
memory_usage = Gauge('memory_usage_in_bytes', 'System Memory Usage')


def process_request():
    REQUEST_COUNT.inc()
    time.sleep(random.random())

sender.setup('fluentd.bot', host='localhost', port=8080)

API_TOKEN = "7185531631:AAH-llTUqR4z2nWuNUEfic45SV1EsThFO7g"

bot = telebot.TeleBot(API_TOKEN)

# Define a command handler
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    process_request()
    event.Event('start message', {
        'user_id': message.from_user.id,
        'user_name':   message.from_user.username
        })
    bot.reply_to(message, "Welcome to YourBot! Type /info to get more information.")

@bot.message_handler(commands=["info"])
def send_info(message):
    process_request()
    bot.reply_to(message, "This is a simple Telegram bot for lab3.")

# Define a message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    process_request()
    if message.text.startswith("danger"):
        event.Event('error', { 
            'user_id': message.from_user.id,
            'user_name':   message.from_user.username,
            'user_message': message.text})
        bot.reply_to(message, message.text+ " is eliminated!")
    else:
        bot.reply_to(message, message.text+ " lab3!")
# Start the bot
if __name__ == '__main__':
    start_http_server(9091)
    bot.polling()
