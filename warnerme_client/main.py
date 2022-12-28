import requests

BASE = 'https://warnerme-bot-api.onrender.com/warnMe/' #Adress of our API

class WarnerMe:

	def __init__(self, user_id):
		self.req_str = BASE + str(user_id)

	def status(self):
		resp = requests.get(self.req_str, {}) # You can get current information. your_id is id that was taken by Warner-Me Telegram Bot.
		return resp.json()

	def activate(self, status = True):
		requests.patch(self.req_str, {'codeStatus':'active', 'results': ''}) #patch updates your code status and results. Before running a code script you can change it as active.
		
		if status:
			return self.status()

	def deactivate(self, code_status = 'inactive', result_str = '', status = True, post_telegram = True):

		if post_telegram:
			requests.post(self.req_str, {'codeStatus': code_status, 'results': result_str}) #post also updates your code states and results. The only difference between patch and post is that post will inform you on Telegram automatically when your process is done.
		else:
			requests.patch(self.req_str, {'codeStatus': code_status, 'results': result_str}) #patch updates your code status and results.

		if status:
			return self.status()