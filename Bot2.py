# Пишем 2-ю версию бота

# Импортируем Логгирование и преднастройки
import logging
import settings

# Поиск файлов по шаблону
from glob import glob

# Импортируем из модуля рандом, целочисленный рандом, выбор
from random import choice, randint

# Импортим эмодзи
from emoji import emojize

# Импортируем Updater из либы телеграм бота
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Логгирование сообщение в файл bot2.log, Уровень ИНФО и выше
logging.basicConfig(filename='bot2.log', level=logging.INFO)

# Создаем словарь с проксей-сервером
PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                  'password': settings.PROXY_PASSWORD}}


# Функция приветствия пользователя + emoji
def greet_user(update, context):
    print("Вызван /Start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Таки шалом Вам. {context.user_data['emoji']}")
    update.message.reply_text("Таки, давайте поговорим о кашерном Кацэ")


# Функция отзеркаливания сообщения
def talk_to_me(update, context):
    print('простое сообщение')
    text = update.message.text
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Ой,вэй {text} {context.user_data['emoji']}")


# Функция для работы со смайлами
def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


# Фунция делающая вычисления в игре
def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, Шекели ваши!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, Ничья!"
    else:
        message = f"Ваше число {user_number}, моё {bot_number}, \
давайте Ваши Шекели любезный!"
    return message


# Функция Игры в числа
def guess_number(update, context):
    print(context.args)
    if context.args:
        # Проверка: Целои ли число ?
        try:
            user_number = int(context.args[0])
            # Тут дальше будет игровая логика по генерированию механики игры.
            message = play_random_numbers(user_number)

        except (TypeError, ValueError):
            message = "Таки введите целое число, любезный"

    else:
        message = "Таки введите число, любезнейший"
    update.message.reply_text(message)


# Функция Отправки котиков
def send_cat_picture(update, context):
    print("вызываю котиков /cat")

    # Получаем список всех картинок
    cat_photos_list = glob('picture/cat*.jp*g')

    # Выбираем случайную картинку
    cat_pic_filename = choice(cat_photos_list)

    # Отправка картинки пользователю
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


# Функция для запуска ТГ бота
def main():
    # Создаем ТГ бота, и передаем Апишку для работы
    mybot2 = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    # Используем Диспетчер mybot2.dispatcher,
    # чтобы при наступлени события вызывалась наша функция.
    dp = mybot2.dispatcher

    # Добавляем обработчик, реагирующий на /start и вызывать функцию
    dp.add_handler(CommandHandler("start", greet_user))

    # Обработчик команды guess. Игра больше меньше.
    dp.add_handler(CommandHandler("guess", guess_number))

    # Обработчик команды cat. Картинки с котиками.
    dp.add_handler(CommandHandler("cat", send_cat_picture))

    # Добавляем обработчик реагирующий на текстовые сообшения
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # Запись "Бот стартовал", логгирование
    logging.info('Стартуем!!!!')

    # Отправляем ботв в ТГ за сообщениями
    mybot2.start_polling()

    # Запуск бота. Работает до принудительной осановки.
    mybot2.idle()


# Если этот файл вызвали python3 bot2.py
# то будет вызван main
# если нет, то main вызван не будет.
if __name__ == '__main__':
    main()
