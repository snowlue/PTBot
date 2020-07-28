import keyboards
import news
import urllib.parse
import traceback
import time
from methods import msg, msg_edit, name, link, sex, get_id, delete, isMember, parse_docs, get_allow, upload, read_data, VkBotEventType, longpoll

data = read_data()
states, news_types, mails, mute = data[0], data[1], data[2], data[3]
keyboards.carts = data[4]
payload, state_chat, admin_chat = '', '', 2*10**9+6
internet_text, gadgets_text, games_text = '', '', ''
request_id, request_amount, request_desc, mail_text, mail_docs = '', '', '', '', ''
last_request = time.time()

print('main.py started!\n---------------------')


def main():
    global event, payload, state_chat, admin_chat, states, news_types, mails, mute
    global internet_text, gadgets_text, games_text
    global request_id, request_amount, request_desc, mail_text, mail_docs
    try:
        if event.type not in [VkBotEventType.MESSAGE_REPLY, VkBotEventType.MESSAGE_EDIT]:
            print('\nЛовлю события... Поймал {}'.format(event.type))
        if event.type in [VkBotEventType.MESSAGE_NEW, 'message_event']:
            if event.type == VkBotEventType.MESSAGE_NEW:
                id = event.object['message']['peer_id']  # всегда число!
                payload = event.object['message']['payload'] if 'payload' in event.object['message'] else ''
                text = event.object['message']['text']
                msg_id = event.object['message']['id']
                attachments = event.object['message']['attachments']
                print('{} отправляет сообщение с текстом "{}"'.format(id, text))
            else:
                id = event.object['peer_id']
                payload = str(event.object['payload']) if 'payload' in event.object else ''
                cb_msg_id = event.object['conversation_message_id']
                print('{} нажимает на Callback-кнопку'.format(id))
                

            if id not in states:
                states[id] = ''
            if id not in news_types:
                news_types[id] = ''
            if id not in mails:
                mails[id] = True if id < 2*10**9 else False
            if id not in keyboards.carts:
                keyboards.carts[id] = []

            if id == admin_chat:
                if state_chat == 'wait request_id' and payload != '{"command":"cancel"}':
                    state_chat = 'sending request_id'
                elif state_chat == 'wait amount' and payload != '{"command":"cancel"}':
                    state_chat = 'sending amount'
                elif state_chat == 'wait description' and payload != '{"command":"cancel"}':
                    state_chat = 'sending description'
                elif state_chat == 'wait restart_id' and payload != '{"command":"cancel"}':
                    state_chat = 'sending restart_id'
                elif state_chat == 'wait mail_text' and payload != '{"command":"cancel"}':
                    state_chat = 'sending mail_text'
                elif state_chat == 'wait mail_confirm' and payload != '{"command":"cancel"}':
                    state_chat = 'sending mail_confirm'
                else:
                    state_chat = payload
            else:
                if states[id] == 'wait question' and payload != '{"command":"back_team"}':
                    states[id] = 'sending question'
                elif states[id] == 'wait partner' and payload != '{"command":"back"}':
                    states[id] = 'sending partner'
                else:
                    states[id] = payload
            try:
                if id < 2*10**9 and (states[id] == '{"command":"start"}' or 'нач' in text.lower().split()[0] or 'start' in text.lower().split()[0] or 'ptbot' in text.lower().split()[0] or 'поехали' in text.lower().split()[0] or 'появи' in text.lower().split()[0] or 'откр' in text.lower().split()[0] or 'эй' in text.lower().split()[0] or 'клавиатур' in text.lower().split()[0]) and states[id] not in ['sending idea', 'sending question', 'sending partner']:
                    msg(id, 
'''Привет, я PTBot — дворецкий команды PTCodding. 
Нажмите на нужную Вам кнопку, чтобы команда нашла Вас и быстро ответила, а я не потерял Вас &#128522;

#news — последние новости из сферы IT
#partnership — партнёрство, сотрудничество, спонсорство
#market — магазин услуг и покупки
#team — вопросы к команде и о команде''',
                    keyboards.menu(mails[id]))
                    states[id] = '{"command":"start"}'
                elif id > 2*10**9 and ('нач' in text.lower().split()[1] or 'start' in text.lower().split()[1] or 'ptbot' in text.lower().split()[1] or 'поехали' in text.lower().split()[1] or 'появи' in text.lower().split()[1] or 'откр' in text.lower().split()[1] or 'эй' in text.lower().split()[1] or 'клавиатур' in text.lower().split()[1]):
                    msg(id, 'Привет, я PTBot — чат-бот команды PTCodding. &#9995; С моей помощью вы можете узнать последние новости и задонатить на топовый функционал моим создателям — @ptcodding (команде PTCodding). Если вдруг я стану не нужен, напишите «увидимся», «пока» или что-нибудь в этом роде.',
                        keyboards.conversation(mails[id]))
                    states[id] = '{"command":"start"}'
            except Exception:
                pass


            if id != admin_chat:

                if states[id] == '{"command":"partnership"}':
                    msg(id,
'''Станьте партнёрами PTCodding! Отправьте заявку сюда, и моё начальство рассмотрит её в ближайшие сроки. Следуйте моим советам:
1. Расскажите о себе, чем Вы занимаетесь, какую компанию или бренд представляете.
2. Прикрепите к заявке ссылку на Ваш проект.
3. Расскажите о целях сотрудничества, чего бы хотели добиться.
4. Скажите, какую выгоду получит PTCodding от партнёрства с Вами.

Отправьте сообщение — оно и станет заявкой на партнёрство!''',
                        keyboards.back())
                    states[id] = 'wait partner'

                elif states[id] == 'sending partner':
                    print('{} предлагает партнёрство'.format(id))
                    if id not in mute:
                        msg(admin_chat,
'''#botpartner
[id{0}|{1} {2}] предлагает партнёрство.

Ответить пользователю: https://vk.com/gim132868814?sel={0}'''.format(
                            id, name(id)['first_name'], name(id)['last_name']), forward=str(msg_id))
                        msg(id, 'Ждите ответа! Скоро с Вами свяжутся мои операторы! &#8986;',
                            keyboards.menu(mails[id]))

                elif states[id] == '{"command":"team"}':
                    msg(id,
'''Здесь Вы сможете задать вопрос моему начальству, команде PTCodding, на абсолютно любую тему, какую только вздумается) &#128521;
Также можете почитать немного о команде: как появились они, как появился я, кто когда пришёл и какой вклад внёс &#128526;''',
                        keyboards.team)

                elif states[id] == '{"command":"question"}':
                    msg(id, "Какие-то вопросы? Пишите — команда ответит на всё! &#128170;", keyboards.back('team'))
                    states[id] = 'wait question'

                elif states[id] == 'sending question':
                    print('{} отправляет вопрос'.format(id))
                    if id not in mute:
                        msg(admin_chat,
'''#botquestion
[id{0}|{1} {2}] задаёт вопрос.

Ответить пользователю: https://vk.com/gim132868814?sel={0}'''.format(
                            id, name(id)['first_name'], name(id)['last_name']), forward=str(msg_id))
                        msg(id, 'Ждите ответа на свой вопрос от команды PTCodding! &#8986;', keyboards.team)

                elif states[id] == '{"command":"about"}':
                    msg(id,
'''PTCodding появился 11 ноября 2016 года. За период с момента создания до 1 сентября 2018 года было сделано много крупных проектов: текстовая игра «Кто хочет стать миллионером?», «Мы — люди этой Земли!» и другие.
А уже с 1 сентября начался активный прирост подписчиков, команда начала работать над медиа и активно развивалась в этом направлении. Был опубликован промо-ролик о митапе VK×Junction, 11 ноября на своё двухлетие PTCodding выпустил первый выпуск подкаста «Взгляд в неделю».
2 февраля 2019 года PTCodding переехал на платформу подкастов ВКонтакте и начал активно распространяться на других. С марта по май в PTCodding публиковался экспериментальный подкаст «Игродайджест». В мае появился подкаст «IT-кухня».

Сейчас PTCodding — узнаваемый бренд, известный как команда молодых энтузиастов, которые делают качественный и уникальный IT-контент. Они записывают подкасты, пишут лонгриды, делают музыкальные подборки, популяризуя программирование и IT-технологии в массы.

Вы можете подробнее почитать о каждом участнике команды ниже, нажав на кнопку с именем участника! &#128071;''', 
                        keyboards.about)

                elif states[id] == '{"command":"Pavel"}':
                    msg(id, 'Павел — основатель PTCodding. Именно под его началом были созданы многие код-проекты, концепт и окружение бренда. Павел является шеф-редактором на платформе лонгридов, шеф-кодером в команде программистов. Думает над дальнейшим продвижением и мыслит неординарно, чтобы PTCodding становился лучше для своих слушателей и читателей. Одним из крупнейших проектов Павла являюсь я — PTBot, чат-бот PTCodding!')

                elif states[id] == '{"command":"Bogdan"}':
                    msg(id, 'Богдан — дизайнер PTCodding. Присоединился к команде 14 сентября 2017 года. Под его началом были сделаны все аватарки, шапки сообщества и обложки к лонгридам. Окружение бренда, дизайн и визуалка были сделаны его руками. Является соведущим подкаста «IT-кухня», некоторое время вёл рубрику «Бюдгаджет месяца». Одним из последних проектов стал редизайн товаров в магазине PTCodding.')

                elif states[id] == '{"command":"Dima"}':
                    msg(id, 'Дима — генератор идей команды PTCodding, главный редактор. Присоединился к команде 5 мая 2020 года. Нарисовал характеристики к «Бюдгаджету месяца». Ищет новых партнёров и достойных людей для сотрудничества и работы с командой PTCodding.')

                elif states[id] == '{"command":"back_team"}':
                    msg(id, 'Возвращаю Вас в меню команды.', keyboards.team)

                elif states[id] == '{"command":"buy"}':
                    msg(id,
'''В разделе покупок Вы можете приобрести у нас виртуальные услуги и услуги на дом — рекламу, программирование и дизайн от моего начальства, звукозапись и ремонт Вашего ПК или Android-смартфона. &#128230;
Ещё если Вы вдруг потеряетесь, то всегда можете заглянуть в привычную корзину и магазин от ВКонтакте))) &#128071;''',
                        keyboards.buy)

                elif states[id] == '{"command":"code"}':
                    msg(id,
'''Цена: от 200 руб. &#128181;

Моё начальство напишет чат-бота ВКонтакте или в Telegram под Ваши цели и по Вашим требованиям. Ваши данные: описание функционала и ключевых целей и задач чат-бота, сгенерированный longpoll-токен.
Хочу предупредить Вас: если Вам не понравился чат-бот, есть какие-то проблемы, ошибки, баги, то необходимо сразу же сообщить об этом. Любые недочёты исправляются одним нажатием клавиши.
В чат-боте прописан его создатель, с указанием авторства на сообщество PTCodding. Просьбы вернуть деньги после того, как Вы установили чат-бота в своё сообщество, не принимаются.
Цена может изменяться в зависимости от срока заказа, указана минимальная цена! Также могут появляться специальные условия!

[vk.com/ptcodding?w=product-132868814_2055522|А ещё товар есть в магазине ВКонтакте] &#128072;''',
                        keyboards.itemboard('code'))
                elif states[id] == '{"command":"add_code"}':
                    if 'Создание чат-бота.code' not in keyboards.carts[id]:
                        msg(id, 'Товар добавлен в Вашу корзину.',
                            keyboards.cartboard(id, 'Создание чат-бота.code'))
                    else:
                        msg(id, 'Товар уже в корзине.', keyboards.cartboard(id))
                elif states[id] == '{"command":"delete_code"}':
                    msg(id, 'Товар удалён из Вашей корзины.', keyboards.cartboard(id, 'Создание чат-бота.code'))

                elif states[id] == '{"command":"design"}':
                    msg(id,
'''Цена: от 200 руб. &#128181;

Моё начальство создаст дизайн Вашему бренду по Вашим требованиям. Ваши данные: название бренда, для которого делается дизайн, стиль исполнения.
Хочу предупредить Вас: если Вам не понравился какой-то элемент дизайна, то ему необходимо сразу написать об этом. Любые недочёты исправляются одним нажатием клавиши.
На весь пак дизайна, до оплаты заказа, будет нанесён водяной знак. Просьбы вернуть деньги после того, как Вы оплатили заказ и пак был передан без водяных знаков, не принимаются.
Цена может изменяться в зависимости от срока заказа и техники выполнения, указана минимальная цена! Также могут появляться специальные условия!

[vk.com/ptcodding?w=product-132868814_2064351|А ещё товар есть в магазине ВКонтакте] &#128072;''',
                        keyboards.itemboard('design'))
                elif states[id] == '{"command":"add_design"}':
                    if 'Создание дизайна.design' not in keyboards.carts[id]:
                        msg(id, 'Товар добавлен в Вашу корзину.',
                            keyboards.cartboard(id, 'Создание дизайна.design'))
                    else:
                        msg(id, 'Товар уже в корзине.', keyboards.cartboard(id))
                elif states[id] == '{"command":"delete_design"}':
                    msg(id, 'Товар удалён из Вашей корзины.', keyboards.cartboard(id, 'Создание дизайна.design'))

                elif states[id] == '{"command":"record"}':
                    msg(id,
'''Цена: от 750 руб. &#128181;

Моё начальство запишет Ваш голос на своей домашней студии, обработает звук и отправит исходники в mp3, wav или другом формате на флешку, ВКонтакте или в облако.
При заказе дополнительно сведения, мастеринга или же при полноценной запись под ключ цена оговаривается при оформлении заказа.
Хочу предупредить Вас: на весь звуковой файл накладывается демо-фраза до оплаты заказа. Просьбы вернуть деньги после того, как Вы оплатили заказ и файл был передан без демо-фразы, не принимаются.
Цена может изменяться в зависимости от срока заказа и дополнительных услуг, указана минимальная цена! Для клиентов могут появляться специальные условия!

[vk.com/ptcodding?w=product-132868814_2561900|А ещё товар есть в магазине ВКонтакте] &#128072;''',
                        keyboards.itemboard('record'))
                elif states[id] == '{"command":"add_record"}':
                    if 'Звукозапись.record' not in keyboards.carts[id]:
                        msg(id, 'Товар добавлен в Вашу корзину.', keyboards.cartboard(id, 'Звукозапись.record'))
                    else:
                        msg(id, 'Товар уже в корзине.', keyboards.cartboard(id))
                elif states[id] == '{"command":"delete_record"}':
                    msg(id, 'Товар удалён из Вашей корзины.', keyboards.cartboard(id, 'Звукозапись.record'))

                elif states[id] == '{"command":"fix"}':
                    msg(id,
'''Цена: от 500 руб. &#128181;

Моё начальство также работает с компьютерами и смартфонами: исправляет мелкие неполадки в работе, устанавливает лицензированный Microsoft Office или иное ПО, устанавливают активированную Windows, перепрошивают Android-смартфоны.
Хочу предупредить Вас: проверяйте работоспособность ПО, ПК или смартфона в целом сразу перед оплатой заказа. PTCodding даёт бесплатную гарантию — 1 месяц. Далее гарантия продлевается платно.
Цена может изменяться в зависимости от срока заказа, указана минимальная цена! Для клиентов могут появляться специальные условия!

[vk.com/ptcodding?w=product-132868814_2561901|А ещё товар есть в магазине ВКонтакте] &#128072;''',
                        keyboards.itemboard('fix'))
                elif states[id] == '{"command":"add_fix"}':
                    if 'ПК и смартфоны.fix' not in keyboards.carts[id]:
                        msg(id, 'Товар добавлен в Вашу корзину.', keyboards.cartboard(id, 'ПК и смартфоны.fix'))
                    else:
                        msg(id, 'Товар уже в корзине.', keyboards.cartboard(id))
                elif states[id] == '{"command":"delete_fix"}':
                    msg(id, 'Товар удалён из Вашей корзины.', keyboards.cartboard(id, 'ПК и смартфоны.fix'))

                elif states[id] == '{"command":"cart"}':
                    msg(id,
'''Корзина товаров, которые Вы добавили к заказу.
Товары удаляются из корзины при нажатии на них. Если Вы добавили в корзину какие-то товары, то будет доступна кнопка оформления заказа — нажмите на неё, и с Вами в этом чате свяжутся мои операторы, которые обсудят все условия и цены &#128222;''', 
                        keyboards.cartboard(id))

                elif states[id] == '{"command":"cart_ui"}':
                    msg(id, 'Загляните в привычный магазин, если мой Вам оказался не по душе: vk.com/market-132868814 &#128072;')

                elif states[id] == '{"command":"order"}':
                    print('{} оформляет заказ.'.format(id))
                    if id not in mute:
                        msg(admin_chat,
'''#order
Вас вызывают для оформления заказа. Пройдите, пожалуйста, по этой ссылке: https://vk.com/gim132868814?sel={}'''.format(id))
                        keyboards.carts[id] = []
                        msg(id, 'Ожидайте... Скоро мои операторы свяжутся с Вами для уточнения деталей и оплаты заказа! &#8986;',
                            keyboards.cartboard(id))

                elif states[id] == '{"command":"back_buy"}':
                    msg(id, 'Возвращаю Вас в меню товаров.', keyboards.buy)

                elif states[id] == '{"command":"news"}':
                    msg(id,
'''Самый востребованный раздел PTBot — новости из мира IT прямо в этом чате! 😱💻
Выберите категорию: интернет, гаджеты или игры — и читайте топ-8 новостей!

Обновление каждые 10 минут.
Данные взяты из news.yandex.ru''',
                        keyboards.news, parse=False)

                elif states[id] == "{'command': 'news_internet'}":
                    news_types[id] = 'internet'
                    if not internet_text:
                        for i in range(0, 8):
                            internet_text += str(i+1) + '&#8419; ' + news.headers_internet[i] + '\n'
                    msg_edit(id, cb_msg_id, 'Последние новости из мира интернета на сегодня: \n' +
                        internet_text, keyboards.listboard())

                elif states[id] == "{'command': 'news_gadgets'}":
                    news_types[id] = 'gadgets'
                    if not gadgets_text:
                        for i in range(0, 8):
                            gadgets_text += str(i+1) + '&#8419; ' + news.headers_gadgets[i] + '\n'
                    msg_edit(id, cb_msg_id, 'Последние новости из мира гаджетов на сегодня: \n' +
                        gadgets_text, keyboards.listboard())

                elif states[id] == "{'command': 'news_games'}":
                    news_types[id] = 'games'
                    if not games_text:
                        for i in range(0, 8):
                            games_text += str(i+1) + '&#8419; ' + news.headers_games[i] + '\n'
                    msg_edit(id, cb_msg_id, 'Последние новости из мира игр на сегодня: \n' +
                        games_text, keyboards.listboard())

                elif states[id] in ["{'command': '1'}", "{'command': '2'}", "{'command': '3'}", "{'command': '4'}", "{'command': '5'}", "{'command': '6'}", "{'command': '7'}", "{'command': '8'}"]:
                    indx = int(states[id].split("'")[3]) - 1
                    if news_types[id] == 'internet':
                        header = news.headers_internet[indx]
                        desc = news.descs_internet[indx]
                        original = news.originals_internet[indx]
                    elif news_types[id] == 'gadgets':
                        header = news.headers_gadgets[indx]
                        desc = news.descs_gadgets[indx]
                        original = news.originals_gadgets[indx]
                    elif news_types[id] == 'games':
                        header = news.headers_games[indx]
                        desc = news.descs_games[indx]
                        original = news.originals_games[indx]
                    msg_edit(id, cb_msg_id, str(indx+1) + '&#8419; ' + header + '\n\n' + desc + '\n\nЧитать далее: ' + original, keyboards.listboard())

                elif states[id] == "{'command': 'back_news'}":
                    msg_edit(id, cb_msg_id,
'''Возвращаю Вас к выбору категории новостей. Выберите категорию: интернет, гаджеты или игры.
Данные взяты из news.yandex.ru''',
                        keyboards.news)
                    news_types[id] = ''

                elif states[id] == '{"command":"donate"}':
                    msg(id, 'Я очень хочу кушать. Я голодный... &#128546; Дайте, пожалуйста, пару долларов, чтобы мне купили пончик &#127849;',
                        keyboards.payboard('action=transfer-to-group&group_id=132868814&aid=10'))

                elif states[id] == '{"command":"unmail"}':
                    if id < 2*10**9:
                        mails[id] = False
                        msg(id, 'Я отписал Вас от рассылок команды PTCodding. Если вдруг захотите подписаться обратно — ниже есть кнопка «Подписаться на рассылки» &#128071;',
                            keyboards.menu(mails[id]))
                    else:
                        msg(id, 'Я отписал этот чат от рассылок команды PTCodding. Если вдруг захотите подписаться обратно — ниже есть кнопка «Подписаться на рассылки» &#128071;',
                            keyboards.conversation(mails[id]))

                elif states[id] == '{"command":"mail"}':
                    mails[id] = True
                    if id < 2*10**9:
                        msg(id, 'Я подписал Вас на рассылки команды PTCodding. Если вдруг захотите отписаться — ниже есть кнопка «Отписаться от рассылок» &#128071;',
                            keyboards.menu(mails[id]))
                    else:
                        msg(id, 'Я подписал этот чат на рассылки команды PTCodding. Если вдруг захотите отписаться — ниже есть кнопка «Отписаться от рассылок» &#128071;',
                            keyboards.conversation(mails[id]))

                # elif states[id] == '{"command":"partners"}':
                # 	msg(id, 'Добро пожаловать в список партнёров команды PTCodding! Благодаря этим людям в PTCodding очень многое изменяется. Я как чат-бот сообщества наблюдаю за всем этим со стороны — PTCodding растёт на глазах! &#128079;', keyboards.partner)

                # elif states[id] == '{"command":"sapod"}':
                # 	msg(id, '@sapod (SAPOD) — первый и единственный подкаст из мира San Andreas. \n\nВедущий подкаста Стич часто появляется и в подкастах от PTCodding. Вместе с Павлом они обсуждают новости уходящего месяца в IT-кухне и жарко спорят, кто лучше: iOS или Android &#128521;\n\nСлушайте Стича в его подкасте SAPOD — vk.com/sapod &#128072;')

                elif states[id] == '{"command":"back"}' and id < 2*10**9:
                    msg(id,
'''Возвращаю Вас в главное меню. Напоминаю назначение кнопок:

#news — последние новости из сферы IT
#partnership — партнёрство, сотрудничество, спонсорство
#market — магазин услуг и покупки
#team — вопросы к команде и о команде''',
                        keyboards.menu(mails[id]))
                    internet_text, gadgets_text, games_text = '', '', ''

                elif states[id] == '{"command":"back"}' and id > 2*10**9:
                    msg(id, 'Возвращаюсь в главное меню.', keyboards.conversation(mails[id]))
                    internet_text, gadgets_text, games_text = '', '', ''

                elif id > 2*10**9 and ('исчез' in text.lower() or 'убер' in text.lower() or 'убр' in text.lower() or 'скр' in text.lower() or 'пок' in text.lower() or 'св' in text.lower() or 'увид' in text.lower() or 'уй' in text.lower() or 'уш' in text.lower()):
                    msg(id, 'Если захотите, чтобы я снова появился — позовите меня по имени', keyboards.emptyboard())

                elif states[id] == '':
                    msg(id, 'Извините, я не понимаю Вас. Чтобы вернуться в главное меню, напишите «начать» или позовите меня по имени &#129335;')

            if id == admin_chat:
                if state_chat == '{"command":"cancel"}':
                    msg(admin_chat, 'Отменяю и исчезаю...')

                elif state_chat == 'sending request_id':
                    request_id = text
                    msg(admin_chat, 'А какую сумму нужно запросить? Отправьте число в ответ на это сообщение.')
                    state_chat = 'wait amount'

                elif state_chat == 'sending amount':
                    request_amount = text
                    msg(admin_chat, 'Какое описание к запросу? Отправьте текст в ответ на это сообщение.')
                    state_chat = 'wait description'

                elif state_chat == 'sending description':
                    try:
                        msg(request_id, 'Меня попросили запросить у Вас оплату для «{}» на сумму в ₽{}. Подтвердите оплату...'.format(text, request_amount),
                            keyboards.payboard('action=pay-to-group&amount={}&description={}&group_id=132868814&aid=10'.format(
                                               request_amount, urllib.parse.quote(text))))
                        msg(admin_chat, 'Запрос оплаты у [id{0}|{1} {2}] прошёл успешно!'.format(
                            request_id, name(request_id, 'gen')['first_name'], name(request_id, 'gen')['last_name']))
                    except Exception:
                        msg(admin_chat,
'''Возникла проблема при запросе оплаты у пользователя.

Загляните в консоль и повторите попытку: dashboard.heroku.com/apps/ptcodding-bot/logs''')
                        print(traceback.format_exc())

                elif state_chat == 'sending restart_id':
                    restart_ids = text.replace(' ', '').split(',')
                    for i in range(1, len(restart_ids)):
                        restart_ids[i] = int(restart_ids[i])
                        msg(restart_ids[i],
'''Здравстуйте, {}! Наш PTBot где-то сломался, но мы его починили. Приносим свои извинения.

С уважением, команда PTCodding.'''.format(name(restart_ids[i])['first_name']))
                        msg(restart_ids[i], 'Привет, это снова я, Ваш любимый PTBot! &#128075; Добро пожаловать в старое доброе меню! &#128526;',
                            keyboards.menu(mails[restart_ids[i]]))
                        msg(admin_chat, 'Баг-перезапуск для {} прошёл успешно!'.format(restart_ids[i]))

                elif state_chat == 'sending mail_text':
                    mail_text = text
                    mail_docs = parse_docs(attachments)
                    paste = 'вложением.' if not mail_text else 'текстом:'
                    msg(admin_chat,
'''Итак, я отправляю рассылку со следующим {}

{}

Подтвердите отправку или пропишите id через запятую с ключевыми словами «только» или «кроме».'''.format(
                        paste, mail_text), keyboards.cancel(), attach=mail_docs)
                    state_chat = 'wait mail_confirm'

                elif state_chat == 'sending mail_confirm':
                    text = text.split('\n')
                    only, exceptly = [], []
                    text.sort()
                    if len(text) == 1:
                        if text[0].split()[0].lower() == 'только':
                            for i in text[0].split(maxsplit=1)[1].replace(' ', '').split(','):
                                only.append(int(i))
                        elif text[0].split()[0].lower() == 'кроме':
                            for i in text[0].split(maxsplit=1)[1].replace(' ', '').split(','):
                                exceptly.append(int(i))
                    elif len(text) == 2:
                        for i in text[0].split(maxsplit=1)[1].replace(' ', '').split(','):
                            exceptly.append(int(i))
                        for i in text[1].split(maxsplit=1)[1].replace(' ', '').split(','):
                            only.append(int(i))

                    msg(admin_chat, 'Начинаю рассылку...')
                    dialog_ids = get_allow()
                    for i in dialog_ids:
                        if i not in mails:
                            mails[i] = dialog_ids[i]
                        if dialog_ids[i] and mails[i]:
                            try:
                                if i in set(only) - set(exceptly):
                                    msg(i, mail_text, attach=mail_docs)
                                elif not only and i not in exceptly:
                                    msg(i, mail_text, attach=mail_docs)
                                elif not only and not exceptly:
                                    msg(i, mail_text, attach=mail_docs)
                            except Exception:
                                pass

                    for i in mails:
                        if mails[i] and i not in dialog_ids:
                            try:
                                if i in set(only) - set(exceptly):
                                    msg(i, mail_text, attach=mail_docs)
                                elif not only and i not in exceptly:
                                    msg(i, mail_text, attach=mail_docs)
                                elif not only and not exceptly:
                                    msg(i, mail_text, attach=mail_docs)
                            except Exception:
                                pass
                    msg(admin_chat, 'Рассылка завершена!')

                elif 'анмут' in text.lower():
                    mute = list(set(mute) - set([int(i) for i in text.replace(' ', '').split(',')[2:]]))
                    paste = 'пуст' if not ', '.join(map(str, mute)) else ', '.join(map(str, mute))
                    msg(admin_chat,
'''Великая печать бана снята. Удачи спамерам! 😎
Список мутированных: ''' + paste + '.')

                elif 'мут' in text.lower():
                    mute += [int(i) for i in text.replace(' ', '').split(',')[2:]]
                    mute = list(set(mute))
                    msg(admin_chat,
'''На всех, кого вы написали, наложил великую печать бана! 😈
Список мутированных: ''' + ', '.join(map(str, mute)) + '.')

                elif 'vk pay' in text.lower() or 'vkpay' in text.lower():
                    msg(admin_chat, 'Решили запросить у кого-то деньги? У кого? Отправьте id пользователя в ответ на это сообщение.', keyboards.cancel())
                    state_chat = 'wait request_id'

                elif 'перезапуск' in text.lower():
                    msg(admin_chat, 'Решили перезапустить меня? У кого? Отправьте id пользователей через запятую.', keyboards.cancel())
                    state_chat = 'wait restart_id'

                elif 'рассылка' in text.lower():
                    msg(admin_chat, 'Какой текст рассылки отправляем пользователям? Отправьте сообщение в ответ на это и не забудьте про первую заглавную', keyboards.cancel())
                    state_chat = 'wait mail_text'

                elif 'консоль' in text.lower():
                    msg(admin_chat, 'Начинаю отправку...')
                    print('\nSTATES')
                    for id in states:
                        print(str(id) + '=' + str(states[id]))
                    print('\nNEWS_TYPES')
                    for id in news_types:
                        print(str(id) + '=' + str(news_types[id]))
                    print('\nMAILS')
                    for id in mails:
                        print(str(id) + '=' + str(int(mails[id])))
                    print('\nMUTE')
                    print(*mute, sep=',')
                    print('\nCARTS')
                    for id in keyboards.carts:
                        print(str(id) + '=' + str(keyboards.carts[id]))
                    msg(admin_chat, 'Все данные словарей states, news_types, mails, carts и списка mute были выведены в консоль!')

                elif 'помощь' in text.lower():
                    msg(admin_chat,
'''
Список команд:
- мут/анмут [числа через запятую] – отключает/включает оповещения о событиях от юзера
- vk pay/vkpay – активирует диалог запроса оплаты у юзера по id
- перезапуск – активирует диалог для перезапуска бота у юзеров по id
- рассылка – активирует диалог для создания и отправки рассылок
- консоль – выводит данные бота в консоль
- помощь – выводит этот список команд.

Не благодарите 😎
''')
        
        elif event.type == VkBotEventType.VKPAY_TRANSACTION:
            id = event.object.from_id
            domain = link(id)
            amount = event.object.amount * 1000
            if event.object.description:
                if sex(id) == 1:
                    msg(admin_chat,
'''#pay
@{0} ({1} {2}) перевела ₽{3} с комментарием «{4}»'''.format(
                        domain, name(id)['first_name'], name(id)['last_name'], amount / 1000000, text))
                else:
                    msg(admin_chat,
'''#pay
@{0} ({1} {2}) перевёл ₽{3} с комментарием «{4}»'''.format(
                        domain, name(id)['first_name'], name(id)['last_name'], amount / 1000000, text))
            else:
                if sex(id) == 1:
                    msg(admin_chat,
'''#pay
@{0} ({1} {2}) пожертвовала ₽{3}'''.format(
                        domain, name(id)['first_name'], name(id)['last_name'], amount / 1000000))
                else:
                    msg(admin_chat,
'''#pay
@{0} ({1} {2}) пожертвовал ₽{3}'''.format(
                        domain, name(id)['first_name'], name(id)['last_name'], amount / 1000000))
            msg(id, 'Большое спасибо за донат! 💙')

        elif event.type == VkBotEventType.MESSAGE_ALLOW:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1 and id not in mute:
                msg(admin_chat,
'''#open
&#128236; @{0} ({1} {2}) разрешила присылать сообщения.
Диалог с подписчиком: https://vk.com/gim132868814?sel={3}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], id))
            elif id not in mute:
                msg(admin_chat,
'''#open
&#128236; @{0} ({1} {2}) разрешил присылать сообщения.
Диалог с подписчиком: https://vk.com/gim132868814?sel={3}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], id))

        elif event.type == VkBotEventType.MESSAGE_DENY:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1 and id not in mute:
                msg(admin_chat,
'''#close
&#128234; @{0} ({1} {2}) запретила присылать сообщения.'''.format(
                    domain, name(id)['first_name'], name(id)['last_name']))
            elif id not in mute:
                msg(admin_chat,
'''#close
&#128234; @{0} ({1} {2}) запретил присылать сообщения.'''.format(
                    domain, name(id)['first_name'], name(id)['last_name']))

        elif event.type == VkBotEventType.GROUP_JOIN:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1 and id not in mute:
                msg(admin_chat,
'''#join
&#128150; @{0} ({1} {2}) вступила в PTCodding.'''.format(
                    domain, name(id)['first_name'], name(id)['last_name']))
            elif id not in mute:
                msg(admin_chat,
'''#join
&#128150; @{0} ({1} {2}) вступил в PTCodding.'''.format(
                    domain, name(id)['first_name'], name(id)['last_name']))

        elif event.type == VkBotEventType.GROUP_LEAVE:
            id = event.object.user_id
            domain = link(id)
            if event.object.self:
                if sex(id) == 1 and id not in mute:
                    msg(admin_chat,
'''#leave
&#128148; @{0} ({1} {2}) покинула PTCodding.'''.format(
                        domain, name(id)['first_name'], name(id)['last_name']))
                elif id not in mute:
                    msg(admin_chat,
'''#leave
&#128148; @{0} ({1} {2}) покинул PTCodding.'''.format(
                        domain, name(id)['first_name'], name(id)['last_name']))
            else:
                if sex(id) == 1:
                    msg(admin_chat,
'''#delete
&#128683; @{0} ({1} {2}) удалена из PTCodding.'''.format(
                        domain, name(id)['first_name'], name(id)['last_name']))
                else:
                    msg(admin_chat,
'''#delete
&#128683; @{0} ({1} {2}) удалён из PTCodding.'''.format(
                        domain, name(id)['first_name'], name(id)['last_name']))

        elif event.type == VkBotEventType.WALL_REPOST:
            id = event.object.from_id
            domain = link(id)
            wall_id = event.object.owner_id
            post_id = event.object.id
            if sex(id) == 1:
                msg(admin_chat,
'''#repost
&#128226; @{0} ({1} {2}) сделала репост записи из PTCodding.
Ссылка на запись: vk.com/wall{3}_{4}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], wall_id, post_id))
            else:
                msg(admin_chat,
'''#repost
&#128226; @{0} ({1} {2}) сделал репост записи из PTCodding.
Ссылка на запись: vk.com/wall{3}_{4}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], wall_id, post_id))

        elif event.type == VkBotEventType.WALL_REPLY_NEW:
            id = event.object.from_id
            domain = link(id)
            comment_id = event.object.id
            post_id = event.object.post_id
            owner_id = event.object.owner_id
            if sex(id) == 1 and id not in mute:
                msg(admin_chat,
'''#comment
&#128196; @{0} ({1} {2}) оставила комментарий к записи из PTCodding.
Ссылка на комментарий: vk.com/ptcodding?w=wall{3}_{4}_r{5}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], owner_id, post_id, comment_id))
            elif id not in mute:
                msg(admin_chat,
'''#comment
&#128196; @{0} ({1} {2}) оставил комментарий к записи из PTCodding.
Ссылка на комментарий: vk.com/ptcodding?w=wall{3}_{4}_r{5}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], owner_id, post_id, comment_id))

        elif event.type == VkBotEventType.BOARD_POST_NEW:
            id = event.object.from_id
            domain = link(id)
            comment_id = event.object.id
            topic_id = event.object.topic_id
            owner_id = event.object.topic_owner_id
            if sex(id) == 1 and id not in mute:
                msg(admin_chat,
'''#comment
&#128196; @{0} ({1} {2}) оставила комментарий в обсуждении PTCodding.
Ссылка на комментарий: vk.com/ptcodding?w=board{3}_{4}_?post={5}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], owner_id, topic_id, comment_id))
            elif id not in mute:
                msg(admin_chat,
'''#comment
&#128196; @{0} ({1} {2}) оставил комментарий в обсуждении PTCodding.
Ссылка на комментарий: vk.com/ptcodding?w=board{3}_{4}_?post={5}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], owner_id, topic_id, comment_id))

        elif event.type == VkBotEventType.MARKET_COMMENT_NEW:
            id = event.object.from_id
            domain = link(id)
            item_id = event.object.item_id
            market_id = event.object.market_owner_id
            if sex(id) == 1 and id not in mute:
                msg(admin_chat,
'''#comment
&#128196; @{0} ({1} {2}) оставила комментарий к товару PTCodding.
Ссылка на комментарий: vk.com/ptcodding?w=product{3}_{4}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], market_id, item_id))
            elif id not in mute:
                msg(admin_chat,
'''#comment
&#128196; @{0} ({1} {2}) оставил комментарий к товару PTCodding.
Ссылка на комментарий: vk.com/ptcodding?w=product{3}_{4}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], market_id, item_id))

        elif event.type == VkBotEventType.USER_UNBLOCK and event.object.by_end_date:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1:
                msg(admin_chat,
'''#unban
&#127379; @{0} ({1} {2}) удалена из чёрного списка PTCodding по истечении срока блокировки.'''.format(
                    domain, name(id)['first_name'], name(id)['last_name']))
            else:
                msg(admin_chat,
'''#unban
&#127379; @{0} ({1} {2}) удалён из чёрного списка PTCodding по истечении срока блокировки.'''.format(
                    domain, name(id)['first_name'], name(id)['last_name']))

        elif event.type == VkBotEventType.POLL_VOTE_NEW:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1 and id not in mute:
                msg(admin_chat,
'''#vote
&#128202; @{0} ({1} {2}) проголосовала в опросе по ссылке: vk.com/poll{3}_{4}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], event.object.owner_id, event.object.poll_id))
            elif id not in mute:
                msg(admin_chat,
'''#vote
&#128202; @{0} ({1} {2}) проголосовал в опросе по ссылке: vk.com/poll{3}_{4}'''.format(
                    domain, name(id)['first_name'], name(id)['last_name'], event.object.owner_id, event.object.poll_id))

        elif event.type == VkBotEventType.GROUP_OFFICERS_EDIT:
            id = event.object.admin_id
            domain = link(id)
            change_id = event.object.user_id
            change_domain = link(change_id)
            levels = {0: 'Нет полномочий', 1: 'Модератор', 2: 'Редактор', 3: 'Администратор'}
            level_old = levels[event.object.level_old]
            level_new = levels[event.object.level_new]
            msg(admin_chat,
'''#permission
&#127385; @{0} ({1} {2}) изменил полномочия участника команды PTCodding @{3} ({4} {5}) с «{6}» на «{7}»'''.format(
                domain, name(id)['first_name'], name(id)['last_name'], change_domain, name(change_id, 'gen')['first_name'], name(change_id, 'gen')['last_name'], level_old, level_new))

        elif event.type == VkBotEventType.GROUP_CHANGE_PHOTO:
            id = event.object.user_id
            domain = link(id)
            msg(admin_chat,
'''#photo
&#128444; @{0} ({1} {2}) изменил главную фотографию PTCodding'''.format(
                domain, name(id)['first_name'], name(id)['last_name']))

    except Exception:
        msg(165504240,
'''
PTBot споткнулся о событие «{0}» пользователя {1}!
Диалог с подписчиком: vk.com/gim132868814?sel={1}

Трейсбэк:
{2}

@pavetranquil (Павел), загляните в консоль и исправьте баг: dashboard.heroku.com/apps/ptcodding-bot/logs'''.format(
            event.type, id, '\n'.join(traceback.format_exc().split('\n')[1:])))
        print(traceback.format_exc())


while True:
    events = longpoll.check()
    if events:
        for event in events:
            main()
    elif time.time() - last_request >= 600:
        print('\nОбновляю новости...')
        news.refresh_internet()
        news.refresh_games()
        news.refresh_gadgets()
        print('Закончил!\n')
        last_request = time.time()
