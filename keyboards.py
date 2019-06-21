import vk_api, json
from vk_api.keyboard import VkKeyboard

chat, menu, buy, buyback, partner, team = VkKeyboard(False), VkKeyboard(False), VkKeyboard(False), VkKeyboard(False), VkKeyboard(False), VkKeyboard(False)

carts = dict()

def back(state=''):
	back = VkKeyboard(False)
	if state == 'buy':
		back.add_button('Вернуться &#8617;', 'negative', '{"command":"back_buy"}')
	elif state == 'team':
		back.add_button('Вернуться &#8617;', 'negative', '{"command":"back_team"}')
	else:
		back.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return back.get_keyboard()

def chatboard(chat):
	chat.add_button('#news &#128240;', 'primary', '{"command":"news"}')
	chat.add_line()
	chat.add_button('Запрос VK Pay', 'primary', '{"command":"request"}')
	chat.add_line()
	chat.add_button('Баг-перезапуск', 'primary', '{"command":"restart"}')
	return chat.get_keyboard()

def menuboard(menu):
	menu.add_button('#idea &#128161;', 'positive', '{"command":"idea"}')
	menu.add_button('#partnership &#129309;', 'positive', '{"command":"partnership"}')
	menu.add_line()
	menu.add_button('#news &#128240;', 'positive', '{"command":"news"}')
	menu.add_button('#buy &#128717;', 'positive', '{"command":"buy"}')
	menu.add_line()
	menu.add_button('#team &#128101;', 'positive', '{"command":"team"}')
	menu.add_line()
	menu.add_button('Пожертвовать &#9749;', payload='{"command":"donat"}')
	menu.add_line()
	menu.add_button('Наши партнёры &#128226;', payload='{"command":"partners"}')
	return menu.get_keyboard()

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


def partnerboard(partner):
	partner.add_button('SAPOD — Подкаст из мира San Andreas &#127897;', 'primary', '{"command":"sapod"}')
	partner.add_line()
	partner.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return partner.get_keyboard()


def appboard(app_id, id, label):
	return json.dumps({"one_time":False, "buttons":[[{"action":{"type":"open_app", "app_id": app_id, "owner_id": id, "label": label}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

def locateboard():
	return json.dumps({"one_time":False, "buttons":[[{"action":{"type":"location", "payload":"{\"command\":\"sent_location\"}"}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back_buy\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

def itemboard(item_name):
	return json.dumps({"one_time":False, "buttons":[[{"color":"primary", "action":{"type":"text", "payload":'{"command":"add_' + item_name + '"}', "label":"Добавить в корзину &#10133;"}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back_buy\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

def payboard(hash):
	return json.dumps({"one_time":False, "buttons":[[{"action":{"type":"vkpay", "hash":hash}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

def donatboard(hash):
	return json.dumps({"one_time":False, "buttons":[[{"action":{"type":"vkpay", "hash":hash}}], [{"color": "primary", "action":{"type":"text", "payload":'{"command": "app_donat"}', "label":"Задонатить через приложение &#128242;"}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

chat = chatboard(chat)
menu = menuboard(menu)
buy = buyboard(buy)
partner = partnerboard(partner)
