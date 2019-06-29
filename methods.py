import vk_api, random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def msg(id, message='', board=[], forward='', parse=True):
	if board:
		vk.messages.send(peer_id=id, random_id=random.randint(-2147483648, 2147483647), message=message, forward_messages=forward, keyboard=board, dont_parse_links=not parse)
		
	else:
		vk_session.method('messages.send', {'peer_id': id, 'random_id': random.randint(-2147483648, 2147483647), 'message': message, 'forward_messages': forward, 'keyboard': board, 'dont_parse_links': not parse})
	print('Сообщение для {} отправлено'.format(id))

def name(id, case='nom'):
	return vk.users.get(user_ids=id, fields='first_name, last_name', name_case=case)[0]

def sex(id):
	return vk.users.get(user_ids=id, fields='sex')[0]['sex']

def get_id(id, offset=1):
	return vk.messages.getHistory(offset=offset, count=1, user_id=id)['items'][0]['id']

def delete(msg_id):
	vk.messages.delete(message_ids=msg_id, delete_for_all=True)

def online():
	vk.groups.enableOnline(group_id=132868814)

def isMember(group, id):
	return vk.groups.isMember(group_id=group, user_id=id)

def get_allow():
	allow_dict, chats_arr, offset = dict(), True, 0
	while chats_arr:
		chats_arr = vk.messages.getConversations(offset=offset, count=200)['items']
		for i in chats_arr:
			allow_dict[i['conversation']['peer']['id']] = i['conversation']['can_write']['allowed']
		offset += 200
	return allow_dict

def read_data():
	is_states, is_news, is_mails, is_carts = False, False, False, False
	states, news_types, mails, carts = dict(), dict(), dict(), dict()
	with open('data.txt', encoding='ascii') as file:
		line = file.readline()
		if line == 'STATES\n':
			while line != 'NEWS_TYPES\n':
				line = file.readline()
				if '=' in line:
					states[int(line.split('=')[0])] = line.split('=')[1].split('\n')[0]
			while line != 'MAILS\n':
				line = file.readline()
				if '=' in line:
					news_types[int(line.split('=')[0])] = line.split('=')[1].split('\n')[0]
			while line != 'CARTS\n':
				line = file.readline()
				if '=' in line:
					mails[int(line.split('=')[0])] = bool(line.split('=')[1].split('\n')[0])
			carts_data = file.readlines()
			for line in carts_data:
				if '=' in line:
					carts[int(line.split('=')[0])] = line.split('=')[1].split('\n')[0]
		file.close()
	return [states, news_types, mails, carts]

vk_session = vk_api.VkApi(token='9dfd38af10a2e483ef4c15dadbb77d6b186e912afcdd58680fd5be588c25b1d8096f4a2038623d54a2cb5')

vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, '132868814', 0)

print('methods.py started!')
