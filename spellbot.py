import tweepy
from config import bot_auth
 
class StreamListener(tweepy.StreamListener):

	def on_status(self, status):
		try:
			if status.user.screen_name==bot.handle:
				return
			if not status.lang=="en":
				return
			if not status.user.followers_count>2000:
				return

			try:
				bot.create_favorite(status.id)
				bot.create_friendship(status.user.screen_name)
			except:
				pass
			
		
			words=status.text.split(" ")
			response=""
			spell_error=False

			for i in words:
				for j in bot.errors:
					if j == i.lower():
						ind=words.index(i)
						if ind==len(words):
							return

						eind=bot.errors.index(j)
						corr=bot.correct[eind]
						response='…%s "%s" %s… !?\n'%(words[ind-1],words[ind].upper(),words[ind+1])
						response+='Did you mean "%s" ?'%corr.upper()
						spell_error=True

			if spell_error:
				print(response,"\n\n")
			
				bot.update_status(status=response, 
				in_reply_to_status_id = status.id,
				auto_populate_reply_metadata=True)

				
		except Exception as e:
			print(e)


	def on_error(self, status_code):
		if status_code == 420:
			return False







class Bot(tweepy.API):


	def set_conf(self,correct,animals):
		self.correct=correct
		self.errors=errors
		self.handle="bot_c137"		
		
	def listen_spellings(self):
		stream_listener = StreamListener()
		stream = tweepy.Stream(auth=auth, listener=stream_listener)
		stream.filter(track=self.errors)
		

	def clean_up_timeline(self):
		for tweet in tweepy.Cursor(self.user_timeline).items():
			if tweet.is_quote_status:
				try:
					quoted_id=tweet.entities['urls'][0]['expanded_url']
					quoted_id=int(quoted_id.split("/")[-1])
					src=self.get_status(quoted_id)
				except:
					self.destroy_status(tweet.id)

	def follow_followers(self):
		self.followers_list=self.followers_ids()
		for follower in self.followers_list:
			self.create_friendship(follower)

	def unfollow_nonfollowers(self):
		self.followers_list=self.followers_ids()
		self.following_list=self.friends_ids()
		for user in self.following_list:
			if user not in self.followers_list:
				self.destroy_friendship(user)





auth = tweepy.OAuthHandler(bot_auth['consumer_key'], bot_auth['consumer_secret'])
auth.set_access_token(bot_auth['access_token'], bot_auth['access_token_secret'])

bot=Bot(auth)


correct=[]
errors=[]

with open("spell.dat") as file:
	for i in file:
		errors.append(i.split("|")[0])
		correct.append(i.split("|")[1][:-1])

bot.set_conf(correct,errors)
bot.listen_spellings()


	