import praw
import os.path

#settings
processed_log = 'processed_submissions.txt'

find_posts_in = "meetsingles" #can be comma separated to check multiple subs
check_for_flair = "request" #will only crosspost if submission contains this flair

post_to_sub = "singles" #where to crosspost to

reddit = praw.Reddit(
	user_agent="Crosspost Bot " + find_posts_in + " -> " + post_to_sub,
	
	#api details
	client_id="",
	client_secret="",
	
	#reddit account details
	username="",
	password="",
)
#end settings

def main():

	print('Bot Started')
	
	if os.path.isfile(processed_log) == False:
		print("Creating processing log file")
		file_object = open('processed_submissions.txt', 'a')
		file_object.close()
	
	submissions = praw.models.util.stream_generator(reddit.subreddit(find_posts_in).new)
	try:
		for s in submissions:
			if check_id(s.id):
				write_id(s.id + "\n")
				if s.link_flair_text is not None:
					if check_for_flair in s.link_flair_text.casefold():
						print("crossposting: " + s.id + " - " + s.title)
						s.crosspost(subreddit=post_to_sub)
					else:
						'Incorrect Flair'
				else:
					'No Flair'
			else:
				'Already Processed'
		
		print("End of submission stream")
	except (prawcore.exceptions.Forbidden, prawcore.exceptions.ServerError):
		'Auth Failed.'
	except:
		traceback.print_exc(file=sys.stdout)

def write_id(id):
	file_object = open(processed_log, 'a')
	file_object.write(id)
	file_object.close()

def check_id(id):
	with open(processed_log, "a+") as file:
		file.seek(0)
		lines = file.read().splitlines()
		if id in lines:
			return False
		else:
			return True
	
if __name__ == "__main__":
	main()