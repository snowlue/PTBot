import vk_api, json
from vk_api.keyboard import VkKeyboard

back, menu, buy, buyback = VkKeyboard(True), VkKeyboard(True), VkKeyboard(True), VkKeyboard(True)

def backboard(back):
	back.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return back.get_keyboard()

def menuboard(menu):
	menu.add_button('#idea &#128161;', 'positive', '{"command":"idea"}')
	menu.add_button('#partnership &#129309;', 'positive', '{"command":"partnership"}')
	menu.add_line()
	menu.add_button('#support &#10067;', 'positive', '{"command":"support"}')
	menu.add_button('#buy &#128717;', 'positive', '{"command":"buy"}')
	menu.add_line()
	menu.add_button('Пожертвовать &#9749;', payload='{"command":"donat"}')
	menu.add_line()
	menu.add_button('Наши партнёры &#128101;', payload='{"command":"partners"}')
	return menu.get_keyboard()

def buyboard(buy):
	buy.add_button('Реклама &#128640;', 'primary', '{"command":"pr"}')
	buy.add_button('Code от PaveTranquil &#128104;', 'primary', '{"command":"code"}')
	buy.add_button('Design от BogToGus &#128142;', 'primary', '{"command":"design"}')
	buy.add_line()
	buy.add_button('Звукозапись &#127911;', 'primary', '{"command":"record"}')
	buy.add_button('Ремонт ПК &#128187;', 'primary', '{"command":"fix"}')
	buy.add_line()
	buy.add_button('Добавить к заказу своё местоположение &#127757;', payload='{"command":"location"}')
	buy.add_line()
	buy.add_button('Перейти в корзину &#128722;', payload='{"command":"basket"}')
	buy.add_line()
	buy.add_button('Вернуться &#8617;', 'negative', '{"command":"back"}')
	return buy.get_keyboard()

def buybackboard(buyback):
	buyback.add_button('Вернуться &#8617;', 'negative', '{"command":"back_buy"}')
	return buyback.get_keyboard()

def partnerboard(id):
	return json.dumps({"one_time":False, "buttons":[[{"color": "primary", "action":{"type":"text", "payload":"{\"command\":\"sapod\"}", "label":"SAPOD - Подкаст из мира San Andreas &#127897;"}}], [{"action":{"type":"open_app", "app_id":7007699, "owner_id": id, "label":"TryOut — тестирование VK Apps"}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back\"}","label":"Вернуться &#8617;"}}]]})

def locateboard():
	return json.dumps({"one_time":True, "buttons":[[{"action":{"type":"location", "payload":"{\"command\":\"sent_location\"}"}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back_buy\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

def payboard(hash):
	return json.dumps({"one_time":True, "buttons":[[{"action":{"type":"vkpay", "hash":hash}}], [{"color":"negative","action":{"type":"text","payload":"{\"command\":\"back\"}","label":"Вернуться &#8617;"}}]]}, ensure_ascii=False)

back = backboard(back)
menu = menuboard(menu)
buy = buyboard(buy)
buyback = buybackboard(buyback)
