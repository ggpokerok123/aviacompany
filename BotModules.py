import requests 
import random
import json
import time
from source import dreams


#Initialisation
inf_file = open('inf.json', 'r', encoding = 'utf-8')
users_file = open('users.json', 'r', encoding = "utf-8")

inf_dict = json.load(inf_file)
users_dict = json.load(users_file)


#Decorator for skipping errors and data autosaving
def trying(func):
	def wrapper(*args, **kwargs):
		try: 
			return func(*args, **kwargs)
		except Exception as ex:
			print("ERROR: " + func.__name__ + ' ' + str(ex) )
			auto_save()
	return wrapper



@trying
def auto_save():
	# for user in users_dict:
		# print(user)
	json.dump(users_dict, open('users.json', 'w', encoding="utf-8"), indent = '\t', sort_keys = True, ensure_ascii = False)
	json.dump(inf_dict, open('inf.json', 'w', encoding="utf-8"), indent = '\t', sort_keys = True, ensure_ascii = False)



@trying
def get_updates_json(request):
	# Gets last 50 updates
	return requests.get(request + 'getUpdates', params={'offset':inf_dict['get_updates_offset']-49}).json()

@trying
def last_update(data, offset=1): 
	return data['result'][max(len(data['result'])-offset,0)]

@trying
def get_name(update):
	return update['message']['from']['first_name'] + ' ' + update['message']['from']['last_name']


@trying
def get_chat_id(update):
	return update['message']['chat']['id']


@trying
def get_username(update):
	try:
		return update['message']['from']['username']
	except: 
		return get_name(update)

@trying 
def get_message(update):
	if update['message']['text'][0:13] != '/send_message': print(get_username(update) + ':', end = ' ')
	if update['message']['text'][0:13] != '/send_message': print(update['message']['text'])
	return update['message']['text']

@trying
def get_entities(update):
	return update['message'].get('entities')


@trying
def send_message(text, chat_id, bot, dis_not=False):
	requests.post(bot + 'sendMessage', params = {'chat_id':chat_id, 'text':text, 'disable_notification':dis_not})
	print('anasteyshen_zbot: ' + str(text), end='\n\n')


@trying
def send_message_to_gohnny(text, bot, pre ='',  dis_not=False):
	requests.post(bot + 'sendMessage', params = {'chat_id':506531795, 
		'text':pre + str(text),
		'disable_notification' : dis_not})


@trying 
def dream_time(bot, dis_not = False):

	#Initialisation
	hours_for_dreams = inf_dict['time_for_dreams']['hours_for_dreams']
	minutes_for_dreams =  inf_dict['time_for_dreams']['minutes_for_dreams']

	# Updating time
	if time.localtime()[3] >= 9 and hours_for_dreams == -1:
		inf_dict.update({"time_for_dreams": {"hours_for_dreams": random.randint(4,9), "minutes_for_dreams": random.randint(0,59)}})

	# When time is over
	if time.localtime()[3] == hours_for_dreams and time.localtime()[4] == minutes_for_dreams:
		for user in users_dict:

			#Initialisation 
			amount_of_dreams = len(dreams)
			rnd = random.randint(0, amount_of_dreams-1)

			# Picking out random id of dream, which shouldn't duplicate previous one
			if rnd == users_dict[user]['last_dream_id']: rnd = rnd - 1 #In case, when new dream id dublicate previous id of dream sended to this user 
			users_dict[user]['last_dream_id'] = (rnd + amount_of_dreams) % amount_of_dreams #In case, when rnd == -1 (just for convenience)

			#Sending each piece of message to each user 
			for piece_of_dream in dreams[rnd]:
				send_message(piece_of_dream, users_dict[user]['user_id'], bot, dis_not = dis_not)

		inf_dict.update({"time_for_dreams": {"hours_for_dreams": -1, "minutes_for_dreams": -1}})

	
