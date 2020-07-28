import requests 
import random
import json
import time
import source


#Initialisation
anasteyshen_zbot = source.anasteyshen_zbot
dreams = source.dreams
download_file = source.download_file

inf_file = open('inf.json', 'r', encoding = 'utf-8')
users_file = open('users.json', 'r', encoding = "utf-8")

inf_dict = json.load(inf_file)
users_dict = json.load(users_file)


#Decorator for skipping errors and data autosaving
def trying(func):
	def wrapper(*args, **kwargs):
		# return func(*args, **kwargs) 	
		try: 
			return func(*args, **kwargs)
		except Exception as ex:
			print("ERROR: " + func.__name__ + ' ' + str(ex) )
			auto_save()
	return wrapper



@trying
def auto_save():
	json.dump(users_dict, open('users.json', 'w', encoding="utf-8"), indent = '\t', sort_keys = True, ensure_ascii = False)
	json.dump(inf_dict, open('inf.json', 'w', encoding="utf-8"), indent = '\t', sort_keys = True, ensure_ascii = False)



@trying
def get_updates_json(bot = anasteyshen_zbot):
	r = requests.get(bot + 'getUpdates', params={
		'offset':inf_dict['get_updates_offset']-49, 
		'timeout': 60
		}, timeout = 60).json()

	if r == None: 
		r = {}
		print("Something has gone wrong")

	return r


@trying
def last_update(data, offset=1): 
	# print("jopen")
	return data['result'][max(len(data['result'])-offset,0)]

@trying
def get_callback_query(update):
	return update['callback_query']

@trying 
def answer_callback_query(text, callback_query, bot):
	requests.post(bot + 'answerCallbackQuery', params = {
		'callback_query_id': callback_query['id'],
		'text': text
		})


@trying
def get_photo(update, bot = anasteyshen_zbot):
	file_id = update['message']['photo']
	file_id.reverse()
	file_id = file_id[0]['file_id']

	# Getting photo's file_id
	r = requests.get(bot + 'getFile', params = {'file_id' : file_id}).json()
	file_path = r['result']['file_path'] # getting file path to download it

	# Getting our binary file 
	r = requests.get(download_file + file_path) # download_file is url for downloading

	# Downloading our photo with name "{username}_{chat_id}.png" in folder "photos"
	username = get_username(update)
	chat_id = get_chat_id(update)
	open('photos/' + str(username) + '_' + str(chat_id) + '.png', 'wb').write(r.content)	

	send_message("Ого, маєш класне фото", chat_id)
	return True

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
def get_text(update):
	if update['message']['text'][0:13] != '/send_message': print(get_username(update) + ':', end = ' ')
	if update['message']['text'][0:13] != '/send_message': print(update['message']['text'])
	return update['message']['text']

@trying
def get_entities(update):
	return update['message'].get('entities')


@trying
def send_message(text, chat_id, bot = anasteyshen_zbot, dis_not = False):
	requests.post(bot + 'sendMessage', params = {'chat_id':chat_id, 'text':text, 'disable_notification':dis_not})
	print('anasteyshen_zbot: ' + str(text), end='\n\n')




@trying 
def send_inline_keyboard(text, chat_id, inline_keyboard_markup, bot, dis_not = False):
	requests.post(bot + 'sendMessage', params = {
		'text' : text,
		'chat_id' : chat_id,
		'disable_notification' : dis_not,
		'reply_markup' : inline_keyboard_markup
		})


@trying
def send_photo(caption, chat_id, input_file, bot = anasteyshen_zbot, dis_not = False):
	if str(input_file.__class__) == "<class '_io.BufferedReader'>":
		# sendMediaGroup
		requests.post(bot + 'sendPhoto', params = {
			'caption' : caption,
			'chat_id' : chat_id,
			}, files = {'photo': input_file})
	else: 
		requests.post(bot + 'sendPhoto', params = {
			'caption' : caption,
			'chat_id' : chat_id,
			'photo' : input_file
			})




# # @trying
# def send_photo2(chat_id, media, bot = anasteyshen_zbot, dis_not = False):
	
# 	r = requests.post(bot + 'sendMediaGroup', params = {
# 		'chat_id': chat_id,
# 		'media': media
# 		})
# 	print(r.text)




@trying
def send_message_to_gohnny(text, bot, pre = '',  dis_not = False):
	requests.post(bot + 'sendMessage', params = {
		'chat_id':506531795, 
		'text':pre + str(text),
		'disable_notification' : dis_not
		})


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

	
