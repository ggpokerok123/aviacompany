import json
import BotModules


users_dict = BotModules.users_dict
inf_dict = BotModules.inf_dict

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


	if etype == 'bot_command':
		if current_entity == '/start':

			#updating users.json
			users_dict.update({username : {'user_id': chat_id, 'last_dream_id': -1, 'send_dreams': False}})
			BotModules.send_message(inf_dict['responses']['greeting'], chat_id)

		elif current_entity == '/dosomething':
			reply = json.dumps(inf_dict['dosomething_inline_keyboard_markup'])
			BotModules.send_inline_keyboard(inf_dict['responses']["dosomething_ans"], chat_id, reply)

		elif current_entity == '/send_message': #'/send_message username text'
			split = text.split(' ', 2)
			BotModules.send_message(split[2], users_dict[split[1]]['user_id'])

	elif etype == 'url':
		BotModules.send_message(inf_dict['responses']['url_ans'], chat_id)

	elif etype == 'text_link':
		BotModules.send_message(current_entity + inf_dict['responses']['text_link_ans'], chat_id)





@BotModules.trying
def text_response(text, chat_id):
	answers = inf_dict['answers']
	if text.lower() in answers:
		BotModules.send_message(answers[text.lower()], chat_id)
	else: 
		BotModules.send_message(text, chat_id)


@BotModules.trying
def callback_query_response(callback_query):
	
	data = callback_query['data']
	chat_id = callback_query['from']['id']

	if data == 'left_button_1': 
		callback_answert_text = 'Поздравляем, ты теперь Федоровский!'
		text = '😡'
	elif data == 'right_button_1': 
		callback_answert_text = 'Вам пизда'
		text = 'Ты ахуел?'
	elif data == 'bottom_button': 
		callback_answert_text = ''
		text = ''
	BotModules.answer_callback_query(callback_answert_text, callback_query)
	BotModules.send_message(text, chat_id)