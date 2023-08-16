import logging
from telegram.ext import Updater, CommandHandler
import requests

# Установка уровня логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Функция для обработки команды /start
def start(update, context):
    update.message.reply_text('Привет! Я бот, который обновляет информацию о ценах на криптовалюту каждые 24 часа.')

# Функция для обновления информации о ценах на криптовалюту
def update_prices(context):
    # Получение данных о ценах с помощью API CoinGecko
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd')

    if response.status_code == 200:
        data = response.json()
        bitcoin_price = data['bitcoin']['usd']
        ethereum_price = data['ethereum']['usd']
        message = f'Цена на Bitcoin: ${bitcoin_price}\nЦена на Ethereum: ${ethereum_price}'

        # Отправка сообщения с обновленной информацией
        context.bot.send_message(chat_id=context.job.context, text=message)
    else:
        logger.error('Ошибка при получении данных о ценах на криптовалюту')

def main():
    # Токен вашего бота
    token = 'YOUR_BOT_TOKEN'

    # Создание экземпляра Updater и передача токена
    updater = Updater(token, use_context=True)

    # Получение диспетчера для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрация обработчика команды /start
    dp.add_handler(CommandHandler("start", start))

    # Регистрация задачи для обновления цен каждые 24 часа
    job_queue = updater.job_queue
    job_queue.run_repeating(update_prices, interval=86400, first=0, context=chat_id)

    # Запуск бота
    updater.start_polling()

    # Остановка бота при нажатии Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
