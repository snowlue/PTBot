import vk_api
import json
from vk_api.keyboard import VkKeyboard


carts = {}


def back(state=''):
    board = VkKeyboard(False)
    if state:
        board.add_button('Вернуться &#8617;', 'negative', '{"command":"back_' + state + '"}')
    else:
        board.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
    return board.get_keyboard()


def cancel():
    board = VkKeyboard(True)
    board.add_button('Отменить ❎', 'negative', '{"command":"cancel"}')
    return board.get_keyboard()


def start():
    board = VkKeyboard(False)
    board.add_button('Начать', payload='{"command":"start"}')
    return board.get_keyboard()


def conversation(mail):
    board = VkKeyboard(False)
    board.add_button('Новости &#128240;', 'primary', '{"command":"news"}')
    board.add_line()
    board.add_button('Пожертвовать &#9749;', 'primary', '{"command":"donate"}')
    board.add_line()
    if mail:
        board.add_button('Отписаться от рассылок &#10062;', payload='{"command":"unmail"}')
    else:
        board.add_button('Подписаться на рассылки &#9989;', payload='{"command":"mail"}')
    return board.get_keyboard()


def menu(mail):


def newsboard(news):
	news.add_button('Интернет', 'primary', '{"command":"news_internet"}')
	news.add_line()
	news.add_button('Гаджеты', 'primary', '{"command":"news_gadgets"}')
	news.add_line()
	news.add_button('Игры', 'primary', '{"command":"news_games"}')
	news.add_line()
	news.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return news.get_keyboard()
    board = VkKeyboard(False)
    board.add_button('#news &#128240;', 'positive', '{"command":"news"}')
    board.add_line()
    board.add_button('#partnership &#129309;', 'positive', '{"command":"partnership"}')
    board.add_line()
    board.add_button('#market &#128717;', 'positive', '{"command":"buy"}')
    board.add_button('#team &#128101;', 'positive', '{"command":"team"}')
    board.add_line()
    board.add_button('Пожертвовать &#9749;', payload='{"command":"donate"}')
    board.add_line()
    if mail:
        board.add_button('Отписаться от рассылок &#10062;', payload='{"command":"unmail"}')
    else:
        board.add_button('Подписаться на рассылки &#9989;', payload='{"command":"mail"}')
    return board.get_keyboard()


def listboard():
	board = VkKeyboard(False)
	board.add_button('1&#8419;', payload='{"command":"1"}')
	board.add_button('2&#8419;', payload='{"command":"2"}')
	board.add_button('3&#8419;', payload='{"command":"3"}')
	board.add_button('4&#8419;', payload='{"command":"4"}')
	board.add_line()
	board.add_button('5&#8419;', payload='{"command":"5"}')
	board.add_button('6&#8419;', payload='{"command":"6"}')
	board.add_button('7&#8419;', payload='{"command":"7"}')
	board.add_button('8&#8419;', payload='{"command":"8"}')
	board.add_line()
	board.add_button('Вернуться &#8617;', 'negative', '{"command":"back_news"}')
	return board.get_keyboard()


def teamboard():
    board = VkKeyboard(False)
    board.add_button('Задать вопрос команде&#10067;', payload='{"command":"question"}')
    board.add_line()
    board.add_button('О команде &#128142;', payload='{"command":"about"}')
    board.add_line()
    # board.add_button('Наши партнёры &#128226;', payload='{"command":"partners"}')
    # board.add_line()
    board.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
    return board.get_keyboard()


def buyboard():
    board = VkKeyboard(False)
    board.add_button('Создание чат-бота &#129302;', 'primary', '{"command":"code"}')
    board.add_button('Создание дизайна &#128444;', 'primary', '{"command":"design"}')
    board.add_line()
    board.add_button('Звукозапись &#127897;', 'primary', '{"command":"record"}')
    board.add_button('ПК и смартфоны &#128736;', 'primary', '{"command":"fix"}')
    board.add_line()
    board.add_button('Корзина &#128722;', payload='{"command":"cart"}')
    board.add_line()
    board.add_button('Наш магазин ВКонтакте &#128041;', payload='{"command":"cart_ui"}')
    board.add_line()
    board.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
    return board.get_keyboard()


def cartboard(id, item=''):
    if id not in carts:
        carts[id] = []

    board = VkKeyboard(False)
    cart = carts[id]

    if item:
        if item not in cart:
            cart.append(item)
        elif item in cart:
            cart.remove(item)

    for it in cart:
        board.add_button(it.split('.')[0]+' &#10134;',
                         payload='{"command":"delete_' + it.split('.')[1] + '"}')
        board.add_line()
    if cart:
        board.add_button('Оформить заказ &#128222;', 'positive', '{"command":"order"}')
        board.add_line()

    board.add_button('Вернуться &#8617;', 'negative', '{"command":"back_buy"}')
    return board.get_keyboard()


def aboutboard():
    board = VkKeyboard(False)
    board.add_button('Павел Овчинников 👨🏽‍💻', 'primary', '{"command":"Pavel"}')
    board.add_line()
    board.add_button('Богдан Гусев 👨🏼‍💻', 'primary', '{"command":"Bogdan"}')
    board.add_line()
    board.add_button('Дмитрий Якунин 👨🏼‍💼', 'primary', '{"command":"Dima"}')
    board.add_line()
    board.add_button('Вернуться &#8617;', 'negative', '{"command":"back_team"}')
    return board.get_keyboard()


def partnerboard():
    # board = VkKeyboard(False)
    # board.add_button('SAPOD — подкаст из мира San Andreas&#127897;', 'primary', '{"command":"sapod"}')
    # board.add_line()
    # board.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
    # return board.get_keyboard()
    pass


def itemboard(item_name):
    board = VkKeyboard(False, True)
    board.add_button('Добавить в корзину &#10133;', 'primary', '{"command":"add_%s"}' % item_name)
    return board.get_keyboard()


def payboard(hash):
    board = VkKeyboard(False, True)
    board.add_vkpay_button(hash)
    return board.get_keyboard()


def emptyboard():
    return VkKeyboard.get_empty_keyboard()


news = newsboard()
team = teamboard()
about = aboutboard()
buy = buyboard()
# partner = partnerboard(partner)
print('keyboards.py started!')
