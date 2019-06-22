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


vk_session = vk_api.VkApi(token='f5b418b767430283a5ae08615df495e27530e0b8d23a8b54ed5a68610ad71abbed6949e1a419d5671ea4c')

vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, '132868814', 0)
