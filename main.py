import keyboards
from methods import *

payload = ''

for event in longpoll.listen():

	print('\n\nЛовлю события... Поймал {}'.format(event.type))
	if event.type == VkBotEventType.MESSAGE_NEW:
		id = event.object.peer_id
		text = event.object.text
		
		if payload == 'wait idea' and text != 'Вернуться ↩':
			payload = 'sending idea'
		else:
			payload = event.object.payload

		if payload == '{"command":"start"}': 
			msg(id, 'Привет, я PTBot, дворецкий команды PTCodding. \nНажмите на нужную Вам кнопку, чтобы команда нашла Вас и быстро ответила, а я не потерял Вас =) \n\n#idea — идеи и предложения \n#partnership — партнёрство, сотрудничество, спонсорство \n#support — администрация, помощь и вопросы \n#buy — магазин услуг и покупки', board=keyboards.menu)

		print('{} отправляет сообщение с текстом "{}"'.format(id, text))

		if id != 2000000002:
			if payload == '{"command":"idea"}':
				msg(id, "Предложите свою идею для PTCodding! Я pассмотрю её, и команда PTCodding обязательно отпишется Вам в этом диалоге. \nПостарайтесь соблюдать структуру: \n1. Лаконичное название, отражающее суть идеи \n2. Собственно идея, её развёртка \n3. Средства и блага, необходимые для развёртки Вашей идеи \n4. Расскажите, чем Ваша идея поможет сообществу \nНе забудьте, что необходимо уместить Вашу идею в рамках одного сообщения. Спасибо за Ваше содействие и помощь! \n\nС уважением, PTBot.", board=keyboards.back)
				payload = 'wait idea'

			elif payload == 'sending idea':
				attachs	= give_attachs(event.object.id)
				if attachs[0] != '':
					print('{} отправляет идею и прикрепляет {}'.format(id, attachs[0]))
				else:
					print('{} отправляет идею'.format(id))

				if attachs[1] == 0:
					msg(2000000002, '#botidea \n[id{}|{} {}] предлагает идею: \n{}\n\nОтветить пользователю: https://vk.com/gim132868814?sel={}'.format(id ,name(id)[0]['first_name'], name(id)[0]['last_name'], text, id), attach=attachs[0])
				else:
					msg(2000000002, '#botidea \n[id{}|{} {}] предлагает идею, отправляя стикер. \nОтветить пользователю: https://vk.com/gim132868814?sel={}'.format(id ,name(id)[0]['first_name'], name(id)[0]['last_name'], id), attach=attachs[0])
					msg(2000000002, stick=attachs[1])

				msg(id, 'Ваша идея будет доставлена команде PTCodding в аккуратном конвертике с Вашей печатью. Ожидайте ответа! &#8986;', board=keyboards.menu)

			elif payload == '{"command":"partnership"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', board=keyboards.back)

			elif payload == '{"command":"support"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', board=keyboards.back)

			elif payload == '{"command":"buy"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', board=keyboards.buy)

			elif payload == '{"command":"pr"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', board=keyboards.buyback)

			elif payload == '{"command":"code"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', board=keyboards.buyback)

			elif payload == '{"command":"design"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', board=keyboards.buyback)

			elif payload == '{"command":"record"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', board=keyboards.buyback)

			elif payload == '{"command":"fix"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', board=keyboards.buyback)

			elif payload == '{"command":"location"}':
				msg(id, 'У вас есть возможность отправить Ваше местоположение сразу для заказа звукозаписи или ремонта ПК.', board=keyboards.locateboard())

			elif payload == '{"command":"sent_location"}':
				msg(id, 'Спасибо за отправку Вашего местоположения! Команда PTCodding обязательно учтёт это при оформлении заказа! &#128521;', board=keyboards.buy)
					
			elif payload == '{"command":"basket"}':
				msg(id, 'Ваша корзина расположена по этой ссылке: https://vk.com/ptcodding?w=app6468267_-132868814', board=keyboards.buyback)
			
			elif payload == '{"command":"back_buy"}':
				msg(id, 'Возвращаю Вас в меню товаров. Напоминаю назначение кнопок: \n\n', board=keyboards.buy)

			elif payload == '{"command":"donat"}':
				msg(id, 'Я очень хочу кушать. Я голодный... &#128546; Дайте, пожалуйста, пару долларов, чтобы мне купили пончик. &#127849;', board=keyboards.payboard('action=transfer-to-group&group_id=132868814&aid=10'))

			elif payload == '{"command":"partners"}':
				msg(id, 'Добро пожаловать в список партнёров команды PTCodding! Я от лица команды говорю жизни спасибо за то, что она свела нас с этими людьми, ведь без их поддержки и помощи у нас бы ничего не получилось бы! &#128079;', board=keyboards.partnerboard(id))
			
			elif payload == '{"command":"sapod"}':
				msg(id, '@sapod (SAPOD) — первый и единственный подкаст из мира San Andreas. \n\nВедущий подкаста Стич часто появляется и в подкастах от PTCodding. Вместе с Павлом они обсуждают новости уходящего месяца в IT-кухне и жарко спорят, кто лучше: iOS или Android &#128521;\n\nСлушайте Стича в его подкасте SAPOD — vk.com/sapod &#128072;')

			elif payload == '{"command":"back"}':
				msg(id, 'Возвращаю Вас в главное меню. Напоминаю назначение кнопок: \n\n#idea — идеи и предложения \n#partnership — партнёрство, сотрудничество, спонсорство \n#support — администрация, помощь и вопросы \n#buy — магазин услуг и покупки', board=keyboards.menu)


	if event.type == VkBotEventType.MESSAGE_REPLY:
		text = event.object.text
		id = event.object.peer_id
		if event.object.text.find('/restartptbot0921') != -1:
			msg(id, 'Перезапуск клавиатуры...', board=keyboards.menu)
			payload = ''


	if event.type == VkBotEventType.VKPAY_TRANSACTION:
		id = event.object.from_id
		amount = event.object.amount * 1000
		if description in event.object and event.object.description:
			msg(2000000002, '{} перевёл ₽{} с комментарием «{}»'.format(name(id), amount, text))
		else:
			msg(2000000002, '{} пожертвовал ₽{}'.format(name(id), amount))