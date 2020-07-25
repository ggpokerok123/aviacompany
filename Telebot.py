from source import *
import BotModules
import random
import time
import responses
import json 

last_data = BotModules.last_update(BotModules.get_updates_json(anasteyshen_zbot))




try:
	while True: 
		BotModules.dream_time(anasteyshen_zbot, dis_not = True)
		data = BotModules.last_update(BotModules.get_updates_json(anasteyshen_zbot))
		if last_data == data or data == None: continue 

		message = BotModules.get_message(data)
		chat_id = BotModules.get_chat_id(data)
		entities = BotModules.get_entities(data)
		username = BotModules.get_username(data)





		if entities != None: 
			responses.entity_response(message, chat_id, username, entities)
		else: 
			responses.text_response(message, chat_id, username)

		BotModules.send_message_to_gohnny(message, anasteyshen_zbot, pre = str(username) + ': ')

		last_data = data
		time.sleep(.5)
except BaseException:
	BotModules.auto_save()
	

