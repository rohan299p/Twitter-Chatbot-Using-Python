import tweepy #Python Library to communicate with Twitter platform and use its API.
import time
#import atexit 
import sys    #use to access system-specific parameters and functions.
#import random 
from random_words import RandomWords  #generate random words
from PyDictionary import PyDictionary #Dictionary Module for Python to get meanings, translations, synonyms
import datetime #work with date and time.
import schedule #schedule some tasks at particular time interval
import requests #library for making HTTP requests in Python
from lxml import html #provides a special Element API for HTML elements

print('Hey, SLASH here! A twitter bot.')

#API keys
CONSUMER_KEY='JkCAwpR61ACt4uAPNXE60J5kM'
CONSUMER_SECRET='wZELp6zTjvBxhWjMVaRhJ3DP7BpOg0Utx9v9jQlQynOncPJr58'
ACCESS_KEY='1317182765385699328-wOlhsgnlYDQgQnlIKYVLatzqSW3gUO'
ACCESS_SECRET='05S3TQQRHZEmiSSIweCN2kesthcItZO5jcq39TQUgDi34'

#authentication and access
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) 
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)


# image='bot.jpg'
''' ---------------------------------------------Backup Code for Status Update-------------------------------------------
def postStatus(update):
    try:
        api.update_status(update)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            # Do something special
            print('Duplicate Message')
postStatus("Hello ,ChatBotSDL is Online Now")
'''

#get current date and time 
def getDatetime():
    now = datetime.datetime.now()
    return now


#tweet word and meaning every day 10:00 am
def tweetDictionary():

    dictionary = PyDictionary()
    rw = RandomWords()

    word = rw.random_word()
    definitions = dictionary.meaning(word)     # definitions is dictionary of two items (noun,verb)

    # print('\nWord : ',word, '\nDefinitions : ', definitions)
    # F-strings provide a way to embed expressions inside string literals, using a minimal syntax

    now = getDatetime()
    tweet = f'''Word of the Day
    Date: {now.strftime("%y-%m-%d")}
    Word: {word}
    Meaning: {definitions}
    Source: "PyDictionary"
    '''
    size = sys.getsizeof(tweet)
    print('Dictionary tweet size: ', size)

    if size < 362:
        api.update_status(tweet)
        print('Word tweeted successfully')
    else:
        print('error, loading again')
        tweetDictionary()
   
schedule.every().day.at("11:25").do(tweetDictionary)


#tweet coronavirus cases updates everyday 11:30 pm
def covid19Update():
    # proxyDict = {
    #     'http' : "add http proxy",
    #     'https' : "add https proxy"
    # }

    res = requests.get("https://www.worldometers.info/coronavirus/country/india/")
    doc = html.fromstring(res.content)
    totalCases, totalDeaths, totalRecovered =doc.xpath('//div[@class="maincounter-number"]/span/text()')

    todayInfo = doc.xpath('//li[@class="news_li"]/strong/text()')

    # print('\nConfirmed cases : ',todayInfo[0],'\nDeaths : ', todayInfo[1])
    # print('\nTotal cases : ',totalCases,'\nTotal Recovered : ', totalRecovered,'\nTotal Deaths : ', totalDeaths)

    now = getDatetime()

    tweet1 = f'''India: Coronavirus Latest Updates
    Date: {now.strftime("%y-%m-%d")}  Time: {now.strftime("%H:%M:%S")}
    Confirmed cases: +{todayInfo[0]}
    Deaths: +{todayInfo[1]}
    Source: https://www.worldometers.info/coronavirus/country/india/

    #coronavirus #covid19 #coronavirusnews #coronavirusupdates
    '''

    tweet2 = f'''India: Coronavirus Latest Updates
    Date: {now.strftime("%y-%m-%d")}  Time: {now.strftime("%H:%M:%S")}
    Total cases: {totalCases}
    Recovered: {totalRecovered}
    Deaths: {totalDeaths}
    Source: https://www.worldometers.info/coronavirus/country/india/

    #coronavirus #covid19 #coronavirusnews #coronavirusupdates
    '''

    # size1 = sys.getsizeof(tweet1)
    # size2 = sys.getsizeof(tweet2)
    # print(size1,size2)
    
    api.update_status(tweet1)
    api.update_status(tweet2)
    print('Covid19 Status updated successful')

schedule.every().day.at("11:25").do(covid19Update)


