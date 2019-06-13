import keyboards
from methods import *

payload = ''

try:
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
				msg(id, 'Привет, я PTBot, дворецкий команды PTCodding. \nНажмите на нужную Вам кнопку, чтобы команда нашла Вас и быстро ответила, а я не потерял Вас =) \n\n#idea — идеи и предложения \n#partnership — партнёрство, сотрудничество, спонсорство \n#support — администрация, помощь и вопросы \n#buy — магазин услуг и покупки', keyboards.menu)

			print('{} отправляет сообщение с текстом "{}"'.format(id, text))

			if id != 2000000002:
				if payload == '{"command":"idea"}':
					msg(id, "Предложите свою идею для PTCodding! Я pассмотрю её, и команда PTCodding обязательно отпишется Вам в этом диалоге. \nПостарайтесь соблюдать структуру: \n1. Лаконичное название, отражающее суть идеи \n2. Собственно идея, её развёртка \n3. Средства и блага, необходимые для развёртки Вашей идеи \n4. Расскажите, чем Ваша идея поможет сообществу \nНе забудьте, что необходимо уместить Вашу идею в рамках одного сообщения. Спасибо за Ваше содействие и помощь! \n\nС уважением, PTBot.", keyboards.back)
					payload = 'wait idea'

				elif payload == 'sending idea':
					attachs	= give_attachs(event.object.id)
					if attachs:
						print('{} отправляет идею и прикрепляет {}'.format(id, attachs))
					else:
						print('{} отправляет идею'.format(id))

					msg(2000000002, '#botidea \n[id{}|{} {}] предлагает идею: \n{}\n\nОтветить пользователю: https://vk.com/gim132868814?sel={}'.format(id ,name(id)['first_name'], name(id)['last_name'], text, id), attach=attachs)

					msg(id, 'Ваша идея будет доставлена команде PTCodding в аккуратном конвертике с Вашей печатью. Ожидайте ответа! &#8986;', keyboards.menu)

				elif payload == '{"command":"partnership"}':
					msg(id, 'Мы работаем над этим разделом...\nSoon...', keyboards.back)

				elif payload == '{"command":"support"}':
					msg(id, 'Мы работаем над этим разделом...\nSoon...', keyboards.back)

				elif payload == '{"command":"buy"}':
					msg(id, 'В разделе покупок Вы можете приобрести у нас виртуальные услуги и услуги на дом — рекламу, программирование и дизайн от моего начальства, звукозапись и ремонт Вашего ПК или Android-смартфона. &#128230; \nЕщё если Вы вдруг потеряетесь, то всегда можете заглянуть в привычную корзину и магазин от ВКонтакте))) &#128071;', keyboards.buy)

				elif payload == '{"command":"code"}':
					msg(id, 'Цена: от 200 руб. &#128181; \n\nМой начальник Павел вместе с командой создадут любую программу под Ваши цели и по Вашим требованиям. Ваши данные: описание функционала и ключевых целей и задач программы. \nХочу предупредить Вас: если Вам не понравилась программа, есть какие-то проблемы, ошибки, баги, то необходимо сразу же сообщить об этом. Любые недочёты исправляются одним нажатием клавиши. \nВ программе прописаны копирайты, с указанием авторства на сообщество PTCodding. Просьбы вернуть деньги после того, как Вы оплатили заказ, не принимаются. \nЦена может изменяться в зависимости от срока заказа и формата работы, указана минимальная цена! Также могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2055522 &#128072;', keyboards.itemboard('code'))

				elif payload == '{"command":"add_code"}':
					msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Code от Павла-code'))

				elif payload == '{"command":"delete_code"}':
					msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Code от Павла-code', False))

				elif payload == '{"command":"design"}':
					msg(id, 'Цена: от 200 руб. &#128181; \n\nДизайнер команды PTCodding создаст дизайн Вашему бренду по Вашим требованиям. Ваши данные: название бренда, для которой делается аватарка, дизайн \nХочу предупредить Вас: если Вам не понравился какой-то элемент дизайна, то ему необходимо сразу написать об этом. Любые недочёты исправляются одним нажатием клавиши. \nНа весь пак-дизайн, до оплаты заказа, будет нанесён водяной знак. Просьбы вернуть деньги после того, как Вы оплатили заказ и пак был передан без водяных знаков, не принимаются. \nЦена может изменяться в зависимости от срока заказа и техники выполнения, указана минимальная цена! Также могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2064351 &#128072;', keyboards.itemboard('design'))

				elif payload == '{"command":"add_design"}':
					msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Design от Богдана-design'))

				elif payload == '{"command":"delete_design"}':
					msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Design от Богдана-design', False))

				elif payload == '{"command":"record"}':
					msg(id, 'Мы работаем над этим разделом...\nSoon...', keyboards.itemboard('record'))

				elif payload == '{"command":"add_record"}':
					msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Звукозапись-record'))

				elif payload == '{"command":"delete_record"}':
					msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Звукозапись-record', False))

				elif payload == '{"command":"fix"}':
					msg(id, 'Мы работаем над этим разделом...\nSoon...', keyboards.itemboard('fix'))

				elif payload == '{"command":"add_fix"}':
					msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Ремонт ПК-fix'))

				elif payload == '{"command":"delete_fix"}':
					msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Ремонт ПК-fix', False))

				elif payload == '{"command":"cart"}':
					msg(id, 'Корзина товаров, которые Вы добавили к заказу. \nТовары удаляются из корзины при нажатии на них. Если Вы добавили в корзину какие-то товары, то будет доступна кнопка оформления заказа — нажмите на неё, и с Вами в этом чате свяжутся мои операторы, которые обсудят все условия и цены &#128222;', keyboards.cartboard(id))
						
				elif payload == '{"command":"cart_ui"}':
					msg(id, 'Загляните в привычный магазин, если мой Вам оказался не по душе: https://vk.com/market-132868814 &#128072;', keyboards.buyback)

				elif payload == '{"command":"order"}':
					msg(2000000002, 'Вас вызывают для оформления заказа. Пройдите, пожалуйста, по этой ссылке: https://vk.com/gim132868814?sel={}'.format(id))
				
				elif payload == '{"command":"back_buy"}':
					msg(id, 'Возвращаю Вас в меню товаров.', keyboards.buy)

				elif payload == '{"command":"news"}':
					msg(id, 'Мы работаем над этим разделом...\nSoon...', keyboards.back)

				elif payload == '{"command":"donat"}':
					msg(id, 'Я очень хочу кушать. Я голодный... &#128546; Дайте, пожалуйста, пару долларов, чтобы мне купили пончик. &#127849;', keyboards.payboard('action=transfer-to-group&group_id=132868814&aid=10'))
					raise Exception

				elif payload == '{"command":"partners"}':
					msg(id, 'Добро пожаловать в список партнёров команды PTCodding! Я от лица команды говорю жизни спасибо за то, что она свела нас с этими людьми, ведь без их поддержки и помощи у нас бы ничего не получилось бы! &#128079;', keyboards.partner)
				
				elif payload == '{"command":"sapod"}':
					msg(id, '@sapod (SAPOD) — первый и единственный подкаст из мира San Andreas. \n\nВедущий подкаста Стич часто появляется и в подкастах от PTCodding. Вместе с Павлом они обсуждают новости уходящего месяца в IT-кухне и жарко спорят, кто лучше: iOS или Android &#128521;\n\nСлушайте Стича в его подкасте SAPOD — vk.com/sapod &#128072;')

				elif payload == '{"command":"tryout"}':
					msg(id, 'TryOut — платформа для тестирования сервисов VK Mini Apps. \n\nНаш недавний партнёр @hit2hat (Степан Новожилов) делает так, чтобы обнаружение и исправление багов не было рутиной как для тестеров, так и для самих разработчиков. \nПавел и Степан давно работают вместе над разными проектами и постигают хакатоны. &#9994; \n\nЗаглядывайте в TryOut Степана — там PTCodding иногда проводит бета-тестирования своих проектов &#128071;', keyboards.appboard(id))
				
				elif payload == '{"command":"back"}':
					msg(id, 'Возвращаю Вас в главное меню. Напоминаю назначение кнопок: \n\n#idea — идеи и предложения \n#partnership — партнёрство, сотрудничество, спонсорство \n#support — администрация, помощь и вопросы \n#buy — магазин услуг и покупки', keyboards.menu)


		if event.type == VkBotEventType.MESSAGE_REPLY:
			text = event.object.text
			id = event.object.peer_id

			if id == 2000000002:
				if text.find('Заказ оформлен') != -1:
					msg(text.split()[-1], 'Спасибо Вам за оформление заказа. В дальнейшем мои операторы будут поддерживать с Вами периодическую связь по поводу заказа, а я всегда работаю здесь для Вас, в этом чате ', keyboards.menu)
					payload = ''

				elif text.find('Перезапуск') != -1:
					msg(text.split()[-1], 'Меня перезапустили. Не знаю, почему, но так надо, видимо.')

				elif text.find('Баг-перезапуск') != -1:
					msg(text.split()[-1], 'Добрый день! Видимо, наш PTBot где-то сломался, но сейчас уже всё хорошо. Приносим свои извинения, и перезапускаем его...')
					msg(text.split()[-1], 'Привет, это снова я, Ваш любимый PTBot! &#128075; Добро пожаловать в старое доброе меню — где какие кнопки, я думаю, Вы и сами знаете! &#128526;')

				elif text.find('Оплатить-') != -1:
					amount = text.split('-')[1]
					description = text.split()[3].split('"')[1]
					msg(id, 'Меня попросили запустить для Вас оплату «{}» на сумму в ₽{}. Подтвердите оплату...'.format(description, amount), keyboards.payboard('action=pay-to-group&amount={}&description={}&group_id=132868814&aid=10'.format(amount, description)))



		if event.type == VkBotEventType.VKPAY_TRANSACTION:
			id = event.object.from_id
			amount = event.object.amount * 1000
			if description in event.object and event.object.description:
				msg(2000000002, '{} перевёл ₽{} с комментарием «{}»'.format(name(id), amount, text))
			else:
				msg(2000000002, '{} пожертвовал ₽{}'.format(name(id), amount))

except Exception:
	print(keyboards.carts)
	msg(2000000002, 'Бот упал с лестницы самодержавия! @pavetranquil (Павел), помоги ему подняться — исправь баг &#128513;')