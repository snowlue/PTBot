import vk_api, random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def msg(id, message='', stick=0, attach='', board=[]):
	vk.method('messages.send', {'peer_id': id, 'random_id': random.randint(-2147483648, 2147483647), 'message': message, 'attachment': attach, 'sticker_id': stick, 'keyboard': board})
	print('Сообщение для {} отправлено'.format(id))

def name(id):
	return vk.method('users.get', {'user_ids': id, 'fields': 'first_name, last_name', 'name_case': 'Nom'})[0]

def give_attachs(msg_id):
	attachs, stick = [], 0
	for a in vk.method('messages.getById', {'message_ids': msg_id, 'extended': 1})['items'][0]['attachments']:
		type = a['type']
		if 'access_key' in a[type]: attachs.append(type + str(a[type]['owner_id']) + '_' + str(a[type]['id']) + '_' + str(a[type]['access_key']))
		elif type == 'sticker': stick = a[type]['sticker_id']
		else: attachs.append(type + str(a[type]['owner_id']) + '_' + str(a[type]['id']))
	attachs = ', '.join(attachs)
	arr = [attachs, stick]
	return arr

def online():
	vk.method('groups.enableOnline', {'group_id': 132868814})

vk = vk_api.VkApi(token='a65f7372579bd5eb918cf5c04562e251e243500569ae286f8d489383813ebb4043e3d711b8b4b8aad831f')

longpoll = VkBotLongPoll(vk, '132868814', 0)
