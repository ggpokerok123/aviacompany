import BotModules
import responses
import time

last_data = BotModules.last_update(BotModules.get_updates_json())
if last_data != None: BotModules.inf_dict.update({'get_updates_offset': last_data["update_id"]})


print('daun')
try:
	while True:
		BotModules.dream_time(dis_not = True)
		data = BotModules.last_update(BotModules.get_updates_json())
		
		if data == None or last_data['update_id'] >= data['update_id']: continue 

		##############################################################################################

		BotModules.get_photo(data)


		text = BotModules.get_text(data)
		chat_id = BotModules.get_chat_id(data)
		entities = BotModules.get_entities(data)
		username = BotModules.get_username(data)
		callback_query = BotModules.get_callback_query(data)


		if entities != None: 
			responses.entity_response(text, chat_id, username, entities)
		elif text != None: 
			responses.text_response(text, chat_id, username)
		elif callback_query != None: 
			responses.callback_query_response(callback_query)

		# BotModules.send_message_to_gohnny(text, pre = str(username) + ': ')

		##############################################################################################

		last_data = data
		BotModules.inf_dict.update({'get_updates_offset': last_data["update_id"]})
		time.sleep(.5)
except BaseException:
	BotModules.auto_save()
	