def botOffline():
    while(True):
        now = getDatetime()
        tweet = f'''Date: {now.strftime("%y-%m-%d")}
        Time: {now.strftime("%H:%M:%S")}  
        Bot Status - Offline
        '''

        print('Bot Offline')
        api.update_status(tweet)
        break


#update bot status by tweeting
def botOnline():
    now = getDatetime()
    tweet = f'''Date: {now.strftime("%y-%m-%d")}
    Time: {now.strftime("%H:%M:%S")}  
    Bot Status - Online
    '''

    print('Bot Online')
    api.update_status(tweet)


file_name = 'last_seen_id.txt'
#get latest mention id
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


#store latest mention id
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


#like tweets of users whom our chatbot follows check every minute
def auto_like_followers():
    maxLimit = 5
    for tweet in tweepy.Cursor(api.home_timeline).items(maxLimit):
        try:
            tweet.favorite()
            print("tweet liked of friend whom I follow !")
        except tweepy.TweepError as error:
            if error.api_code == 139:
                print('no new tweets from users which I follow !')
        except StopIteration:
            break
schedule.every(1).minutes.do(auto_like_followers)


#like, retweet, dm and follow who mentions our bot (checks every 15 seconds)
def reply_to_tweets():
    FOLLOW= True
    message='Hello Sir , Feel Free to Drop your feedbacks to this DM'
    print('retrieving and replying to tweets...', flush=True)

    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.

    mentions = api.mentions_timeline(retrieve_last_seen_id(file_name), tweet_mode='extended')
    for mention in reversed(mentions):

        #store_last_seen_id(last_seen_id, file_name)
        if '#hellobot' in mention.full_text.lower() :
            #print(str(mention.id) + ' - ' + mention.full_text, flush=True)
            try:
                if '#like' not in mention.full_text.lower() and '#retweet' not in mention.full_text.lower() :
                    print(str(mention.id)+ ' - '+mention.full_text)
                    api.update_status('@' + mention.user.screen_name + 'Hello, Back To You, Auto-Reply Works !', mention.id)
            except tweepy.TweepError as error:
                if error.api_code == 187:
                    # Do something special
                    print('Duplicate Message')
                else:
                    raise error
            try:
                if '#like' in mention.full_text.lower() and '#retweet' not in mention.full_text.lower():
                    try:
                        print(str(mention.id)+ ' - '+mention.full_text)
                        api.update_status('@' + mention.user.screen_name + 'Hello, Back To You, Auto-Reply And Auto-Like Works !', mention.id)
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            # Do something special
                            print('Duplicate Message')
                        else:
                            raise error
                    if not mention.favorited:
                        api.create_favorite(mention.id)
                if '#retweet' in mention.full_text.lower() and '#like' not in mention.full_text.lower() :
                    try:
                        print(str(mention.id)+ ' - '+mention.full_text)
                        api.update_status('@' + mention.user.screen_name + 'Hello, Back To You, Auto-Reply And Auto-Retweet Works !', mention.id)
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            # Do something special
                            print('Duplicate Message')
                        else:
                            raise error
                    if not mention.retweeted:
                        api.retweet(mention.id)
                if '#retweet' in mention.full_text.lower() and '#like' in mention.full_text.lower() :
                    try:
                        print(str(mention.id)+ ' - '+mention.full_text)
                        api.update_status('@' + mention.user.screen_name + 'Hello, Back To You, Auto-Reply ,Auto-Like And Auto-Retweet Works !', mention.id)
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            # Do something special
                            print('Duplicate Message')
                        else:
                            raise error
                    if not mention.retweeted:
                        api.retweet(mention.id)
                    if not mention.favorited:
                        api.create_favorite(mention.id)
                if FOLLOW:
                    if not mention.user.following:
                        mention.user.follow()
                        print('Followed the user')


            except tweepy.TweepError as error:
                if error.api_code == 139:
                        print('Already Liked and Retweeted')
                else:
                    raise error
            try:
                recipient_id=mention.user.id
                direct_message=api.send_direct_message(recipient_id,message)
                print(direct_message.message_create['message_data']['text'])

            except tweepy.TweepError as error:
                        if error.api_code == 349:
                            # Do something special
                            print('User Has Denied Permission')
            store_last_seen_id(mention.id, file_name)


botOnline() #bot started
while True:
    reply_to_tweets()      #reply to tweets 
    schedule.run_pending() #check for pending scheduled tweets
    '''
    try:
        sys.exit( tweetOffline() )
        {
            print("Exiting")
        }
    except SystemExit:
        print ('--------------------------------------')
    '''
    time.sleep(15)




