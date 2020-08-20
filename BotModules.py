import requests 
import random
import json
import time

from pytube import YouTube
from googletrans import Translator
from Imageprediction.ImagePrediction import predict


#Initialisation

translator = Translator()

inf_file = open('inf.json', 'r', encoding = 'utf-8')
users_file = open('users.json', 'r', encoding = 'utf-8')

inf_dict = json.load(inf_file)
users_dict = json.load(users_file)

anasteyshen_zbot = inf_dict['anasteyshen_zbot']
dreams = inf_dict['dreams']
download_file = inf_dict['download_file']

#Decorator for skipping errors and data autosaving
def trying(func):
	def wrapper(*args, **kwargs):
		# return func(*args, **kwargs) 	
		try: 
			return func(*args, **kwargs)
		except Exception as ex:
			print("ERROR: " + func.__name__ + ' ' + str(ex))
			auto_save()
	return wrapper



@trying
def auto_save():
	json.dump(users_dict, open('users.json', 'w', encoding = "utf-8"), indent = '\t', sort_keys = True, ensure_ascii = False)
	json.dump(inf_dict, open('inf.json', 'w', encoding = "utf-8"), indent = '\t', sort_keys = True, ensure_ascii = False)



@trying
def get_updates_json(bot = anasteyshen_zbot):
	r = requests.get(bot + 'getUpdates', params={
		'offset':inf_dict['get_updates_offset']-49
		}, timeout = 60).json()

	if r == None: 
		r = {'haha' : 'it\'s an Error ) ) )'}
		print("Something has gone wrong")

	return r


@trying
def last_update(data, offset=1): 
	return None if len(data['result']) == 0 else data['result'][max(len(data['result'])-offset,0)]

@trying
def get_callback_query(update):
	return update['callback_query']

@trying 
def answer_callback_query(text, callback_query, bot = anasteyshen_zbot):
	requests.post(bot + 'answerCallbackQuery', params = {
		'callback_query_id': callback_query['id'],
		'text': text
		})


@trying
def get_photo(update, bot = anasteyshen_zbot):

	username = get_username(update)
	chat_id = get_chat_id(update)
	file_id = update['message']['photo'][-1]['file_id']
	
	send_message("Ща, грузит", chat_id)
		
	# Getting photo's file_id
	r = requests.get(bot + 'getFile', params = {'file_id' : file_id}).json()
	file_path = r['result']['file_path'] # getting file path to download it

	# Getting our binary file 
	r = requests.get(download_file + file_path) # download_file is url for downloading


	# Downloading photo to this folder and use imageprediction.py
	open('Imageprediction/img.jpg', 'wb').write(r.content)	
	predictions, probabilities = predict()

	
	if probabilities[0] >= 50.0 and probabilities[0]-probabilities[1] > 10.0: 
		translation = translator.translate(predictions[0].replace('_', ' '), dest = 'ru')
		translation = translator.translate(translation.text, src = 'ru', dest = 'uk')
		send_message('Ого, маєш класний ' + translation.text.lower(), chat_id)

	elif probabilities[0] >= 50.0 and probabilities[0]-probabilities[1] <= 10: 
		translation = translator.translate(predictions[0].replace('_', ' '), dest = 'ru')
		translation = translator.translate(translation.text, src = 'ru', dest = 'uk')
		send_message('Ого, маєш класний ' + translation.text.lower(), chat_id)

		translation = translator.translate(predictions[1].replace('_', ' '), dest = 'ru')
		translation = translator.translate(translation.text, src = 'ru', dest = 'uk')
		send_message('Чи маєш гарний ' + translation.text.lower() + '...', chat_id)

	else: 
		send_message('Я не понял(', chat_id)

	# Downloading our photo with name "{username}_{chat_id}.png" in folder "photos"
	open('photos/' + str(username) + '_' + str(chat_id) + '.png', 'wb').write(r.content)	

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
def send_message(text, chat_id, inline_keyboard_markup = None, bot = anasteyshen_zbot, dis_not = False):
	requests.post(bot + 'sendMessage', params = {
		'chat_id': chat_id, 
		'text': text, 
		'disable_notification': dis_not,
		'reply_markup': inline_keyboard_markup
		})
	# print('anasteyshen_zbot: ' + str(text), end='\n\n')




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




