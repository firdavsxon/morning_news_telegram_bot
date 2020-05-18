import requests
from bs4 import BeautifulSoup
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler)
from telegram import InlineQueryResultArticle, InputTextMessageContent
import schedule
from threading import Thread
from time import sleep

response = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.select('.storylink')


def create_custom_hn(links):
	hn = []
	for idx, item in enumerate(links):
		title = links[idx].getText()
		href = links[idx].get('href', None)
		while len(hn) != 25:
			hn.append({'title': title, 'link': href})
			break
	return hn


# telegram bot configuration

my_token = 'your token'
msg = create_custom_hn(links)
chat_id_me = 'telegram chat id
chat_id = 'telegram chat id'


updater = Updater(token=my_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

# inline caps for telegram channel for opening youtube, wikipedia .etc in bot chat
def inline_caps(update, context):
	query = update.inline_query.query
	if not query:
		return
	results = list()
	results.append(
		InlineQueryResultArticle(
			id=query.upper(),
			title='Caps',
			input_message_content=InputTextMessageContent(query.upper())
		)
	)
	context.bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


def send(msg, chat_id, token=my_token):
	"""
	Send a message to a telegram user specified on chatId
	chat_id must be a number!
	"""
	bot = telegram.Bot(token=token)
	return bot.sendMessage(chat_id=chat_id, text=msg)


def inout_message(msg):
	string= []
	for i in range(len(msg)):
		tit = msg[i]['title']
		lin = msg[i]['link']
		string.append(f'\n ~ {tit}, {lin}\n')
	return ''.join(string)


send(inout_message(msg), chat_id_me, my_token)


def calling_me():
	return send(inout_message(msg), chat_id_me, my_token)


def calling_friend():
	return send(inout_message(msg), chat_id, my_token)


def schedule_checker():
	while True:
		schedule.run_pending()
		sleep(1)


if __name__ == "__main__":
	# Create the job in schedule.
	# schedule.every().minute.do(calling_me)
	# schedule.every().minute.do(calling_friend)
	schedule.every().day.at("15:00").do(calling_me)
	schedule.every().day.at("17:00").do(calling_friend)
	#
	# Spin up a thread to run the schedule check so it doesn't block your bot.
	# This will take the function schedule_checker which will check every second
	# to see if the scheduled job needs to be ran.
	Thread(target=schedule_checker).start()
	#
	# And then of course, start your server.
	# server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

