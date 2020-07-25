from source import *
import json
import BotModules

@BotModules.trying
def entity_response(text, chat_id, username, entities, num = 0):
	"""
	Example: "entities":[{"offset":0,"length":6,"type":"bot_command"}]

	Type of the entity. Can be:
	“mention” (@username), 
	“hashtag” (#hashtag), 
	“cashtag” ($USD), 
	“bot_command” (/start@jobs_bot),
	“url” (https://telegram.org), 
	“email” (do-not-reply@telegram.org), 
	“phone_number” (+1-212-555-0123), 
	“bold” (bold text), 
	“italic” (italic text),
	“underline” (underlined text), 
	“strikethrough” (strikethrough text),
	“code” (monowidth string), 
	“pre” (monowidth block), 
	“text_link” (for clickable text URLs), 
	“text_mention” (for users without usernames)
	"""

	etype = entities[num]['type']
	current_entity = text[entities[num]['offset']:entities[num]['offset']+entities[num]['length']]
	users_dict = BotModules.users_dict

	if etype == 'bot_command':
		if current_entity == '/start':

			#updating users.json
			users_dict.update({username : {'user_id': chat_id, 'last_dream_id': -1}})
			BotModules.send_message(greeting, chat_id, anasteyshen_zbot)

		elif current_entity == '/dosomething':
			BotModules.send_message(dosomething_ans, chat_id, anasteyshen_zbot)

		elif current_entity == '/send_message': #'/send_message username text'
			split = text.split(' ', 2)
			BotModules.send_message(split[2], users_dict[split[1]]['user_id'], anasteyshen_zbot)



	elif etype == 'url':
		BotModules.send_message(url_ans, chat_id, anasteyshen_zbot)

	elif etype == 'text_link':
		BotModules.send_message(current_entity + text_link_ans, chat_id, anasteyshen_zbot)

@BotModules.trying
def text_response(text, chat_id, username):
	if text.lower() in answers:
		BotModules.send_message(answers[text.lower()], chat_id, anasteyshen_zbot)
	else: 
		BotModules.send_message(text, chat_id, anasteyshen_zbot)