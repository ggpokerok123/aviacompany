from source import *
import BotModules
import random
import time
import responses
import json 

last_data = BotModules.last_update(BotModules.get_updates_json())
BotModules.inf_dict.update({'get_updates_offset': last_data["update_id"]})



# input_file1 = {
# 	'type': 'photo',
# 	'media': 'https://i.pinimg.com/originals/7a/04/2c/7a042c17c987a64636eda30198cad865.jpg'
# 	}

# input_file2 = {
# 	'type': 'photo',
# 	'media': 'https://i.ytimg.com/vi/xqtgMIkjAvw/hqdefault.jpg'
# }

# media = [json.dumps(input_file1), json.dumps(input_file2)]
# # open('photos/Gohnny_506531795.png', 'rb')

# BotModules.send_photo2(506531795, media)
# # BotModules.send_photo('snake', 506531795, 'https://i.pinimg.com/originals/7a/04/2c/7a042c17c987a64636eda30198cad865.jpg')


try:
	while True: 
		BotModules.dream_time(anasteyshen_zbot, dis_not = True)
		data = BotModules.last_update(BotModules.get_updates_json(anasteyshen_zbot))

		if last_data['update_id'] >= data['update_id'] or data == None: continue 

		##############################################################################################

		if BotModules.get_photo(data): 
			pass
		else:
			text = BotModules.get_text(data)
			chat_id = BotModules.get_chat_id(data)
			entities = BotModules.get_entities(data)
			username = BotModules.get_username(data)
			callback_query = BotModules.get_callback_query(data)


			if entities != None: 
				responses.entity_response(text, chat_id, username, entities)
			elif text != None: 
				responses.text_response(text, chat_id)
			elif callback_query != None: 
				responses.callback_query_response(callback_query)

			BotModules.send_message_to_gohnny(text, anasteyshen_zbot, pre = str(username) + ': ')

		##############################################################################################

		last_data = data
		BotModules.inf_dict.update({'get_updates_offset': last_data["update_id"]})
		time.sleep(.5)
except BaseException:
	BotModules.auto_save()
	

