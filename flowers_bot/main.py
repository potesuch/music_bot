import requests
import datetime

class BotHandler:

	def __init__(self, token):
		self.token = token
		self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

	def get_updates(self, offset=None, timeout=100):
		method = 'getUpdates'
		params = {'timeout': timeout, 'offset': offset}
		resp = requests.get(self.api_url + method, params)
		result_json = resp.json()['result']
		return result_json

	def send_message(self, chat_id, text):
		method = 'sendMessage'
		params = {'chat_id': chat_id, 'text': text}
		resp = requests.post(self.api_url + method, params)
		return resp

	def send_photo(self, chat_id, photo):
		method = 'sendPhoto'
		params = {'chat_id': chat_id, 'photo': photo}
		resp = requests.post(self.api_url + method, params)
		return resp

	def get_last_update(self):
		get_result = self.get_updates()

		if len(get_result) > 0:
			last_update = get_result[-1]
		else:
			lest_update = None

		return last_update

token = '711130363:AAFJTUhyiysVSG3Ltk42HNW2rc6NfwuGIUY'
fl_bot = BotHandler(token)
now = datetime.datetime.now()


def main():
	new_offset = None

	while True:
		fl_bot.get_updates(new_offset)

		last_update = fl_bot.get_last_update()

		if last_update is None: continue

		last_update_id = last_update['update_id']
		last_chat_text = last_update['message']['text']
		last_chat_id = last_update['message']['chat']['id']
		last_chat_name = last_update['message']['chat']['first_name']

		print (last_chat_text)

		if last_chat_text == '/bop':
			contests = requests.get('https://random.dog/woof.json').json()
			url = contests['url']
			print (url)
			fl_bot.send_photo(last_chat_id, url)

		new_offset = last_update_id + 1
					
if __name__ == '__main__':
	main()