@trying
def send_media_group(chat_id, media, files = None, bot = anasteyshen_zbot, dis_not = False):
	"""
	type can be: animation, photo, video, audio, document
	media = [
		{
			"type": "photo",
			"media": "https://i.pinimg.com/originals/7a/04/2c/7a042c17c987a64636eda30198cad865.jpg",
			'caption': 'А шо, звучит хайпово'
		}, 
		{
			"type": "photo",
			"media": "https://i.ytimg.com/vi/xqtgMIkjAvw/hqdefault.jpg"
		}
	]

	or 
	
	files = {'a' : open('a.png', 'rb'), 'b' : open('b.png', 'rb')}
	media = [
		{
			"type": "photo",
			"media": "attach://b",
			'caption': 'А шо, звучит хайпово'
		}, 
		{
			"type": "photo",
			"media": "attach://a"
		}
	]

	"""
	requests.post(bot + 'sendMediaGroup', params = {
		'chat_id': chat_id,
		'media': media
		}, files = files)


@trying
def send_audio(caption, chat_id, audio, title, performer, bot = anasteyshen_zbot):
	r = requests.post(bot + 'sendAudio', params = {
		'chat_id': chat_id,
		'caption': caption,
		'title': title,
		'performer': performer
		}, files = {
		'audio': audio
		}).json()
	# json.dump(r, open('debug.json', 'w', encoding = "utf-8"), indent = '\t', sort_keys = True, ensure_ascii = False)




@trying
def send_message_to_gohnny(text, pre = '',  dis_not = False,  bot = anasteyshen_zbot):
	requests.post(bot + 'sendMessage', params = {
		'chat_id':506531795, 
		'text':pre + str(text),
		'disable_notification' : dis_not
		})


@trying 
def edit_message_text(message_id, edited_text, chat_id, reply_markup = None, bot = anasteyshen_zbot):
	requests.post(bot + 'editMessageText', params = {
		"message_id": message_id,
		"chat_id": chat_id,
		"text": edited_text,
		"reply_markup": reply_markup 
		})

@trying 
def dream_time(bot = anasteyshen_zbot, dis_not = False):

	#Initialisation
	hours_for_dreams = inf_dict['time_for_dreams']['hours_for_dreams']
	minutes_for_dreams =  inf_dict['time_for_dreams']['minutes_for_dreams']

	# Updating time
	if time.localtime()[3] >= 10 and hours_for_dreams == -1:
		inf_dict.update({"time_for_dreams": {"hours_for_dreams": random.randint(4,9), "minutes_for_dreams": random.randint(0,59)}})

	# When time is over
	if time.localtime()[3] == hours_for_dreams and time.localtime()[4] == minutes_for_dreams:
		for user in users_dict:
			if users_dict[user]['send_dreams'] == False: continue

			#Initialisation 
			amount_of_dreams = len(dreams)
			rnd = random.randint(0, amount_of_dreams-1)

			# Picking out random id of dream, which shouldn't duplicate previous one
			if rnd == users_dict[user]['last_dream_id']: rnd = rnd - 1 #In case, when new dream id dublicate previous id of dream sended to this user 
			users_dict[user]['last_dream_id'] = (rnd + amount_of_dreams) % amount_of_dreams #In case, when rnd == -1 (just for convenience)

			#Sending each piece of message to each user 
			for piece_of_dream in dreams[rnd]:
				send_message(piece_of_dream, users_dict[user]['user_id'], bot, dis_not = dis_not) # user['user_id'] instead of users_dict[user]['user_id']???

		inf_dict.update({"time_for_dreams": {"hours_for_dreams": -1, "minutes_for_dreams": -1}})

	







@trying
def yt_search_and_send(q, chat_id):
	yt_token = 'AIzaSyBhS2JrJ0PgQF73SLFvub72fmmArIFSN0s'
	yt_url = 'https://www.googleapis.com/youtube/v3/'

	r = requests.get(yt_url + 'search', params = {
		"key": yt_token,
		"part": "snippet",
		"maxResults": 6,
		"type": "video",
		"q": q # KeyWords for searching 
		}).json()['items']

	audio_inline_keyboard_markup = inf_dict['audio_inline_keyboard_markup']

	# json.dump(r, open('debug.json', 'w', encoding = "utf-8"), indent = '\t', sort_keys = True, ensure_ascii = False)
	text = ''
	i = 1 
	videoID_dict = {}
	for video in r: 
		text += str(i) + ' ' + video['snippet']['channelTitle'] + ' - ' + video['snippet']['title'] + '\n\n'
		videoID_dict.update({str(i): video['id']['videoId']})
		i += 1 
		# print(video['snippet']['title'])

		# video['snippet']['title']
		# video['id']['videoId']
		# video['snippet']['channelTitle']

		# yt_id = video['id']['videoId']
		# yt = YouTube(f'https://www.youtube.com/watch?v={yt_id}')
		# yt.streams.filter(only_audio = True)[0].download('./audios')
	print(videoID_dict)
	send_message('Какую?\n\n' + text, chat_id, json.dumps(audio_inline_keyboard_markup))





