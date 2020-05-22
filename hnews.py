import requests
from bs4 import BeautifulSoup
import telegram
import schedule
from threading import Thread
from time import sleep
from datetime import date

file = requests.get('https://news.ycombinator.com/').text
soup = BeautifulSoup(file, 'html.parser')
links = soup.select('.storylink')
athing = soup.select('.athing')

def create_custom_hnews(links, athing):
	hnews = []
	string =[]
	for idx, val in enumerate(links):
		title_text = links[idx].getText()
		href_url = links[idx].get('href', None)
		rnk = athing[idx].select('.rank')
		r = int(rnk[0].getText().replace('.', ''))
		hnews.append({'rank': r, 'title': title_text, 'url': href_url})
	for idx, i in enumerate(range(len(hnews))):
		title = hnews[i]['title']
		link = hnews[i]['url']
		rank = hnews[i]['rank']
		string.append(f'\n {rank}. {title},\n{link}\n')
		if idx == 25:
			break
	return ''.join(string)


# telegram bot configuration

my_token = 'your token'
msg = create_custom_hn(links, athing)
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

today = date.today()
send(f'Top news for {today.strftime("%a, %d %B, %Y")} \n'+msg, chat_id_me, my_token)

def calling():
	return send(f'Top news for {today.strftime("%a, %d %B, %Y")} \n'+msg, chat_id_me, my_token)



def schedule_checker():
	while True:
		schedule.run_pending()
		sleep(1)


if __name__ == "__main__":
	# Create the job in schedule.
	# schedule.every().hour.do(calling)
	schedule.every().day.at("10:00").do(calling)
	#
	# Spin up a thread to run the schedule check so it doesn't block your bot.
	# This will take the function schedule_checker which will check every second
	# to see if the scheduled job needs to be ran.
	Thread(target=schedule_checker).start()
	#
	# And then of course, start your server.
	# server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

