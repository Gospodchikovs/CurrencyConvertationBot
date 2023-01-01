import telebot
from extensions import APIException, PriceRequestor
from config import TOKEN_BOT

bot = telebot.TeleBot(TOKEN_BOT)  # Бот доступен по ссылке https://t.me/gospodchikovbot
requestor = PriceRequestor()

пше
@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    bot.reply_to(message, 'Формат строки для конвертации валюты:\n' +
                 '<имя валюты, цену которой вы хоите узнать> <имя валюты, в которой надо узнать цену первой валюты>' +
                 ' <количество первой валюты>\n' +
                 'Команды бота для конвертации валюты:\n' +
                 '/values - список доступных для конвертации валют\n' +
                 '/help - подсказка по командам\n')


@bot.message_handler(commands=['values'])
def list_currency(message):
    values = 'Доступные для конвертации валюты:\n'
    for item in requestor.get_values():
        values += item + '\n'
    bot.reply_to(message, values)


@bot.message_handler(content_types=['text'])
def convert_currency(message):
    req = message.text.split()
    try:
        if len(req) != 3:
            raise APIException('В запросе должно быть три параметра!')
        answer = requestor.get_price(req[0], req[1], req[2])
    except APIException as error:
        bot.reply_to(message, f'Ошибка при вводе команды. {error}')
    except Exception as error:
        bot.reply_to(message, f'Не удается выполнить команду. {error}')
    else:
        bot.reply_to(message, f'Стоимость {req[2]} ед. валюты {req[0]} составляет {answer:.2f} ед. в валюте {req[1]}.')


bot.polling(none_stop=True)
