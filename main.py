import praw, datetime, json, os, time

r = praw.Reddit("frontOfLeague by /u/thirdegree")

def _login():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	SUBREDDIT = raw_input("Subreddit to post to?\n> ")
	r.login(USERNAME, PASSWORD)
	return SUBREDDIT

Trying = True
while Trying:
	try:
		SUBREDDIT = _login()
		Trying = False
	except praw.errors.InvalidUserPass:
		print "Invalid Username/password, please try again."

def main():
	try:
		obj = open("frontOfLeague", "r+")
	except IOError:
		obj = open('frontOfLeague', "w+")
	try:
		front = json.loads(obj.read())
		front = set([(i[0], i[1]) for i in front])
	except ValueError:
		front = set([])
	obj.close()
	league = r.get_subreddit("leagueoflegends")
	limit = 25
	league_hot = league.get_hot(limit=limit)
	for place, post in zip(xrange(1,limit+1), league_hot):
		#I'm so thankful this worked the first time, this is just awful.
		name = post.permalink
		current = filter(lambda x: x[0]==name, list(front))
		#technically only works if no post is rank > 100000000
		smallest_past = min([i[1] for i in current] or [100000000])
		smallest = min(place, smallest_past)
		front.add((name, smallest))
	front = list(front)
	front.sort(key=lambda x: x[1])
	with open("frontOfLeague", "w") as obj:
		json.dump(front, obj, indent=4)

def poster():
	global LAST_CLEARED
	LAST_CLEARED = datetime.date.today()
	obj = open("frontOfLeague", "r")
	front = json.loads(obj.read())
	obj.close()
	posting_str = ""
	for post in front:
		posting_str += post[0] + " :: " + str(post[1]) + "\n\n"
	r.submit(SUBREDDIT, "Front of league for %s."%datetime.date.today(), text=posting_str)
	os.remove("frontOfLeague")

while True:
	try:
		main()
		if not "LAST_CLEARED" in globals():
			poster()
		elif (LAST_CLEARED - datetime.date.today()).days >= 1:
			poster()
		time.sleep(100)
	except:
		time.sleep(100)