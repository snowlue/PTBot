import keyboards, news
import urllib.parse, traceback, time
from methods import msg, name, link, sex, get_id, delete, isMember, parse_docs, get_allow, upload, read_data, VkBotEventType, longpoll

data = read_data()
states, news_types, mails, mute = data[0], data[1], data[2], data[3]
keyboards.carts = data[4]
payload, state_chat, id_chat = '', '', 2*10**9+6
internet_text, gadgets_text, games_text = '', '', ''
last_request = time.time()

print('main.py started!')

def main():
    global event, internet_text, gadgets_text, games_text, payload, state_chat, id_chat, states, news_types, mails, mute
    try:
        print('\nЛовлю события... Поймал {}'.format(event.type))
        if event.type == VkBotEventType.MESSAGE_NEW:
            id = event.object.peer_id
            text = event.object.text
            msg_id = event.object.id
            payload = event.object.payload
            attachments = event.object.attachments

            if id not in states:
                states[id] = ''
            if id not in news_types:
                news_types[id] = ''
            if id not in mails:
                mails[id] = True if id < 2*10**6 else False
            if id not in keyboards.carts:
                keyboards.carts[id] = []

            if id == id_chat:
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
                elif state_chat == 'wait mail_confirm' and payload != '{"command":"cancel"}}':
                    state_chat = 'sending mail_confirm'	
                else:
                    state_chat = payload
            else:
                if states[id] == 'wait idea' and text != 'Вернуться ↩':
                    states[id] = 'sending idea'
                elif states[id] == 'wait question' and text != 'Вернуться ↩':
                    states[id] = 'sending question'
                elif states[id] == 'wait partner' and text != 'Вернуться ↩':
                    states[id] = 'sending partner'
                else:
                    states[id] = payload
            try:
                if id < 2*10**9 and (states[id] == '{"command":"start"}' or 'нач' in text.lower().split()[0] or 'start' in text.lower().split()[0] or 'ptbot' in text.lower().split()[0] or 'поехали' in text.lower().split()[0] or 'появи' in text.lower().split()[0] or 'откр' in text.lower().split()[0] or 'эй' in text.lower().split()[0] or 'клавиатур' in text.lower().split()[0]) and states[id] not in ['sending idea', 'sending question', 'sending partner']: 
                    msg(id, 'Привет, я PTBot — дворецкий команды PTCodding. \nНажмите на нужную Вам кнопку, чтобы команда нашла Вас и быстро ответила, а я не потерял Вас &#128522; \n\n#news — последние новости из сферы IT \n#partnership — партнёрство, сотрудничество, спонсорство \n#market — магазин услуг и покупки \n#team — вопросы к команде и о команде', keyboards.menu(mails[id]))
                elif id > 2*10**9 and ('нач' in text.lower().split()[1] or 'start' in text.lower().split()[1] or 'ptbot' in text.lower().split()[1] or 'поехали' in text.lower().split()[1] or 'появи' in text.lower().split()[1] or 'откр' in text.lower().split()[1] or 'эй' in text.lower().split()[1] or 'клавиатур' in text.lower().split()[1]):
                    msg(id, 'Привет, я PTBot — чат-бот команды PTCodding. &#9995; С моей помощью вы можете узнать последние новости и задонатить на топовый функционал моим создателям — команде PTCodding. &#128176; Если вдруг я стану не нужен, напиши «скройся», «уберись», «исчезни», «пока» или что-нибудь в этом роде. &#128521;', keyboards.conversation(mails[id]))
            except Exception:
                pass


            print('{} отправляет сообщение с текстом "{}"'.format(id, text))

            if id != 2*10**9+6:
                if states[id] == '{"command":"partnership"}':
                    msg(id, 'Станьте партнёрами PTCodding! Отправьте заявку сюда, и моё начальство рассмотрит её в ближайшие сроки. Следуйте моим советам:\n1. Расскажите о себе, чем Вы занимаетесь, какую компанию или бренд представляете. \n2. Прикрепите к заявке ссылку на Ваш проект. \n3. Расскажите о целях сотрудничества, чего бы хотели добиться. \n4. Скажите, какую выгоду получит PTCodding от партнёрства с Вами. \n\nОтправьте сообщение — оно и станет заявкой на партнёрство!', keyboards.back())
                    states[id] = 'wait partner'

                elif states[id] == 'sending partner':
                    print('{} предлагает партнёрство'.format(id))
                    if id not in mute:
                        msg(id_chat, '#botpartner \n[id{0}|{1} {2}] предлагает партнёрство.\n\nОтветить пользователю: https://vk.com/gim132868814?sel={0}'.format(id, name(id)['first_name'], name(id)['last_name']), forward=str(msg_id))
                        msg(id, 'Ждите ответа! Скоро с Вами свяжутся мои операторы! &#8986;', keyboards.menu(mails[id]))



                elif states[id] == '{"command":"team"}':
                    msg(id, 'Здесь Вы сможете задать вопрос моему начальству, команде PTCodding, на абсолютно любую тему, какую только вздумается) &#128521;\nТакже можете почитать немного о команде: как появились они, как появился я, кто когда пришёл и какой вклад внёс &#128526;', keyboards.team)

                elif states[id] == '{"command":"question"}':
                    msg(id, "Какие-то вопросы? Пишите — команда ответит на всё! &#128170;", keyboards.back('team'))
                    states[id] = 'wait question'

                elif states[id] == 'sending question':
                    print('{} отправляет вопрос'.format(id))
                    if id not in mute:
                        msg(id_chat, '#botquestion \n[id{0}|{1} {2}] задаёт вопрос.\n\nОтветить пользователю: https://vk.com/gim132868814?sel={0}'.format(id, name(id)['first_name'], name(id)['last_name']), forward=str(msg_id))
                        msg(id, 'Ждите ответа на свой вопрос от команды PTCodding! &#8986;', keyboards.team)

                elif states[id] == '{"command":"about"}':
                    msg(id, 'PTCodding появился 11 ноября 2016 года. За период с момента создания до 1 сентября 2018 года было сделано много крупных проектов: текстовая игра «Кто хочет стать миллионером?», «Мы — люди этой Земли!» и другие. \nА уже с 1 сентября начался активный прирост подписчиков, команда начала работать над медиа и активно развивалась в этом направлении. Был опубликован промо-ролик о митапе VK×Junction, 11 ноября на своё двухлетие PTCodding выпустил первый выпуск подкаста «Взгляд в неделю». \n2 февраля 2019 года PTCodding переехал на платформу подкастов ВКонтакте и начал активно распространяться на других. С марта по май в PTCodding публиковался экспериментальный подкаст «Игродайджест». В мае появился подкаст «IT-кухня». \n\nСейчас PTCodding — узнаваемый бренд, известный как команда молодых энтузиастов, которые делают качественный и уникальный IT-контент. Они записывают подкасты, пишут лонгриды, делают музыкальные подборки, популяризуя программирование и IT-технологии в массы. !\n\nВы можете подробнее почитать о каждом участнике команды ниже, нажав на кнопку с именем участника! &#128071;', keyboards.about)

                elif states[id] == '{"command":"Pavel"}':
                    msg(id, 'Павел — основатель PTCodding. Именно под его началом были созданы многие код-проекты, концепт и окружение бренда. Павел является шеф-редактором на платформе лонгридов, шеф-кодером в команде программистов. Думает над дальнейшим продвижением и мыслит неординарно, чтобы PTCodding становился лучше для своих слушателей и читателей. Одним из крупнейших проектов Павла являюсь я — PTBot, чат-бот PTCodding!')

                elif states[id] == '{"command":"Bogdan"}':
                    msg(id, 'Богдан — дизайнер PTCodding. Присоединился к команде 14 сентября 2017 года. Под его началом были сделаны все аватарки, шапки сообщества и обложки к лонгридам. Окружение бренда, дизайн и визуалка были сделаны его руками. Является соведущим подкаста «IT-кухня», некоторое время вёл рубрику «Бюдгаджет месяца». Одним из последних проектов стал редизайн товаров в магазине PTCodding.')

                elif states[id] == '{"command":"Dima"}':
                    msg(id, 'Дима — генератор идей команды PTCodding, главный редактор. Присоединился к команде 5 мая 2020 года. Нарисовал характеристики к «Бюдгаджету месяца». Ищет новых партнёров и достойных людей для сотрудничества и работы с командой PTCodding.')

                elif states[id] == '{"command":"back_team"}':
                    msg(id, 'Возвращаю Вас в меню команды.', keyboards.team)



                elif states[id] == '{"command":"buy"}':
                    msg(id, 'В разделе покупок Вы можете приобрести у нас виртуальные услуги и услуги на дом — рекламу, программирование и дизайн от моего начальства, звукозапись и ремонт Вашего ПК или Android-смартфона. &#128230; \nЕщё если Вы вдруг потеряетесь, то всегда можете заглянуть в привычную корзину и магазин от ВКонтакте))) &#128071;', keyboards.buy)

                elif states[id] == '{"command":"code"}':
                    msg(id, 'Цена: от 200 руб. &#128181; \n\nМоё начальство напишет чат-бота ВКонтакте или в Telegram под Ваши цели и по Вашим требованиям. Ваши данные: описание функционала и ключевых целей и задач чат-бота, сгенерированный longpoll-токен. \nХочу предупредить Вас: если Вам не понравился чат-бот, есть какие-то проблемы, ошибки, баги, то необходимо сразу же сообщить об этом. Любые недочёты исправляются одним нажатием клавиши. \nВ чат-боте прописан его создатель, с указанием авторства на сообщество PTCodding. Просьбы вернуть деньги после того, как Вы установили чат-бота в своё сообщество, не принимаются. \nЦена может изменяться в зависимости от срока заказа, указана минимальная цена! Также могут появляться специальные условия! \n\n[vk.com/ptcodding?w=product-132868814_2055522|А ещё товар есть в магазине ВКонтакте] &#128072;', keyboards.itemboard('code'))
                elif states[id] == '{"command":"add_code"}':
                    if 'Создание чат-бота.code' not in keyboards.carts[id]:
                        msg(id, 'Товар добавлен в Вашу корзину.', keyboards.cartboard(id, 'Создание чат-бота.code'))
                    else:
                        msg(id, 'Товар уже в корзине.', keyboards.cartboard(id))
                elif states[id] == '{"command":"delete_code"}':
                    msg(id, 'Товар удалён из Вашей корзины.', keyboards.cartboard(id, 'Создание чат-бота.code'))

                elif states[id] == '{"command":"design"}':
                    msg(id, 'Цена: от 200 руб. &#128181; \n\nМоё начальство создаст дизайн Вашему бренду по Вашим требованиям. Ваши данные: название бренда, для которого делается дизайн, стиль исполнения. \nХочу предупредить Вас: если Вам не понравился какой-то элемент дизайна, то ему необходимо сразу написать об этом. Любые недочёты исправляются одним нажатием клавиши. \nНа весь пак дизайна, до оплаты заказа, будет нанесён водяной знак. Просьбы вернуть деньги после того, как Вы оплатили заказ и пак был передан без водяных знаков, не принимаются. \nЦена может изменяться в зависимости от срока заказа и техники выполнения, указана минимальная цена! Также могут появляться специальные условия! \n\n[vk.com/ptcodding?w=product-132868814_2064351|А ещё товар есть в магазине ВКонтакте]. &#128072;', keyboards.itemboard('design'))
                elif states[id] == '{"command":"add_design"}':
                    if 'Создание дизайна.design' not in keyboards.carts[id]:
                        msg(id, 'Товар добавлен в Вашу корзину.', keyboards.cartboard(id, 'Создание дизайна.design'))
                    else:
                        msg(id, 'Товар уже в корзине.', keyboards.cartboard(id))
                elif states[id] == '{"command":"delete_design"}':
                    msg(id, 'Товар удалён из Вашей корзины.', keyboards.cartboard(id, 'Создание дизайна.design'))

                elif states[id] == '{"command":"record"}':
                    msg(id, 'Цена: от 750 руб. &#128181; \n\nМоё начальство запишет Ваш голос на своей домашней студии, обработает звук и отправит исходники в mp3, wav или другом формате на флешку, ВКонтакте или в облако. \nПри заказе дополнительно сведения, мастеринга или же при полноценной запись под ключ цена оговаривается при оформлении заказа. \nХочу предупредить Вас: на весь звуковой файл накладывается демо-фраза до оплаты заказа. Просьбы вернуть деньги после того, как Вы оплатили заказ и файл был передан без демо-фразы, не принимаются. \nЦена может изменяться в зависимости от срока заказа и дополнительных услуг, указана минимальная цена! Для клиентов могут появляться специальные условия! \n\n[vk.com/ptcodding?w=product-132868814_2561900|А ещё товар есть в магазине ВКонтакте]. &#128072;', keyboards.itemboard('record'))
                elif states[id] == '{"command":"add_record"}':
                    if 'Звукозапись.record' not in keyboards.carts[id]:
                        msg(id, 'Товар добавлен в Вашу корзину.', keyboards.cartboard(id, 'Звукозапись.record'))
                    else:
                        msg(id, 'Товар уже в корзине.', keyboards.cartboard(id))
                elif states[id] == '{"command":"delete_record"}':
                    msg(id, 'Товар удалён из Вашей корзины.', keyboards.cartboard(id, 'Звукозапись.record'))

                elif states[id] == '{"command":"fix"}':
                    msg(id, 'Цена: от 500 руб. &#128181; \n\nМоё начальство также работает с компьютерами и смартфонами: исправляет мелкие неполадки в работе, устанавливает лицензированный Microsoft Office или иное ПО, устанавливают активированную Windows, перепрошивают Android-смартфоны. \nХочу предупредить Вас: проверяйте работоспособность ПО, ПК или смартфона в целом сразу перед оплатой заказа. PTCodding даёт бесплатную гарантию — 1 месяц. Далее гарантия продлевается платно. \nЦена может изменяться в зависимости от срока заказа, указана минимальная цена! Для клиентов могут появляться специальные условия! \n\n[vk.com/ptcodding?w=product-132868814_2561901|А ещё товар есть в магазине ВКонтакте]. &#128072;', keyboards.itemboard('fix'))
                elif states[id] == '{"command":"add_fix"}':
                    if 'ПК и смартфоны.fix' not in keyboards.carts[id]:
                        msg(id, 'Товар добавлен в Вашу корзину.', keyboards.cartboard(id, 'ПК и смартфоны.fix'))
                    else:
                        msg(id, 'Товар уже в корзине.', keyboards.cartboard(id))
                elif states[id] == '{"command":"delete_fix"}':
                    msg(id, 'Товар удалён из Вашей корзины.', keyboards.cartboard(id, 'ПК и смартфоны.fix'))

                elif states[id] == '{"command":"cart"}':
                    msg(id, 'Корзина товаров, которые Вы добавили к заказу. \nТовары удаляются из корзины при нажатии на них. Если Вы добавили в корзину какие-то товары, то будет доступна кнопка оформления заказа — нажмите на неё, и с Вами в этом чате свяжутся мои операторы, которые обсудят все условия и цены &#128222;', keyboards.cartboard(id))
                        
                elif states[id] == '{"command":"cart_ui"}':
                    msg(id, 'Загляните в привычный магазин, если мой Вам оказался не по душе: vk.com/market-132868814 &#128072;')

                elif states[id] == '{"command":"order"}':
                    print('{} оформляет заказ.'.format(id))
                    if id not in mute:
                        msg(id_chat, '#order \nВас вызывают для оформления заказа. Пройдите, пожалуйста, по этой ссылке: https://vk.com/gim132868814?sel={}'.format(id))
                        keyboards.carts[id] = []
                        msg(id, 'Ожидайте... Скоро мои операторы свяжутся с Вами для уточнения деталей и оплаты заказа! &#8986;', keyboards.cartboard(id))
                
                elif states[id] == '{"command":"back_buy"}':
                    msg(id, 'Возвращаю Вас в меню товаров.', keyboards.buy)



                elif states[id] == '{"command":"news"}':
                    msg(id, 'Самый востребованный раздел PTBot — новости из мира IT прямо в этом чате! 😱💻 \nВыберите категорию: интернет, гаджеты или игры — и читайте топ-8 новостей!\n\nОбновление каждые 10 минут.\nДанные взяты из news.yandex.ru', keyboards.news, parse=False)

                elif states[id] == '{"command":"news_internet"}':
                    news_types[id] = 'internet'
                    if not internet_text:
                        for i in range(0, 8):
                            internet_text += str(i+1) + '&#8419; ' + news.headers_internet[i] + '\n'
                    msg(id, 'Последние новости из мира интернета на сегодня: \n' + internet_text, keyboards.listboard())		

                elif states[id] == '{"command":"news_gadgets"}':
                    news_types[id] = 'gadgets'
                    if not gadgets_text:
                        for i in range(0, 8):
                            gadgets_text += str(i+1) + '&#8419; ' + news.headers_gadgets[i] + '\n'
                    msg(id, 'Последние новости из мира гаджетов на сегодня: \n' + gadgets_text, keyboards.listboard())

                elif states[id] == '{"command":"news_games"}':
                    news_types[id] = 'games'
                    if not games_text:
                        for i in range(0, 8):
                            games_text += str(i+1) + '&#8419; ' + news.headers_games[i] + '\n'
                    msg(id, 'Последние новости из мира игр на сегодня: \n' + games_text, keyboards.listboard())

                elif states[id] in ['{"command":"1"}', '{"command":"2"}', '{"command":"3"}', '{"command":"4"}', '{"command":"5"}', '{"command":"6"}', '{"command":"7"}', '{"command":"8"}']:
                    indx = int(states[id].split('"')[3]) - 1
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
                    msg(id, header + '\n\n' + desc + '\n\nЧитать далее: ' + original)
                    

                elif states[id] == '{"command":"back_news"}':
                    msg(id, 'Возвращаю Вас к выбору категории новостей. Выберите категорию: интернет, гаджеты или игры. \n\nДанные взяты из news.yandex.ru', keyboards.news)
                    news_types[id] = ''



                elif states[id] == '{"command":"donate"}':
                    msg(id, 'Я очень хочу кушать. Я голодный... &#128546; Дайте, пожалуйста, пару долларов, чтобы мне купили пончик &#127849;', keyboards.payboard('action=transfer-to-group&group_id=132868814&aid=10'))



                elif states[id] == '{"command":"unmail"}':
                    if id < 2*10**9:
                        mails[id] = False
                        msg(id, 'Я отписал Вас от рассылок команды PTCodding. Если вдруг захотите подписаться обратно — ниже есть кнопка «Подписаться на рассылки» &#128071;', keyboards.menu(mails[id]))
                    else:
                        msg(id, 'Я отписал этот чат от рассылок команды PTCodding. Если вдруг захотите подписаться обратно — ниже есть кнопка «Подписаться на рассылки» &#128071;', keyboards.conversation(mails[id]))

                elif states[id] == '{"command":"mail"}':
                    mails[id] = True
                    if id < 2*10**9:
                        msg(id, 'Я подписал Вас на рассылки команды PTCodding. Если вдруг захотите отписаться — ниже есть кнопка «Отписаться от рассылок» &#128071;', keyboards.menu(mails[id]))
                    else:
                        msg(id, 'Я подписал этот чат на рассылки команды PTCodding. Если вдруг захотите отписаться — ниже есть кнопка «Отписаться от рассылок» &#128071;', keyboards.conversation(mails[id]))


                
                # elif states[id] == '{"command":"partners"}':
                # 	msg(id, 'Добро пожаловать в список партнёров команды PTCodding! Благодаря этим людям в PTCodding очень многое изменяется. Я как чат-бот сообщества наблюдаю за всем этим со стороны — PTCodding растёт на глазах! &#128079;', keyboards.partner)
                # 	msg(id, 'Добро пожаловать в список партнёров команды PTCodding! Партнёров совсем не осталось, но вы можете стать первым в этом списке — нажмите на #partnership и будьте вместе с нами! &#128079;', keyboards.partner)
                    
                
                # elif states[id] == '{"command":"sapod"}':
                # 	msg(id, '@sapod (SAPOD) — первый и единственный подкаст из мира San Andreas. \n\nВедущий подкаста Стич часто появляется и в подкастах от PTCodding. Вместе с Павлом они обсуждают новости уходящего месяца в IT-кухне и жарко спорят, кто лучше: iOS или Android &#128521;\n\nСлушайте Стича в его подкасте SAPOD — vk.com/sapod &#128072;')
                


                elif states[id] == '{"command":"back"}' and id < 2*10**9:
                    msg(id, 'Возвращаю Вас в главное меню. Напоминаю назначение кнопок: \n\n#news — последние новости из сферы IT \n#partnership — партнёрство, сотрудничество, спонсорство \n#market — магазин услуг и покупки \n#team — вопросы к команде и о команде', keyboards.menu(mails[id]))
                    internet_text, gadgets_text, games_text = '', '', ''
                
                elif states[id] == '{"command":"back"}' and id > 2*10**9:
                    msg(id, 'Возвращаю Вас в главное меню.', keyboards.conversation(mails[id]))
                    internet_text, gadgets_text, games_text = '', '', ''

                elif id > 2*10**9 and ('исчезн' in text.lower() or 'убер' in text.lower() or 'убр' in text.lower() or 'скр' in text.lower() or 'пок' in text.lower() or 'св' in text.lower() or 'увид' in text.lower() or 'уй' in text.lower() or 'уш' in text.lower()):
                    msg(id, 'Если захотите, чтобы я снова появился — позовите меня по имени', keyboards.emptyboard())
                
                elif states[id] == '':
                    msg(id, 'Извините, я не понимаю Вас. Чтобы вернуться в главное меню, напишите «начать» или позовите меня по имени &#129335;')




            if id == id_chat:
                if state_chat == '{"command":"cancel"}':
                    msg(id_chat, 'Отменяю и исчезаю...')

                elif state_chat == 'sending request_id':
                    request_id = text.split()[1]
                    msg(id_chat, 'А какую сумму нужно запросить? Отправьте число.')
                    state_chat = 'wait amount'

                elif state_chat == 'sending amount':
                    request_amount = text.split()[1]
                    msg(id_chat, 'Какое описание к запросу? Отправьте текст.')
                    state_chat = 'wait description'

                elif state_chat == 'sending description':
                    request_desc = ' '.join(text.split()[1:])
                    try:
                        msg(request_id, 'Меня попросили запросить у Вас оплату для «{}» на сумму в ₽{}. Подтвердите оплату...'.format(request_desc, request_amount), keyboards.payboard('action=pay-to-group&amount={}&description={}&group_id=132868814&aid=10'.format(request_amount, urllib.parse.quote(request_desc))))
                        msg(id_chat, 'Запрос оплаты у [id{0}|{1} {2}] прошёл успешно!'.format(request_id, name(request_id, 'gen')['first_name'], name(request_id, 'gen')['last_name']))
                    except Exception as err:
                        msg(id_chat, 'Возникла проблема при запросе оплаты у пользователя. \n\nЗагляните в консоль и повторите попытку: dashboard.heroku.com/apps/ptcodding-bot/logs')
                        print(err)
                        print(traceback.format_exc())


                elif state_chat == 'sending restart_id':
                    restart_ids = text.replace(' ', '')
                    restart_ids = restart_ids.split(',')
                    for i in range(1, len(restart_ids)):
                        restart_ids[i] =  int(restart_ids[i])
                        msg(restart_ids[i], 'Здравстуйте, {}! Наш PTBot где-то сломался, но мы его починили. Приносим свои извинения.\n\nС уважением, команда PTCodding.'.format(name(restart_ids[i])['first_name']))
                        msg(restart_ids[i], 'Привет, это снова я, Ваш любимый PTBot! &#128075; Добро пожаловать в старое доброе меню! &#128526;', keyboards.menu(mails[restart_ids[i]]))
                        msg(id_chat, 'Баг-перезапуск прошёл успешно!')


                elif state_chat == 'sending mail_text':
                    mail_text = text
                    docs = parse_docs(attachments)
                    msg(id_chat, 'Итак, я отправляю рассылку со следующим текстом:\n\n{}\n\nПодтвердите отправку или пропишите id через запятую с ключевыми словами «только» или «кроме».'.format(mail_text), attach=docs)
                    state_chat = 'wait mail_confirm'
                
                elif state_chat == 'sending mail_confirm':
                    text = text.split('\n')
                    only, exceptly = [], []
                    text.sort()
                    if len(text) == 1:
                        if text[0].split()[0].lower() == 'только':
                            for i in text[0].split()[1].replace(' ', '').split(','):
                                only.append(int(i))
                        elif text[0].split()[0].lower() == 'кроме':
                            for i in text[0].split()[1].replace(' ', '').split(','):
                                exceptly.append(int(i))
                    elif len(text) == 2:
                        for i in text[0].split(maxsplit=1)[1].replace(' ', '').split(','):
                            exceptly.append(int(i))
                        for i in text[1].split(maxsplit=1)[1].replace(' ', '').split(','):
                            only.append(int(i))

                    msg(id_chat, 'Начинаю рассылку...')
                    dialog_ids = get_allow()
                    for i in dialog_ids:
                        if i not in mails:
                            mails[i] = dialog_ids[i]
                        if dialog_ids[i] and mails[i]:
                            if i in set(only) - set(exceptly):
                                msg(i, mail_text, attach=docs)
                            elif not only and i not in exceptly:
                                msg(i, mail_text, attach=docs)
                            elif not only and not exceptly:
                                msg(i, mail_text, attach=docs)

                    for i in mails:
                        if mails[i] and i not in dialog_ids:
                            try:
                                if i in set(only) - set(exceptly):
                                    msg(i, mail_text, attach=docs)
                                elif not only and i not in exceptly:
                                    msg(i, mail_text, attach=docs)
                                elif not only and not exceptly:
                                    msg(i, mail_text, attach=docs)
                            except Exception:
                                pass
                    msg(id_chat, 'Рассылка завершена!')

                
                elif 'анмут' in text:
                    mute = list(set(mute) - set([int(i) for i in text.split()[2:]]))
                    paste = 'пуст' if not ', '.join(map(str, mute)) else ', '.join(map(str, mute))
                    msg(id_chat, 'Великая печать бана снята. Удачи спамерам! 😎\nСписок мутированных: ' + paste)

                elif 'мут' in text:
                    mute += [int(i) for i in text.split()[2:]]
                    msg(id_chat, 'На всех, кого вы написали, наложил великую печать бана! 😈\nСписок мутированных: ' + ', '.join(map(str, mute)))

                elif 'vk pay' in text:
                    msg(id_chat, 'Решили запросить у кого-то деньги? У кого? Отправьте id пользователя.', keyboards.cancel())
                    state_chat = 'wait request_id'
                        
                elif 'перезапуск' in text:
                    msg(id_chat, 'Решили перезапустить меня? У кого? Отправьте id пользователей через запятую.', keyboards.cancel())
                    state_chat = 'wait restart_id'

                elif 'рассылка' in text:
                    msg(id_chat, 'Какой текст рассылки отправляем пользователям? Отправьте сообщение в ответ на это и не забудьте про первую заглавную', keyboards.cancel())
                    state_chat = 'wait mail_text'

                elif 'консоль' in text:
                    msg(id_chat, 'Начинаю отправку...')
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
                    msg(id_chat, 'Все данные словарей states, news_types, mails, carts и списка mute были выведены в консоль!')



        elif event.type == VkBotEventType.VKPAY_TRANSACTION:
            id = event.object.from_id
            domain = link(id)
            amount = event.object.amount * 1000
            if event.object.description:
                if sex(id) == 1:
                    msg(id_chat, '#pay\n@{0} ({1} {2}) перевела ₽{3} с комментарием «{4}»'.format(domain, name(id)['first_name'], name(id)['last_name'], amount / 1000000, text))
                else:
                    msg(id_chat, '#pay\n@{0} ({1} {2}) перевёл ₽{3} с комментарием «{4}»'.format(domain, name(id)['first_name'], name(id)['last_name'], amount / 1000000, text))
            else:
                if sex(id) == 1:
                    msg(id_chat, '#pay\n@{0} ({1} {2}) пожертвовала ₽{3}'.format(domain, name(id)['first_name'], name(id)['last_name'], amount / 1000000))
                else:
                    msg(id_chat, '#pay\n@{0} ({1} {2}) пожертвовал ₽{3}'.format(domain, name(id)['first_name'], name(id)['last_name'], amount / 1000000))
            msg(id, 'Большое спасибо за донат! 💙')


        elif event.type == VkBotEventType.MESSAGE_ALLOW:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1 and id not in mute:
                msg(id_chat, '#open\n&#128236; @{0} ({1} {2}) разрешила присылать сообщения. \nДиалог с подписчиком: https://vk.com/gim132868814?sel={3}'.format(domain, name(id)['first_name'], name(id)['last_name'], id))
            elif id not in mute:
                msg(id_chat, '#open\n&#128236; @{0} ({1} {2}) разрешил присылать сообщения. \nДиалог с подписчиком: https://vk.com/gim132868814?sel={3}'.format(domain, name(id)['first_name'], name(id)['last_name'], id))
        

        elif event.type == VkBotEventType.MESSAGE_DENY:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1 and id not in mute:
                msg(id_chat, '#close\n&#128234; @{0} ({1} {2}) запретила присылать сообщения.'.format(domain, name(id)['first_name'], name(id)['last_name']))
            elif id not in mute:
                msg(id_chat, '#close\n&#128234; @{0} ({1} {2}) запретил присылать сообщения.'.format(domain, name(id)['first_name'], name(id)['last_name']))


        elif event.type == VkBotEventType.GROUP_JOIN:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1 and id not in mute:
                msg(id_chat, '#join\n&#128150; @{0} ({1} {2}) вступила в PTCodding.'.format(domain, name(id)['first_name'], name(id)['last_name']))
            elif id not in mute:
                msg(id_chat, '#join\n&#128150; @{0} ({1} {2}) вступил в PTCodding.'.format(domain, name(id)['first_name'], name(id)['last_name']))


        elif event.type == VkBotEventType.GROUP_LEAVE:
            id = event.object.user_id
            domain = link(id)
            if event.object.self:
                if sex(id) == 1 and id not in mute:
                    msg(id_chat, '#leave\n&#128148; @{0} ({1} {2}) покинула PTCodding.'.format(domain, name(id)['first_name'], name(id)['last_name']))
                elif id not in mute:
                    msg(id_chat, '#leave\n&#128148; @{0} ({1} {2}) покинул PTCodding.'.format(domain, name(id)['first_name'], name(id)['last_name']))
            else:
                if sex(id) == 1:
                    msg(id_chat, '#delete\n&#128683; @{0} ({1} {2}) удалена из PTCodding.'.format(domain, name(id)['first_name'], name(id)['last_name']))
                else:
                    msg(id_chat, '#delete\n&#128683; @{0} ({1} {2}) удалён из PTCodding.'.format(domain, name(id)['first_name'], name(id)['last_name']))


        elif event.type == VkBotEventType.WALL_REPOST:
            id = event.object.from_id
            domain = link(id)
            wall_id = event.object.owner_id
            post_id = event.object.id
            if sex(id) == 1:
                msg(id_chat, '#repost\n&#128226; @{0} ({1} {2}) сделала репост записи из PTCodding. \nСсылка на запись: vk.com/wall{3}_{4}'.format(domain, name(id)['first_name'], name(id)['last_name'], wall_id, post_id))
            else:
                msg(id_chat, '#repost\n&#128226; @{0} ({1} {2}) сделал репост записи из PTCodding. \nСсылка на запись: vk.com/wall{3}_{4}'.format(domain, name(id)['first_name'], name(id)['last_name'], wall_id, post_id))
        

        elif event.type == VkBotEventType.WALL_REPLY_NEW:
            id = event.object.from_id
            domain = link(id)
            comment_id = event.object.id
            post_id = event.object.post_id
            owner_id = event.object.owner_id
            if sex(id) == 1 and id not in mute:
                msg(id_chat, '#comment\n&#128196; @{0} ({1} {2}) оставила комментарий к записи из PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=wall{3}_{4}_r{5}'.format(domain, name(id)['first_name'], name(id)['last_name'], owner_id, post_id, comment_id))
            elif id not in mute:
                msg(id_chat, '#comment\n&#128196; @{0} ({1} {2}) оставил комментарий к записи из PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=wall{3}_{4}_r{5}'.format(domain, name(id)['first_name'], name(id)['last_name'], owner_id, post_id, comment_id))


        elif event.type == VkBotEventType.BOARD_POST_NEW:
            id = event.object.from_id
            domain = link(id)
            comment_id = event.object.id
            topic_id = event.object.topic_id
            owner_id = event.object.topic_owner_id
            if sex(id) == 1 and id not in mute:
                msg(id_chat, '#comment\n&#128196; @{0} ({1} {2}) оставила комментарий в обсуждении PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=board{3}_{4}_?post={5}'.format(id, name(id)['first_name'], name(id)['last_name'], owner_id, topic_id, comment_id))
            elif id not in mute:
                msg(id_chat, '#comment\n&#128196; @{0} ({1} {2}) оставил комментарий в обсуждении PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=board{3}_{4}_?post={5}'.format(id, name(id)['first_name'], name(id)['last_name'], owner_id, topic_id, comment_id))


        elif event.type == VkBotEventType.MARKET_COMMENT_NEW:
            id = event.object.from_id
            domain = link(id)
            item_id = event.object.item_id
            market_id = event.object.market_owner_id
            if sex(id) == 1 and id not in mute:
                msg(id_chat, '#comment\n&#128196; @{0} ({1} {2}) оставила комментарий к товару PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=product{3}_{4}'.format(domain, name(id)['first_name'], name(id)['last_name'], market_id, item_id))
            elif id not in mute:
                msg(id_chat, '#comment\n&#128196; @{0} ({1} {2}) оставил комментарий к товару PTCodding. \nСсылка на комментарий: vk.com/ptcodding?w=product{3}_{4}'.format(domain, name(id)['first_name'], name(id)['last_name'], market_id, item_id))


        elif event.type == VkBotEventType.USER_UNBLOCK and event.object.by_end_date:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1:
                msg(id_chat, '#unban\n&#127379; @{0} ({1} {2}) удалена из чёрного списка PTCodding по истечении срока блокировки.'.format(domain, name(id)['first_name'], name(id)['last_name']))
            else:
                msg(id_chat, '#unban\n&#127379; @{0} ({1} {2}) удалён из чёрного списка PTCodding по истечении срока блокировки.'.format(domain, name(id)['first_name'], name(id)['last_name']))


        elif event.type == VkBotEventType.POLL_VOTE_NEW:
            id = event.object.user_id
            domain = link(id)
            if sex(id) == 1 and id not in mute:
                msg(id_chat, '#vote\n&#128202; @{0} ({1} {2}) проголосовала в опросе по ссылке: vk.com/poll{3}_{4}'.format(domain, name(id)['first_name'], name(id)['last_name'], event.object.owner_id, event.object.poll_id))
            elif id not in mute:
                msg(id_chat, '#vote\n&#128202; @{0} ({1} {2}) проголосовал в опросе по ссылке: vk.com/poll{3}_{4}'.format(id, name(id)['first_name'], name(id)['last_name'], event.object.owner_id, event.object.poll_id))


        elif event.type == VkBotEventType.GROUP_OFFICERS_EDIT:
            id = event.object.admin_id
            domain = link(id)
            change_id = event.object.user_id
            change_domain = link(change_id)
            levels = {0: 'Нет полномочий', 1: 'Модератор', 2: 'Редактор', 3: 'Администратор'}
            level_old = levels[event.object.level_old]
            level_new = levels[event.object.level_new]
            msg(id_chat, '#permission\n&#127385; @{0} ({1} {2}) изменил полномочия участника команды PTCodding @{3} ({4} {5}) с «{6}» на «{7}»'.format(domain, name(id)['first_name'], name(id)['last_name'], change_domain, name(change_id, 'gen')['first_name'], name(change_id, 'gen')['last_name'], level_old, level_new))


        elif event.type == VkBotEventType.GROUP_CHANGE_PHOTO:
            id = event.object.user_id
            domain = link(id)
            msg(id_chat, '#photo\n&#128444; @{0} ({1} {2}) изменил главную фотографию PTCodding'.format(domain, name(id)['first_name'], name(id)['last_name']))

    except Exception as err:
        msg(id_chat, '#log\nPTBot споткнулся о событие «{}» пользователя {}!\n\nТрейсбэк:\n{}\n\n@pavetranquil (Павел), загляните в консоль и исправьте баг: dashboard.heroku.com/apps/ptcodding-bot/logs'.format(event.type, id, '\n'.join(traceback.format_exc().split('\n')[1:])))
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
