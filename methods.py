import vk_api, random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def msg(id, message='', board=[], attach=''):
	if board:
		vk.messages.send(peer_id=id, random_id=random.randint(-2147483648, 2147483647), message=message, attachment=attach, keyboard=board)
	else:
		vk_session.method('messages.send', {'peer_id': id, 'random_id': random.randint(-2147483648, 2147483647), 'message': message, 'attachment': attach, 'keyboard': board})
	print('Сообщение с текстом «{}» для {} отправлено'.format(message ,id))

def name(id, case='nom'):
	return vk.users.get(user_ids=id, fields='first_name, last_name', name_case=case)[0]

def sex(id):
	return vk.users.get(user_ids=id, fields='sex')[0]['sex']

def get_attachs(msg_id):
	attachs = []
	for a in vk.messages.getById(message_ids=msg_id, extended=1)['items'][0]['attachments']:
		type = a['type']
		if 'access_key' in a[type]: attachs.append(type + str(a[type]['owner_id']) + '_' + str(a[type]['id']) + '_' + str(a[type]['access_key']))
		else: attachs.append(type + str(a[type]['owner_id']) + '_' + str(a[type]['id']))
	attachs = ', '.join(attachs)
	return attachs

def get_poll(id, own_id, var_id=0):
	poll = vk.polls.getById(owner_id=own_id, poll_id=id)
	name = poll['question']
	if var_id:
		for ans in poll['answers']:
			if ans['id'] == var_id:
				answer = ans['text']
		return [name, answer]
	else:
		return name

def online():
	vk.groups.enableOnline(group_id=132868814)

def isMember(group, id):
	return vk.groups.isMember(group_id=group, user_id=id)


vk_session = vk_api.VkApi(token='a65f7372579bd5eb918cf5c04562e251e243500569ae286f8d489383813ebb4043e3d711b8b4b8aad831f')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, '132868814', 0)
