import vk_api
import random
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def msg(id, message='', board=[], forward='', attach='', parse=True):
	vk_session.method('messages.send', {'peer_id': id, 'random_id': random.randint(-2147483648, 2147483647), 
										'message': message, 'forward_messages': forward, 'keyboard': board, 
										'dont_parse_links': not parse, 'attachment': attach})
	print('Сообщение для {} отправлено'.format(id))

def msg_edit(id, m_id, message='', board=[]):
	vk_session.method('messages.edit', {'peer_id': id, 'message': message, 
										'keyboard': board, 'conversation_message_id': m_id, 'dont_parse_links': True})
	print('Сообщение для {} изменено'.format(id))

def name(id, case='nom'):
	if int(id) > 0:
		return vk.users.get(user_ids=id, fields='first_name, last_name', name_case=case)[0]
	else:
		return {'first_name': vk.groups.getById(group_id=id)[0]['name'], 'last_name': ''}


def link(id):
	if int(id) > 0:
		return vk.users.get(user_ids=id, fields='domain')[0]['domain']
	else:
		return vk.groups.getById(group_id=id)[0]['screen_name']


def sex(id):
	if int(id) > 0:
		return vk.users.get(user_ids=id, fields='sex')[0]['sex']


def get_id(id, offset=1):
	return vk.messages.getHistory(offset=offset, count=1, user_id=id)['items'][0]['id']


def delete(msg_id):
	vk.messages.delete(message_ids=msg_id, delete_for_all=True)


def isMember(group, id):
	return vk.groups.isMember(group_id=group, user_id=id)


def parse_docs(attachments):
	links = []
	for attach in attachments:
		type = attach['type']
		object = attach[type]
		if type == 'doc':
			is_photo = True if object['type'] == 4 else False
			if is_photo:
				url = object['url']
				links.append(upload(url))
		elif type == 'photo':
			url = object['sizes'][-1]['url']
			links.append(upload(url))
		elif type == 'video':
			links.append('video{}_{}_{}'.format(object['owner_id'], object['id'], object['access_key']))
	return ','.join(links)


def get_allow():
	allow_dict, chats_arr, offset = dict(), True, 0
	while chats_arr:
		chats_arr = vk.messages.getConversations(offset=offset, count=200)['items']
		for i in chats_arr:
			allow_dict[i['conversation']['peer']['id']] = i['conversation']['can_write']['allowed']
		offset += 200
	return allow_dict


def upload(*args):
	session = requests.Session()
	links = []
	for arg in args:
		obj = session.get(arg, stream=True)
		vk_obj = vk_upload.photo_messages(photos=obj.raw)[0]
		links.append('photo{}_{}_{}'.format(vk_obj['owner_id'], vk_obj['id'], vk_obj['access_key']))
	return ','.join(links)


def read_data():
	states, news_types, mails, mute, carts = dict(), dict(), dict(), [], dict()
	with open('data.txt', encoding='utf-8') as file:
		line = file.readline()
		if line == '\ufeffSTATES\n':
			while line != 'NEWS_TYPES\n':
				line = file.readline()
				if '=' in line:
					states[int(line.split('=')[0])] = line.split('=')[1][:-1]
			while line != 'MAILS\n':
				line = file.readline()
				if '=' in line:
					news_types[int(line.split('=')[0])] = line.split('=')[1][:-1]
			while line != 'MUTE\n':
				line = file.readline()
				if '=' in line:
					mails[int(line.split('=')[0])] = bool(int(line.split('=')[1][:-1]))
			line = file.readline().strip()
			if line:
				mute = list(map(int, line.split(',')))
			file.readline()
			file.readline()
			carts_data = file.readlines()
			for line in carts_data:
				if '=' in line:
					carts[int(line.split('=')[0])] = line.split('=')[1][:-1]
		file.close()
	return [states, news_types, mails, mute, carts]


vk_session = vk_api.VkApi(
	token='9dfd38af10a2e483ef4c15dadbb77d6b186e912afcdd58680fd5be588c25b1d8096f4a2038623d54a2cb5')

vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, '132868814', 0)

vk_upload = vk_api.upload.VkUpload(vk_session)

print('methods.py started!')
