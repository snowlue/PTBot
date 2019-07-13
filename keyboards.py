import vk_api, json
from vk_api.keyboard import VkKeyboard

chat, buy, buyback, partner, team, about, news = VkKeyboard(False), VkKeyboard(False), VkKeyboard(False), VkKeyboard(False), VkKeyboard(False), VkKeyboard(False), VkKeyboard(False)

carts = dict()

def back(state=''):
	back = VkKeyboard(False)
	if state:
		back.add_button('Вернуться &#8617;', 'negative', '{"command":"back_' + state + '"}')
	else:
		back.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return back.get_keyboard()

def start():
	start = VkKeyboard(False)
	start.add_button('Начать', payload='{"command":"start"}')
	return start.get_keyboard()

def chatboard(chat):
	chat.add_button('#news &#128240;', 'primary', '{"command":"news"}')
	chat.add_line()
	chat.add_button('Запрос VK Pay', 'primary', '{"command":"request"}')
	chat.add_line()
	chat.add_button('Баг-перезапуск', 'primary', '{"command":"restart"}')
	chat.add_line()
	chat.add_button('Вернуть к началу', 'primary', '{"command":"to_start"}')
	chat.add_line()
	chat.add_button('Отправить рассылку', 'primary', '{"command":"mailing"}')
	chat.add_line()
	chat.add_button('Вывести данные в консоль', 'primary', '{"command":"output"}')
	return chat.get_keyboard()

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
	menu = VkKeyboard(False)
	menu.add_button('#news &#128240;', 'positive', '{"command":"news"}')
	menu.add_line()
	menu.add_button('#idea &#128161;', 'positive', '{"command":"idea"}')
	menu.add_button('#partnership &#129309;', 'positive', '{"command":"partnership"}')
	menu.add_line()
	menu.add_button('#market &#128717;', 'positive', '{"command":"buy"}')
	menu.add_button('#team &#128101;', 'positive', '{"command":"team"}')
	menu.add_line()
	menu.add_button('Пожертвовать &#9749;', payload='{"command":"donate"}')
	menu.add_line()
	if mail:
		menu.add_button('Отписаться от рассылок &#10062;', payload='{"command":"unmail"}')
	else:
		menu.add_button('Подписаться на рассылки &#9989;', payload='{"command":"mail"}')
	return menu.get_keyboard()

def newsboard(news):
	news.add_button('Интернет', 'primary', '{"command":"news_internet"}')
	news.add_line()
	news.add_button('Гаджеты', 'primary', '{"command":"news_gadgets"}')
	news.add_line()
	news.add_button('Игры', 'primary', '{"command":"news_games"}')
	news.add_line()
	news.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return news.get_keyboard()

def listboard():
	board = VkKeyboard(False)
	board.add_button('1&#8419;', 'primary', '{"command":"1"}')
	board.add_button('2&#8419;', 'primary', '{"command":"2"}')
	board.add_button('3&#8419;', 'primary', '{"command":"3"}')
	board.add_button('4&#8419;', 'primary', '{"command":"4"}')
	board.add_line()
	board.add_button('5&#8419;', 'primary', '{"command":"5"}')
	board.add_button('6&#8419;', 'primary', '{"command":"6"}')
	board.add_button('7&#8419;', 'primary', '{"command":"7"}')
	board.add_button('8&#8419;', 'primary', '{"command":"8"}')
	board.add_line()
	board.add_button('Обновить &#128260;', payload='{"command":"refresh"}')
	board.add_line()
	board.add_button('Вернуться &#8617;', 'negative', '{"command":"back_news"}')
	return board.get_keyboard()

def teamboard(team):
	team.add_button('Задать вопрос команде&#10067;', payload='{"command":"question"}')
	team.add_line()
	team.add_button('О команде &#128142;', payload='{"command":"about"}')
	team.add_line()
	team.add_button('Наши партнёры &#128226;', payload='{"command":"partners"}')
	team.add_line()
	team.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return team.get_keyboard()

def buyboard(buy):
	buy.add_button('Создание чат-бота &#129302;', 'primary', '{"command":"code"}')
	buy.add_button('Создание дизайна &#128444;', 'primary', '{"command":"design"}')
	buy.add_line()
	buy.add_button('Звукозапись &#127897;', 'primary', '{"command":"record"}')
	buy.add_button('ПК и смартфоны &#128736;', 'primary', '{"command":"fix"}')
	buy.add_line()
	buy.add_button('Корзина &#128722;', payload='{"command":"cart"}')
	buy.add_line()
	buy.add_button('Наш магазин ВКонтакте &#128041;', payload='{"command":"cart_ui"}')
	buy.add_line()
	buy.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return buy.get_keyboard()

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
		board.add_button(it.split('.')[0]+' &#10134;', payload='{"command":"delete_' + it.split('.')[1] + '"}')
		board.add_line()
	if cart:
		board.add_button('Оформить заказ &#128222;', 'positive', '{"command":"order"}')
		board.add_line()

	board.add_button('Вернуться &#8617;', 'negative', '{"command":"back_buy"}')
	return board.get_keyboard()

def aboutboard(about):
	about.add_button('Павел Овчинников 👨🏽‍💻', 'primary', '{"command":"Pavel"}')
	about.add_line()
	about.add_button('Богдан Гусев 👨🏼‍💻', 'primary', '{"command":"Bogdan"}')
	about.add_line()
	about.add_button('Ксения Хубутия 👩🏻‍💼', 'primary', '{"command":"Kseno"}')
	about.add_line()
	about.add_button('Вернуться &#8617;', 'negative', '{"command":"back_team"}')
	return about.get_keyboard()


def partnerboard(partner):
	partner.add_button('SAPOD — подкаст из мира San Andreas&#127897;', 'primary', '{"command":"sapod"}')
	partner.add_line()
	partner.add_button('keksik.media — издание о соц.сетях и IT&#128240;', 'primary', '{"command":"keksik"}')
	partner.add_line()
	partner.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return partner.get_keyboard()

def itemboard(item_name):
	return json.dumps({"one_time":False, "buttons":[[{"color":"primary", "action":{"type":"text", "payload":'{"command":"add_' + item_name + '"}', "label":"Добавить в корзину &#10133;"}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back_buy\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

def payboard(hash):
	return json.dumps({"one_time":False, "buttons":[[{"action":{"type":"vkpay", "hash":hash}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

def donateboard(hash, app_id, id, label):
	return json.dumps({"one_time":False, "buttons":[[{"action":{"type":"vkpay", "hash":hash}}], [{"action":{"type":"open_app", "app_id": app_id, "owner_id": id, "label": label}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

def emptyboard():
	return json.dumps({"one_time":True, "buttons":[]})


chat = chatboard(chat)
news = newsboard(news)
team = teamboard(team)
about = aboutboard(about)
buy = buyboard(buy)
partner = partnerboard(partner)

print('keyboards.py started!')
