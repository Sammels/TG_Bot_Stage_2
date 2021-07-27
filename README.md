Расширяем функционал стандартного бота, которого наваял ранее.
Стадия 2
Что-то про виртуальное окружение.

# Виртуальное окружение
Обязательная часть во всех проектах

python3 -m venv venv

Активация виртуального окружения

source /venv/bin/activate

1. Добавить venv/ в .gitignore
2. Зафиксируем зависимости pip3 freeze > requirements.txt
--------------------------------------
Пробуем добавить возможность игры бота.
1. Передаем целое число типа /guess 10
2. Бот генерирует случайное число и сравнивает с тем, которое мы передали.
3. Чьё число больше, тот и выиграл.

# CommandHandler всегда выше чем MessageHandler
Иначе команды будут съедены.

1. Добавляем
dp.add_handler(CommandHandler("guess", guess_number))

2. Делаем Заготовку функции которая будет принимать данные от пользователя

def guess_number(update, context):
    if context.args:
        message = "Вы ввели число"
    else:
        message = "Введите число"
    update.message.reply_text(message)

3. Добавляем исключения. На всякий случай.
--------------------------------

Добавляем генерацию случайного числа из промежутка на 10 меньше и на 10 больше

Импортируем модуль random.
для целочисленного вывода используем функцию randint.

from random inport randint
--------------------------------
Создаем функцию, которая делает вычисления.

/code def play_random_numbers(user_number):
    bot_number = randint(user_number-150, user_number+200)
    if user_number > bot_number:
        message = f"Вы загадали {user_number}, а мой сверхразум {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Вы загадали {user_number}, а мой сверхразум {bot_number}, ничья!"
    else:
        message = f"Вы загадали {user_number}, а мой сверхразум {bot_number}, Ви таки продули свои шекели!"
    return message
/code
<h3> Делать включение в функцию, было плохой идеей</h3>


----------------
Отправка изображения пользователю

1. Создаем папку с изображениями picture файлы с расширением .jpg или .jpeg
2. Ищем в папке picture файлы с расширением .jpg, .jpeg
3. Выбираем случайную картинку и отсылаем пользователю.

'''dp.add_handler(CommandHandler("cat", send_cat_picture))'''

Для поиска файлов по шаблону используем модуль glob из стандартной либы.
Используем * который означает тут может быть что угодно.

'''from glob import glob
print(glob('picture/cat*.jpg'))

print(glob('picture/cat*.jp*g'))
'''

Для выбора случайного элемента  списка мы будем использовать функцию choice из random

Напишем функцию, которая отсылает картинку.
1. Получаем имя случайного файла с картинкой
2. берем его id чата с текущим пользователем из update.effective_chat.id и
при помощи update.bot.send_photo отправляем фотку.

'''
def send_cat_picture(update, context):
    cat_photo_list = glob('picture/cat*.jp*g')
    cat_pic_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))
'''
----------------------------
Добавление Emoji
Установка либы,
Добавление в requirements emoji
pip3 install emoji
pip3 freeze > requirements.txt


Добавим в settings набор смайликов
USER_EMOJI = [':smiley_cat:',':smiling_imp:', ':panda_face:',':dog:']

Модификация функции greet_user
Команда /start добавляет к сообщению случайный смайлик.
Выберем случайный смайлик choice а с помощью emojize переведем в картинку

def greet_user(update, context):
    smile = get_smile()
    update.message.reply_text(f"Шалом праавославный {smile}!")

Создадим отдельную функцию для смайликов

def get_smile():
    smile = choice(settings.USER_EMOJI)
    return emojize(smile, use_aliases=True)

---------------------------
Запоминание пользовательских данных

Для запоминания будем использовать context.user_data
Это словарь. Если добавим ключ с даными  эти данные будут доступны для пользователя

Модифицируем функцию get_smile().
Она будет получать аргумент context.user_data. Будем проверять есть ли там ключ
'emoji' - если есть, то отдавать сохраненную  там emoji. Если нет, будем создавать.

Сделаем чтобы пользователю присваивался случайный смайлик и запоминался.

Модификация get_smile(user_data)

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']
