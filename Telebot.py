from source import *
import BotModules
import random
import time
import responses
import json 

last_data = BotModules.last_update(BotModules.get_updates_json())
if last_data != None: BotModules.inf_dict.update({'get_updates_offset': last_data["update_id"]})

# print("AND HERE WE GO\n")


try:
	while True:
		# print('mem1')
		BotModules.dream_time(anasteyshen_zbot, dis_not = True)
		data = BotModules.last_update(BotModules.get_updates_json())
		# print('mem2')
		if data == None or last_data['update_id'] >= data['update_id']: continue 

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
	

