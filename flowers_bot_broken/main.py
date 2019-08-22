from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
def get_url():
	contests = requests.get('https://random.dog/woof.json').json()
	url = contests['url']
	return url

def bop(bot, update):
	url = get_url()
	print (url)
	print (update['update_id'])
	chat_id = update.message.chat_id
	print (chat_id)
	bot.send_photo(chat_id=chat_id, photo=url)

def main():
	updater = Updater('711130363:AAFJTUhyiysVSG3Ltk42HNW2rc6NfwuGIUY', use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('bop', bop))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()