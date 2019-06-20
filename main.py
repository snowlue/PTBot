import keyboards, urllib.parse, traceback
from methods import *

payload, state, state_chat = '', '', ''

# try:
for event in longpoll.listen():

	print('\nЛовлю события... Поймал {}'.format(event.type))
	if event.type == VkBotEventType.MESSAGE_NEW:
		id = event.object.peer_id
		text = event.object.text
		msg_id = event.object.id
		payload = event.object.payload
		
		if id == 2000000002:
			if state_chat == 'wait request_id' and text.split()[1] != 'Вернуться ↩':
				state_chat = 'sending request_id'
			elif state_chat == 'wait amount' and text.split()[1] != 'Вернуться ↩':
				state_chat = 'sending amount'
			elif state_chat == 'wait description' and text.split()[1] != 'Вернуться ↩':
				state_chat = 'sending description'
			elif state_chat == 'wait restart_id' and ' '.join(text.split()[1:]) != 'Вернуться ↩':
				state_chat = 'sending restart_id'
		if id < 2000000000:
			if state == 'wait idea' and text != 'Вернуться ↩':
				state = 'sending idea'

		if id == 2000000002 and (payload == '{"command":"start"}' or text.lower().find('начать') != -1):
			msg(id, 'Привет, команда PTCodding! Рад вас видеть! Вижу, что этот чат — чат моих создателей. Включаю дополнительные функции &#128522; \n\n#news — последние новости из сферы IT \nЗапрос VK Pay — запрос средств с указанием amount, description и id \nБаг-перезапуск — перезапуск бота по id с сообщением о баге', keyboards.chat)
		elif id < 2000000000 and payload == '{"command":"start"}': 
			msg(id, 'Привет, я PTBot, дворецкий команды PTCodding. \nНажмите на нужную Вам кнопку, чтобы команда нашла Вас и быстро ответила, а я не потерял Вас &#128522; \n\n#idea — идеи и предложения \n#partnership — партнёрство, сотрудничество, спонсорство \n#support — администрация, помощь и вопросы \n#buy — магазин услуг и покупки \n#news — последние новости из сферы IT', keyboards.menu)

		print('{} отправляет сообщение с текстом "{}"'.format(id, text))

		if id in [223166352, 165504240, 186823615, 484735371, 2000000002]:
			if payload == '{"command":"idea"}':
				msg(id, "Предложите свою идею для PTCodding! Я pассмотрю её, и команда PTCodding обязательно отпишется Вам в этом диалоге. \nПостарайтесь соблюдать структуру: \n1. Лаконичное название, отражающее суть идеи \n2. Собственно идея, её развёртка \n3. Средства и блага, необходимые для развёртки Вашей идеи \n4. Расскажите, чем Ваша идея поможет сообществу \nНе забудьте, что необходимо уместить Вашу идею в рамках одного сообщения. Спасибо за Ваше содействие и помощь! \n\nС уважением, PTBot.", keyboards.back)
				state = 'wait idea'

			elif state == 'sending idea' and id != 2000000002:
				print('{} отправляет идею'.format(id))

				msg(2000000002, '#botidea \n[id{0}|{1} {2}] предлагает идею.\n\nОтветить пользователю: https://vk.com/gim132868814?sel={0}'.format(id, name(id)['first_name'], name(id)['last_name']), forward=str(msg_id))

				msg(id, 'Ваша идея будет доставлена команде PTCodding в аккуратном конвертике с Вашей печатью. Ожидайте ответа! &#8986;', keyboards.menu)

			elif payload == '{"command":"partnership"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', keyboards.back)

			elif payload == '{"command":"support"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', keyboards.back)

			elif payload == '{"command":"buy"}':
				msg(id, 'В разделе покупок Вы можете приобрести у нас виртуальные услуги и услуги на дом — рекламу, программирование и дизайн от моего начальства, звукозапись и ремонт Вашего ПК или Android-смартфона. &#128230; \nЕщё если Вы вдруг потеряетесь, то всегда можете заглянуть в привычную корзину и магазин от ВКонтакте))) &#128071;', keyboards.buy)

			elif payload == '{"command":"code"}':
				msg(id, 'Цена: от 200 руб. &#128181; \n\nМоё начальство напишет чат-бота ВКонтакте или в Telegram под Ваши цели и по Вашим требованиям. Ваши данные: описание функционала и ключевых целей и задач чат-бота, сгенерированный longpoll-токен. \nХочу предупредить Вас: если Вам не понравился чат-бот, есть какие-то проблемы, ошибки, баги, то необходимо сразу же сообщить об этом. Любые недочёты исправляются одним нажатием клавиши. \nВ чат-боте прописан его создатель, с указанием авторства на сообщество PTCodding. Просьбы вернуть деньги после того, как Вы установили чат-бота в своё сообщество, не принимаются. \nЦена может изменяться в зависимости от срока заказа, указана минимальная цена! Также могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2055522 &#128072;', keyboards.itemboard('code'))
			elif payload == '{"command":"add_code"}':
				msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Создание чат-бота—code'))
			elif payload == '{"command":"delete_code"}':
				msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Создание чат-бота—code', False))

			elif payload == '{"command":"design"}':
				msg(id, 'Цена: от 200 руб. &#128181; \n\nМоё начальство создаст дизайн Вашему бренду по Вашим требованиям. Ваши данные: название бренда, для которого делается дизайн, стиль исполнения. \nХочу предупредить Вас: если Вам не понравился какой-то элемент дизайна, то ему необходимо сразу написать об этом. Любые недочёты исправляются одним нажатием клавиши. \nНа весь пак дизайна, до оплаты заказа, будет нанесён водяной знак. Просьбы вернуть деньги после того, как Вы оплатили заказ и пак был передан без водяных знаков, не принимаются. \nЦена может изменяться в зависимости от срока заказа и техники выполнения, указана минимальная цена! Также могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2064351 &#128072;', keyboards.itemboard('design'))
			elif payload == '{"command":"add_design"}':
				msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Создание дизайна—design'))
			elif payload == '{"command":"delete_design"}':
				msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Создание дизайна—design', False))

			elif payload == '{"command":"record"}':
				msg(id, 'Цена: от 750 руб. &#128181; \n\nМоё начальство запишет Ваш голос на своей домашней студии, обработает звук и отправит исходники в mp3, wav или другом формате на флешку, ВКонтакте или в облако. \nПри заказе дополнительно сведения, мастеринга или же при полноценной запись под ключ цена оговаривается при оформлении заказа. \nХочу предупредить Вас: на весь звуковой файл накладывается демо-фраза до оплаты заказа. Просьбы вернуть деньги после того, как Вы оплатили заказ и файл был передан без демо-фразы, не принимаются. \nЦена может изменяться в зависимости от срока заказа и дополнительных услуг, указана минимальная цена! Для клиентов могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2561900 &#128072;', keyboards.itemboard('record'))
			elif payload == '{"command":"add_record"}':
				msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Звукозапись—record'))
			elif payload == '{"command":"delete_record"}':
				msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Звукозапись—record', False))

			elif payload == '{"command":"fix"}':
				msg(id, 'Цена: от 500 руб. &#128181; \n\nМоё начальство также работает с компьютерами и смартфонами: исправляет мелкие неполадки в работе, устанавливает лицензированный Microsoft Office или иное ПО, устанавливают активированную Windows, перепрошивают Android-смартфоны. \nХочу предупредить Вас: проверяйте работоспособность ПО, ПК или смартфона в целом сразу перед оплатой заказа. PTCodding даёт бесплатную гарантию — 1 месяц. Далее гарантия продлевается платно. \nЦена может изменяться в зависимости от срока заказа, указана минимальная цена! Для клиентов могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2561901 &#128072;', keyboards.itemboard('fix'))
			elif payload == '{"command":"add_fix"}':
				msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'ПК и смартфоны—fix'))
			elif payload == '{"command":"delete_fix"}':
				msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'ПК и смартфоны—fix', False))

			elif payload == '{"command":"cart"}':
				msg(id, 'Корзина товаров, которые Вы добавили к заказу. \nТовары удаляются из корзины при нажатии на них. Если Вы добавили в корзину какие-то товары, то будет доступна кнопка оформления заказа — нажмите на неё, и с Вами в этом чате свяжутся мои операторы, которые обсудят все условия и цены &#128222;', keyboards.cartboard(id))
					
			elif payload == '{"command":"cart_ui"}':
				msg(id, 'Загляните в привычный магазин, если мой Вам оказался не по душе: https://vk.com/market-132868814 &#128072;', keyboards.buyback)

			elif payload == '{"command":"order"}':
				msg(2000000002, 'Вас вызывают для оформления заказа. Пройдите, пожалуйста, по этой ссылке: https://vk.com/gim132868814?sel={}'.format(id))
				msg(id, 'Ожидайте... Скоро мои операторы свяжутся с Вами для уточнения деталей и оплаты заказа! &#8986;')
			
			elif payload == '{"command":"back_buy"}':
				msg(id, 'Возвращаю Вас в меню товаров.', keyboards.buy)

			elif payload == '{"command":"news"}':
				msg(id, 'Мы работаем над этим разделом...\nSoon...', keyboards.back)

			elif payload == '{"command":"donat"}':
				msg(id, 'Я очень хочу кушать. Я голодный... &#128546; Дайте, пожалуйста, пару долларов, чтобы мне купили пончик. &#127849;', keyboards.donatboard('action=transfer-to-group&group_id=132868814&aid=10'))

			elif payload == '{"command":"app_donat"}':
				msg(id, 'Если хотите поддержать наш проект, то лучше сделайте пожертвование через приложение — так Вы не просто поддержите нас, но и продвинете проект! &#128200;', keyboards.appboard(6887721, -132868814, 'Пончик — наши донаты &#127849;'))
			
			elif payload == '{"command":"partners"}':
				msg(id, 'Добро пожаловать в список партнёров команды PTCodding! Благодаря этим людям в PTCodding очень многое изменяется. Я как чат-бот сообщества наблюдаю за всем этим со стороны — PTCodding растёт на глазах! &#128079;', keyboards.partner)
			
			elif payload == '{"command":"sapod"}':
				msg(id, '@sapod (SAPOD) — первый и единственный подкаст из мира San Andreas. \n\nВедущий подкаста Стич часто появляется и в подкастах от PTCodding. Вместе с Павлом они обсуждают новости уходящего месяца в IT-кухне и жарко спорят, кто лучше: iOS или Android &#128521;\n\nСлушайте Стича в его подкасте SAPOD — vk.com/sapod &#128072;')
			
			elif payload == '{"command":"back"}' and id != 2000000002:
				msg(id, 'Возвращаю Вас в главное меню. Напоминаю назначение кнопок: \n\n#idea — идеи и предложения \n#partnership — партнёрство, сотрудничество, спонсорство \n#support — администрация, помощь и вопросы \n#buy — магазин услуг и покупки \n#news — последние новости из сферы IT', keyboards.menu)


		if id == 2000000002:
			if payload == '{"command":"request"}':
				msg(id, 'Решили запросить у кого-то деньги? У кого? Отправьте id пользователя.', keyboards.back)
				state_chat = 'wait request_id'

			elif state_chat == 'sending request_id':
				request_id = text.split()[1]
				msg(id, 'А какую сумму нужно запросить? Отправьте число.', keyboards.back)
				state_chat = 'wait amount'

			elif state_chat == 'sending amount':
				request_amount = text.split()[1]
				msg(id, 'Какое описание к запросу? Отправьте текст.')
				state_chat = 'wait description'

			elif state_chat == 'sending description':
				request_desc = ' '.join(text.split()[1:])
				try:
					msg(request_id, 'Меня попросили запросить у Вас оплату для «{}» на сумму в ₽{}. Подтвердите оплату...'.format(request_desc, request_amount), keyboards.payboard('action=pay-to-group&amount={}&description={}&group_id=132868814&aid=10'.format(request_amount, urllib.parse.quote(request_desc))))
					msg(id, 'Запрос оплаты у [id{0}|{1} {2}] прошёл успешно!'.format(request_id, name(request_id, 'gen')['first_name'], name(request_id, 'gen')['last_name']), keyboards.chat)
				except Exception as err:
					msg(id, 'Возникла проблема при запросе оплаты у пользователя. \n\n@pavetranquil (Павел), загляните в консоль и повторите попытку: dashboard.heroku.com/apps/ptcodding-bot/logs', keyboards.chat)
					print(err)
					print(traceback.format_exc())
				
			elif payload == '{"command":"restart"}':
				msg(id, 'Решили перезапустить меня? У кого? Отправьте id пользователя.', keyboards.back)
				state_chat = 'wait restart_id'

			elif state_chat == 'sending restart_id':
				restart_id = text.split()[1]
				msg(restart_id, 'Добрый день, {}! Видимо, наш PTBot где-то сломался, но сейчас уже всё хорошо. Приносим свои извинения, и перезапускаем его.\n\nС уважением, команда PTCodding.'.format(name(restart_id)['first_name']))
				msg(restart_id, 'Привет, это снова я, Ваш любимый PTBot! &#128075; Добро пожаловать в старое доброе меню! &#128526;', keyboards.menu)
				msg(id, 'Баг-перезапуск у [id{0}|{1} {2}] прошёл успешно!'.format(restart_id, name(restart_id, 'gen')['first_name'], name(restart_id, 'gen')['last_name']), keyboards.chat)

			elif payload == '{"command":"back"}':
				msg(id, 'Возвращаю вас в главное меню.', keyboards.chat)


	elif event.type == VkBotEventType.VKPAY_TRANSACTION:
		id = event.object.from_id
		amount = event.object.amount * 1000
		if event.object.description:
			if sex(id) == 1:
				msg(2000000002, '[id{0}|{1} {2}] перевела ₽{3} с комментарием «{4}»'.format(id, name(id)['first_name'], name(id)['last_name'], amount, text))
			else:
				msg(2000000002, '[id{0}|{1} {2}] перевёл ₽{3} с комментарием «{4}»'.format(id, name(id)['first_name'], name(id)['last_name'], amount, text))
		else:
			if sex(id) == 1:
				msg(2000000002, '[id{0}|{1} {2}] пожертвовала ₽{3}'.format(id, name(id)['first_name'], name(id)['last_name'], amount))
			else:
				msg(2000000002, '[id{0}|{1} {2}] пожертвовал ₽{3}'.format(id, name(id)['first_name'], name(id)['last_name'], amount))


	elif event.type == VkBotEventType.MESSAGE_ALLOW:
		id = event.object.user_id
		if sex(id) == 1:
			msg(2000000002, '&#128236; [id{0}|{1} {2}] разрешила присылать сообщения. \nДиалог с подписчиком: https://vk.com/gim132868814?sel={0}'.format(id, name(id)['first_name'], name(id)['last_name']))
		else:
			msg(2000000002, '&#128236; [id{0}|{1} {2}] разрешил присылать сообщения. \nДиалог с подписчиком: https://vk.com/gim132868814?sel={0}'.format(id, name(id)['first_name'], name(id)['last_name']))
	

	elif event.type == VkBotEventType.MESSAGE_DENY:
		id = event.object.user_id
		if sex(id) == 1:
			msg(2000000002, '&#128234; [id{0}|{1} {2}] запретил присылать сообщения.'.format(id, name(id)['first_name'], name(id)['last_name']))
		else:
			msg(2000000002, '&#128234; [id{0}|{1} {2}] запретил присылать сообщения.'.format(id, name(id)['first_name'], name(id)['last_name']))


	elif event.type == VkBotEventType.GROUP_JOIN:
		id = event.object.user_id
		if sex(id) == 1:
			msg(2000000002, '&#128150; [id{0}|{1} {2}] вступила в PTCodding.'.format(id, name(id)['first_name'], name(id)['last_name']))
		else:
			msg(2000000002, '&#128150; [id{0}|{1} {2}] вступил в PTCodding.'.format(id, name(id)['first_name'], name(id)['last_name']))


	elif event.type == VkBotEventType.GROUP_LEAVE:
		id = event.object.user_id
		if event.object.self:
			if sex(id) == 1:
				msg(2000000002, '&#128148; [id{0}|{1} {2}] покинула PTCodding.'.format(id, name(id)['first_name'], name(id)['last_name']))
			else:
				msg(2000000002, '&#128148; [id{0}|{1} {2}] покинул PTCodding.'.format(id, name(id)['first_name'], name(id)['last_name']))
		else:
			if sex(id) == 1:
				msg(2000000002, '&#128683; [id{0}|{1} {2}] удалёна из PTCodding.'.format(id, name(id)['first_name'], name(id)['last_name']))
			else:
				msg(2000000002, '&#128683; [id{0}|{1} {2}] удалён из PTCodding.'.format(id, name(id)['first_name'], name(id)['last_name']))


	elif event.type == VkBotEventType.WALL_REPOST:
		id = event.object.from_id
		wall_id = event.object.owner_id
		post_id = event.object.id
		if sex(id) == 1:
			msg(2000000002, '&#128226; [id{0}|{1} {2}] сделала репост записи из PTCodding. \nСсылка на запись: vk.com/wall{3}_{4}'.format(id, name(id)['first_name'], name(id)['last_name'], wall_id, post_id))
		else:
			msg(2000000002, '&#128226; [id{0}|{1} {2}] сделал репост записи из PTCodding. \nСсылка на запись: vk.com/wall{3}_{4}'.format(id, name(id)['first_name'], name(id)['last_name'], wall_id, post_id))
	

	elif event.type == VkBotEventType.WALL_REPLY_NEW:
		id = event.object.from_id
		comment_id = event.object.id
		post_id = event.object.post_id
		owner_id = event.object.owner_id
		if sex(id) == 1:
			msg(2000000002, '&#128196; [id{0}|{1} {2}] оставила комментарий к записи из PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=wall{3}_{4}_r{5}'.format(id, name(id)['first_name'], name(id)['last_name'], owner_id, post_id, comment_id))
		else:
			msg(2000000002, '&#128196; [id{0}|{1} {2}] оставил комментарий к записи из PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=wall{3}_{4}_r{5}'.format(id, name(id)['first_name'], name(id)['last_name'], owner_id, post_id, comment_id))


	elif event.type == VkBotEventType.BOARD_POST_NEW:
		id = event.object.from_id
		comment_id = event.object.id
		topic_id = event.object.topic_id
		owner_id = event.object.topic_owner_id
		if sex(id) == 1:
			msg(2000000002, '&#128196; [id{0}|{1} {2}] оставила комментарий в обсуждении PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=board{3}_{4}_?post={5}'.format(id, name(id)['first_name'], name(id)['last_name'], owner_id, topic_id, comment_id))
		else:
			msg(2000000002, '&#128196; [id{0}|{1} {2}] оставил комментарий в обсуждении PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=board{3}_{4}_?post={5}'.format(id, name(id)['first_name'], name(id)['last_name'], owner_id, topic_id, comment_id))


	elif event.type == VkBotEventType.MARKET_COMMENT_NEW:
		id = event.object.from_id
		item_id = event.object.item_id
		market_id = event.object.market_owner_id
		if sex(id) == 1:
			msg(2000000002, '&#128196; [id{0}|{1} {2}] оставила комментарий к товару PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=product{3}_{4}'.format(id, name(id)['first_name'], name(id)['last_name'], market_id, item_id))
		else:
			msg(2000000002, '&#128196; [id{0}|{1} {2}] оставил комментарий к товару PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=product{3}_{4}'.format(id, name(id)['first_name'], name(id)['last_name'], market_id, item_id))


	elif event.type == VkBotEventType.USER_UNBLOCK and event.object.by_end_date:
		id = event.object.user_id
		if sex(id) == 1:
			msg(2000000002, '&#127379; [id{0}|{1} {2}] удалёна из чёрного списка PTCodding по истечении срока блокировки.'.format(id, name(id)['first_name'], name(id)['last_name']))
		else:
			msg(2000000002, '&#127379; [id{0}|{1} {2}] удалён из чёрного списка PTCodding по истечении срока блокировки.'.format(id, name(id)['first_name'], name(id)['last_name']))


	elif event.type == VkBotEventType.POLL_VOTE_NEW:
		id = event.object.user_id
		if sex(id) == 1:
			msg(2000000002, '&#128202; [id{0}|{1} {2}] проголосовала в опросе по ссылке: vk.com/poll{3}_{4}'.format(id, name(id)['first_name'], name(id)['last_name'], event.object.owner_id, event.object.poll_id))
		else:
			msg(2000000002, '&#128202; [id{0}|{1} {2}] проголосовал в опросе по ссылке: vk.com/poll{3}_{4}'.format(id, name(id)['first_name'], name(id)['last_name'], event.object.owner_id, event.object.poll_id))


	elif event.type == VkBotEventType.GROUP_OFFICERS_EDIT:
		id = event.object.admin_id
		change_id = event.object.user_id
		levels = {0: 'Нет полномочий', 1: 'Модератор', 2: 'Редактор', 3: 'Администратор'}
		level_old = levels[event.object.level_old]
		level_new = levels[event.object.level_new]
		msg(2000000002, '&#127385; [id{0}|{1} {2}] изменил полномочия участника команды PTCodding [id{3}|{4} {5}] с «{6}» на «{7}»'.format(id, name(id)['first_name'], name(id)['last_name'], change_id, name(change_id, 'gen')['first_name'], name(change_id, 'gen')['last_name'], level_old, level_new))


	elif event.type == VkBotEventType.GROUP_CHANGE_PHOTO:
		id = event.object.user_id
		msg(2000000002, '&#128444 [id{0}|{1} {2}] изменил главную фотографию PTCodding'.format(id, name(id)['first_name'], name(id)['last_name']))
		

# except Exception:
# 	msg(2000000002, 'PTBot споткнулся о событие {} пользователя {}! \n\n@pavetranquil (Павел), загляните в консоль и исправьте баг: dashboard.heroku.com/apps/ptcodding-bot/log'.format(event.type, id))
#	print(err)
#	print(traceback.format_exc())