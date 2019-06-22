import keyboards, news
import urllib.parse, traceback
from methods import *

payload, state_chat, states = '', '', dict()

for event in longpoll.listen():
	try:
		print('\nЛовлю события... Поймал {}'.format(event.type))
		if event.type == VkBotEventType.MESSAGE_NEW:
			id = event.object.peer_id
			text = event.object.text
			msg_id = event.object.id
			payload = event.object.payload

			if id not in states:
				states[id] = ''

			if id == 2000000002:
				if state_chat == 'wait request_id' and ' '.join(text.split()[1:]) != 'Вернуться ↩':
					state_chat = 'sending request_id'
				elif state_chat == 'wait amount' and ' '.join(text.split()[1:]) != 'Вернуться ↩':
					state_chat = 'sending amount'
				elif state_chat == 'wait description' and ' '.join(text.split()[1:]) != 'Вернуться ↩':
					state_chat = 'sending description'
				elif state_chat == 'wait restart_id' and ' '.join(text.split()[1:]) != 'Вернуться ↩':
					state_chat = 'sending restart_id'
				else:
					state_chat = payload
			if id < 2000000000:
				if states[id] == 'wait idea' and text != 'Вернуться ↩':
					states[id] = 'sending idea'
				elif states[id] == 'wait question' and text != 'Вернуться ↩':
					states[id] = 'sending question'
				elif states[id] == 'wait partner' and text != 'Вернуться ↩':
					states[id] = 'sending partner'
				else:
					states[id] = payload


			if id == 2000000002 and (payload == '{"command":"start"}' or text.lower().find('начать') != -1):
				msg(id, 'Привет, команда PTCodding! Рад вас видеть! Вижу, что этот чат — чат моих создателей. Включаю дополнительные функции &#128522; \n\n#news — последние новости из сферы IT \nЗапрос VK Pay — запрос средств с указанием amount, description и id \nБаг-перезапуск — перезапуск бота по id с сообщением о баге', keyboards.chat)
			elif id < 2000000000 and states[id] == '{"command":"start"}': 
				msg(id, 'Привет, я PTBot, дворецкий команды PTCodding. \nНажмите на нужную Вам кнопку, чтобы команда нашла Вас и быстро ответила, а я не потерял Вас &#128522; \n\n#idea — идеи и предложения \n#partnership — партнёрство, сотрудничество, спонсорство \n#news — последние новости из сферы IT \n#market — магазин услуг и покупки \n#team — вопросы к команде и о команде', keyboards.menu)

			print('{} отправляет сообщение с текстом "{}"'.format(id, text))

			if id < 2000000000:
				if states[id] == '{"command":"idea"}':
					msg(id, "Предложите свою идею для PTCodding! Я pассмотрю её, и команда PTCodding отпишется Вам в этом диалоге. \nСоблюдайте структуру: \n1. Название, отражающее суть идеи \n2. Собственно идея, её развёртка \n3. Расскажите, чем Ваша идея поможет сообществу \nНе забудьте — необходимо уместить всё в рамках одного сообщения. Спасибо за Вашу помощь! \n\nС уважением, PTBot.", keyboards.back())
					states[id] = 'wait idea'

				elif states[id] == 'sending idea':
					print('{} отправляет идею'.format(id))
					msg(2000000002, '#botidea \n[id{0}|{1} {2}] предлагает идею.\n\nОтветить пользователю: https://vk.com/gim132868814?sel={0}'.format(id, name(id)['first_name'], name(id)['last_name']), forward=str(msg_id))
					msg(id, 'Ваша идея будет доставлена команде PTCodding в аккуратном конвертике с Вашей печатью. Ожидайте ответа! &#8986;', keyboards.menu)



				elif states[id] == '{"command":"partnership"}':
					msg(id, 'Станьте партнёрами PTCodding! Отправьте заявку сюда, и моё начальство рассмотрит её в ближайшие сроки. Следуйте моим советам:\n1. Расскажите о себе, чем Вы занимаетесь, какую компанию или бренд представляете. \n2. Прикрепите к заявке ссылку на Ваш проект. \n3. Расскажите о целях сотрудничества, чего бы хотели добиться. \n4. Скажите, какую выгоду получит PTCodding от партнёрства с Вами. \n\nОтправьте сообщение — оно и станет заявкой на партнёрство!', keyboards.back())
					states[id] = 'wait partner'

				elif states[id] == 'sending partner':
					print('{} предлагает партнёрство'.format(id))
					msg(2000000002, '#botpartner \n[id{0}|{1} {2}] предлагает партнёрство.\n\nОтветить пользователю: https://vk.com/gim132868814?sel={0}'.format(id, name(id)['first_name'], name(id)['last_name']), forward=str(msg_id))
					msg(id, 'Ждите ответа! Скоро с Вами свяжутся мои операторы! &#8986;', keyboards.menu)



				elif states[id] == '{"command":"team"}':
					msg(id, 'Здесь Вы сможете задать вопрос моему начальству, команде PTCodding, на абсолютно любую тему, какую только вздумается) &#128521;\nТакже можете почитать немного о команде: как появились они, как появился я, кто когда пришёл и какой вклад внёс &#128526;', keyboards.team)

				elif states[id] == '{"command":"question"}':
					msg(id, "Какие-то вопросы? Пишите — команда ответит на все! &#128170;", keyboards.back('team'))
					states[id] = 'wait question'

				elif states[id] == 'sending question':
					print('{} отправляет вопрос'.format(id))
					msg(2000000002, '#botquestion \n[id{0}|{1} {2}] задаёт вопрос.\n\nОтветить пользователю: https://vk.com/gim132868814?sel={0}'.format(id, name(id)['first_name'], name(id)['last_name']), forward=str(msg_id))
					msg(id, 'Ждите ответа на свой вопрос от команды PTCodding! &#8986;', keyboards.team)

				elif states[id] == '{"command":"about"}':
					msg(id, 'PTCodding появился 11 ноября 2016 года. За период с момента создания до 1 сентября 2018 года было сделано много крупных проектов: текстовая игра «Кто хочет стать миллионером?», «Мы — люди этой Земли!», прочие проекты. PTCodding наполнялся контент, команда опубликовала Backstage на свою деятельность. \nС 1 сентября начался активный прирост подписчиков, команда начала работать над медиа и активно развивалась в этом направлении. Был опубликован промо-ролик о митапе VK×Junction, 11 ноября на своё двухлетие PTCodding выпустил первый выпуск подкаста «Взгляд в неделю». \n2 февраля PTCodding переехал на платформу подкастов ВКонтакте и начал активно распространяться на других платформах подкастов. С марта по май в PTCodding публиковался подкаст «Игродайджест». В мае появился подкаст «IT-кухня». \n\nСейчас PTCodding — узнаваемый бренд в Санкт-Петербурге, известный как команда подростков, которые делают качественный и уникальный IT-контент. Каждый день они растут и становятся лучше и известнее, популяризуя программирование и IT-технологии в массы. Они записывают подкасты, пишут лонгриды, делают музыкальные подборки!\n\nВы можете подробнее почитать о каждом участнике команды ниже, нажав на кнопку с именем участника! &#128071;', keyboards.about)

				elif states[id] == '{"command":"Pavel"}':
					msg(id, 'Павел — основатель PTCodding. Именно под его началом были созданы многие код-проекты, концепт и окружение бренда. Павел является шеф-редактором на платформе лонгридов, главным ведущим подкастов «Взгляд в неделю» и «IT-кухня», шеф-кодером в команде программистов. Он ищет новых партнёров и достойных людей для сотрудничества и работы в команде PTCodding, думает над дальнейшим продвижением и мыслит неординарно, чтобы PTCodding становился лучше для своих слушателей и читателей. Одним из крупнейших проектов Павла являюсь я — PTBot, чат-бот PTCodding!')

				elif states[id] == '{"command":"Bogdan"}':
					msg(id, 'Богдан — дизайнер PTCodding. Присоединился к команде 14 сентября 2017 года. Под его началом были сделаны все аватарки, шапки сообщества и обложки к лонгридам. Всё окружение бренда, весь дизайн были сделаны его руками. Является соведущим подкаста «IT-кухня», некоторое время вёл рубрику «Бюдгаджет месяца». Является активным участником команды PTCodding, участвует во всех общих принятиях решений, опросах и активно продвигает свои мнения и позиции. Одним из последних проектов стал редизайн товаров в магазине PTCodding.')

				elif states[id] == '{"command":"Kseno"}':
					msg(id, 'Ксено — творческий и в некоторых вопросах юридический мозг команды PTCodding, генератор идей. Присоединилась к команде 4 февраля 2018 года. Именно в её голове зародилась идея делать подкасты. Когда команда выясняла, с чего начать, Ксения предложила записывать еженедельный подкаст, в котором озвучиваются новости ушедшей недели — подкаст «Взгляд в неделю». Принимала участие в записи бонусного выпуска 1 июня.')

				elif states[id] == '{"command":"back_team"}':
					msg(id, 'Возвращаю Вас в меню команды.', keyboards.team)



				elif states[id] == '{"command":"buy"}':
					msg(id, 'В разделе покупок Вы можете приобрести у нас виртуальные услуги и услуги на дом — рекламу, программирование и дизайн от моего начальства, звукозапись и ремонт Вашего ПК или Android-смартфона. &#128230; \nЕщё если Вы вдруг потеряетесь, то всегда можете заглянуть в привычную корзину и магазин от ВКонтакте))) &#128071;', keyboards.buy)

				elif states[id] == '{"command":"code"}':
					msg(id, 'Цена: от 200 руб. &#128181; \n\nМоё начальство напишет чат-бота ВКонтакте или в Telegram под Ваши цели и по Вашим требованиям. Ваши данные: описание функционала и ключевых целей и задач чат-бота, сгенерированный longpoll-токен. \nХочу предупредить Вас: если Вам не понравился чат-бот, есть какие-то проблемы, ошибки, баги, то необходимо сразу же сообщить об этом. Любые недочёты исправляются одним нажатием клавиши. \nВ чат-боте прописан его создатель, с указанием авторства на сообщество PTCodding. Просьбы вернуть деньги после того, как Вы установили чат-бота в своё сообщество, не принимаются. \nЦена может изменяться в зависимости от срока заказа, указана минимальная цена! Также могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2055522 &#128072;', keyboards.itemboard('code'))
				elif states[id] == '{"command":"add_code"}':
					msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Создание чат-бота.code'))
				elif states[id] == '{"command":"delete_code"}':
					msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Создание чат-бота.code'))

				elif states[id] == '{"command":"design"}':
					msg(id, 'Цена: от 200 руб. &#128181; \n\nМоё начальство создаст дизайн Вашему бренду по Вашим требованиям. Ваши данные: название бренда, для которого делается дизайн, стиль исполнения. \nХочу предупредить Вас: если Вам не понравился какой-то элемент дизайна, то ему необходимо сразу написать об этом. Любые недочёты исправляются одним нажатием клавиши. \nНа весь пак дизайна, до оплаты заказа, будет нанесён водяной знак. Просьбы вернуть деньги после того, как Вы оплатили заказ и пак был передан без водяных знаков, не принимаются. \nЦена может изменяться в зависимости от срока заказа и техники выполнения, указана минимальная цена! Также могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2064351 &#128072;', keyboards.itemboard('design'))
				elif states[id] == '{"command":"add_design"}':
					msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Создание дизайна.design'))
				elif states[id] == '{"command":"delete_design"}':
					msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Создание дизайна.design'))

				elif states[id] == '{"command":"record"}':
					msg(id, 'Цена: от 750 руб. &#128181; \n\nМоё начальство запишет Ваш голос на своей домашней студии, обработает звук и отправит исходники в mp3, wav или другом формате на флешку, ВКонтакте или в облако. \nПри заказе дополнительно сведения, мастеринга или же при полноценной запись под ключ цена оговаривается при оформлении заказа. \nХочу предупредить Вас: на весь звуковой файл накладывается демо-фраза до оплаты заказа. Просьбы вернуть деньги после того, как Вы оплатили заказ и файл был передан без демо-фразы, не принимаются. \nЦена может изменяться в зависимости от срока заказа и дополнительных услуг, указана минимальная цена! Для клиентов могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2561900 &#128072;', keyboards.itemboard('record'))
				elif states[id] == '{"command":"add_record"}':
					msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'Звукозапись.record'))
				elif states[id] == '{"command":"delete_record"}':
					msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'Звукозапись.record'))

				elif states[id] == '{"command":"fix"}':
					msg(id, 'Цена: от 500 руб. &#128181; \n\nМоё начальство также работает с компьютерами и смартфонами: исправляет мелкие неполадки в работе, устанавливает лицензированный Microsoft Office или иное ПО, устанавливают активированную Windows, перепрошивают Android-смартфоны. \nХочу предупредить Вас: проверяйте работоспособность ПО, ПК или смартфона в целом сразу перед оплатой заказа. PTCodding даёт бесплатную гарантию — 1 месяц. Далее гарантия продлевается платно. \nЦена может изменяться в зависимости от срока заказа, указана минимальная цена! Для клиентов могут появляться специальные условия! \n\nСсылка на товар в нашем магазине ВКонтакте: vk.com/ptcodding?w=product-132868814_2561901 &#128072;', keyboards.itemboard('fix'))
				elif states[id] == '{"command":"add_fix"}':
					msg(id, 'Товар добавлен в Вашу корзину', keyboards.cartboard(id, 'ПК и смартфоны.fix'))
				elif states[id] == '{"command":"delete_fix"}':
					msg(id, 'Товар удалён из Вашей корзины', keyboards.cartboard(id, 'ПК и смартфоны.fix'))

				elif states[id] == '{"command":"cart"}':
					msg(id, 'Корзина товаров, которые Вы добавили к заказу. \nТовары удаляются из корзины при нажатии на них. Если Вы добавили в корзину какие-то товары, то будет доступна кнопка оформления заказа — нажмите на неё, и с Вами в этом чате свяжутся мои операторы, которые обсудят все условия и цены &#128222;', keyboards.cartboard(id))
						
				elif states[id] == '{"command":"cart_ui"}':
					msg(id, 'Загляните в привычный магазин, если мой Вам оказался не по душе: https://vk.com/market-132868814 &#128072;', keyboards.back('buy'))

				elif states[id] == '{"command":"order"}':
					msg(2000000002, 'Вас вызывают для оформления заказа. Пройдите, пожалуйста, по этой ссылке: https://vk.com/gim132868814?sel={}'.format(id))
					msg(id, 'Ожидайте... Скоро мои операторы свяжутся с Вами для уточнения деталей и оплаты заказа! &#8986;')
				
				elif states[id] == '{"command":"back_buy"}':
					msg(id, 'Возвращаю Вас в меню товаров.', keyboards.buy)



				elif states[id] == '{"command":"news"}':
					news.refresh()
					news_text = ''
					for i in range(0,8):
						news_text += str(i+1) + '. ' + news.headers[i] + '\n'
					msg(id, 'Самый востребованный раздел PTBot! 😱💻 \n\nПоследние новости из мира IT:\n' + news_text + '\n\nДанные взяты с сайта news.yandex.ru', keyboards.news, parse=False)

				elif states[id] == '{"command":"1"}':
					header = news.headers[0]
					desc = news.descs[0]
					original = news.originals[0]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))
				
				elif states[id] == '{"command":"2"}':
					header = news.headers[1]
					desc = news.descs[1]
					original = news.originals[1]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))

				elif states[id] == '{"command":"3"}':
					header = news.headers[2]
					desc = news.descs[2]
					original = news.originals[2]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))
				
				elif states[id] == '{"command":"4"}':
					header = news.headers[3]
					desc = news.descs[3]
					original = news.originals[3]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))

				elif states[id] == '{"command":"5"}':
					header = news.headers[4]
					desc = news.descs[4]
					original = news.originals[4]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))
				
				elif states[id] == '{"command":"6"}':
					header = news.headers[5]
					desc = news.descs[5]
					original = news.originals[5]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))

				elif states[id] == '{"command":"7"}':
					header = news.headers[6]
					desc = news.descs[6]
					original = news.originals[6]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))
				
				elif states[id] == '{"command":"8"}':
					header = news.headers[7]
					desc = news.descs[7]
					original = news.originals[7]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))

				elif states[id] == '{"command":"refresh"}':
					try:
						delete(get_id(165504240, 1))
					except Exception:
						pass
					news.refresh()
					news_text = ''
					for i in range(0,8):
						news_text += str(i+1) + '. ' + news.headers[i] + '\n'
					msg(id, 'Обновляю список новостей... \n\nПоследние новости из мира IT:\n' + news_text + '\n\nДанные взяты с сайта news.yandex.ru', parse=False)

				elif states[id] == '{"command":"back_news"}':
					news_text = ''
					for i in range(0,8):
						news_text += str(i+1) + '. ' + news.headers[i] + '\n'
					msg(id, 'Возвращаю вас обратно к выбору новостей... \n\nПоследние новости из мира IT:\n' + news_text + '\n\nДанные взяты с сайта news.yandex.ru', keyboards.news, parse=False)



				elif states[id] == '{"command":"donat"}':
					msg(id, 'Я очень хочу кушать. Я голодный... &#128546; Дайте, пожалуйста, пару долларов, чтобы мне купили пончик. &#127849;', keyboards.donatboard('action=transfer-to-group&group_id=132868814&aid=10'))

				elif states[id] == '{"command":"app_donat"}':
					msg(id, 'Если хотите поддержать наш проект, то лучше сделайте пожертвование через приложение — так Вы не просто поддержите нас, но и продвинете проект! &#128200;', keyboards.appboard(6887721, -132868814, 'Пончик — наши донаты &#127849;'))


				
				elif states[id] == '{"command":"partners"}':
					msg(id, 'Добро пожаловать в список партнёров команды PTCodding! Благодаря этим людям в PTCodding очень многое изменяется. Я как чат-бот сообщества наблюдаю за всем этим со стороны — PTCodding растёт на глазах! &#128079;', keyboards.partner)
				
				elif states[id] == '{"command":"sapod"}':
					msg(id, '@sapod (SAPOD) — первый и единственный подкаст из мира San Andreas. \n\nВедущий подкаста Стич часто появляется и в подкастах от PTCodding. Вместе с Павлом они обсуждают новости уходящего месяца в IT-кухне и жарко спорят, кто лучше: iOS или Android &#128521;\n\nСлушайте Стича в его подкасте SAPOD — vk.com/sapod &#128072;')
				


				elif states[id] == '{"command":"back"}':
					msg(id, 'Возвращаю Вас в главное меню. Напоминаю назначение кнопок: \n\n#idea — идеи и предложения \n#partnership — партнёрство, сотрудничество, спонсорство \n#news — последние новости из сферы IT \n#market — магазин услуг и покупки \n#team — вопросы к команде и о команде', keyboards.menu)



			if id == 2000000002:
				if state_chat == '{"command":"news"}':
					news.refresh()
					news_text = ''
					for i in range(0,8):
						news_text += str(i+1) + '. ' + news.headers[i] + '\n'
					msg(id, 'Самый востребованный раздел PTBot! 😱💻 \n\nПоследние новости из мира IT:\n' + news_text + '\n\nДанные взяты с сайта news.yandex.ru', keyboards.news, parse=False)

				elif state_chat == '{"command":"1"}':
					header = news.headers[0]
					desc = news.descs[0]
					original = news.originals[0]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))
				
				elif state_chat == '{"command":"2"}':
					header = news.headers[1]
					desc = news.descs[1]
					original = news.originals[1]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))

				elif state_chat == '{"command":"3"}':
					header = news.headers[2]
					desc = news.descs[2]
					original = news.originals[2]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))
				
				elif state_chat == '{"command":"4"}':
					header = news.headers[3]
					desc = news.descs[3]
					original = news.originals[3]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))

				elif state_chat == '{"command":"5"}':
					header = news.headers[4]
					desc = news.descs[4]
					original = news.originals[4]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))
				
				elif state_chat == '{"command":"6"}':
					header = news.headers[5]
					desc = news.descs[5]
					original = news.originals[5]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))

				elif state_chat == '{"command":"7"}':
					header = news.headers[6]
					desc = news.descs[6]
					original = news.originals[6]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))
				
				elif state_chat == '{"command":"8"}':
					header = news.headers[7]
					desc = news.descs[7]
					original = news.originals[7]
					msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.back('news'))

				elif state_chat == '{"command":"refresh"}':
					try:
						delete(get_id(165504240, 1))
					except Exception:
						pass
					news.refresh()
					news_text = ''
					for i in range(0,8):
						news_text += str(i+1) + '. ' + news.headers[i] + '\n'
					msg(id, 'Обновляю список новостей... \n\nПоследние новости из мира IT:\n' + news_text + '\n\nДанные взяты с сайта news.yandex.ru', parse=False)

				elif state_chat == '{"command":"back_news"}':
					news_text = ''
					for i in range(0,8):
						news_text += str(i+1) + '. ' + news.headers[i] + '\n'
					msg(id, 'Возвращаю вас обратно к выбору новостей... \n\nПоследние новости из мира IT:\n' + news_text + '\n\nДанные взяты с сайта news.yandex.ru', keyboards.news, parse=False)


				elif state_chat == '{"command":"request"}':
					msg(id, 'Решили запросить у кого-то деньги? У кого? Отправьте id пользователя.', keyboards.back())
					state_chat = 'wait request_id'

				elif state_chat == 'sending request_id':
					request_id = text.split()[1]
					msg(id, 'А какую сумму нужно запросить? Отправьте число.', keyboards.back())
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

					
				elif state_chat == '{"command":"restart"}':
					msg(id, 'Решили перезапустить меня? У кого? Отправьте id пользователя.', keyboards.back())
					state_chat = 'wait restart_id'

				elif state_chat == 'sending restart_id':
					restart_id = text.split()[1]
					msg(restart_id, 'Добрый день, {}! Видимо, наш PTBot где-то сломался, но сейчас уже всё хорошо. Приносим свои извинения, и перезапускаем его.\n\nС уважением, команда PTCodding.'.format(name(restart_id)['first_name']))
					msg(restart_id, 'Привет, это снова я, Ваш любимый PTBot! &#128075; Добро пожаловать в старое доброе меню! &#128526;', keyboards.menu)
					msg(id, 'Баг-перезапуск у [id{0}|{1} {2}] прошёл успешно!'.format(restart_id, name(restart_id, 'gen')['first_name'], name(restart_id, 'gen')['last_name']), keyboards.chat)


				elif state_chat == '{"command":"back_to_start"}':
					msg(id, 'Кого возвращаем к самому началу? Отправьте id пользователя.', keyboards.back())
					state_chat = 'wait start_id'

				elif state_chat == 'wait start_id':
					start_id = text.split()[1]
					msg(start_id, 'Машина времени чудесна... С её помощью можно вернуть нас к тому моменту, когда мы ещё не были знакомы...', keyboard.start())
					try:
						delete(get_id(start_id, 0))
					except Exception:
						pass
					msg(id, 'Возврат к началу у [id{0}|{1} {2}] прошёл успешно!'.format(start_id, name(start_id, 'gen')['first_name'], name(start_id, 'gen')['last_name']), keyboards.chat)


				elif state_chat == '{"command":"back"}':
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

	except Exception as err:
		msg(2000000002, 'PTBot споткнулся о событие {} пользователя {}! \n\n@pavetranquil (Павел), загляните в консоль и исправьте баг: dashboard.heroku.com/apps/ptcodding-bot/logs'.format(event.type, id))
		print(err)
		print(traceback.format_exc())
	