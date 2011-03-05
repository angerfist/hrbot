#!/usr/bin/python

import os, twitter, time, getopt, random, sys, traceback, ConfigParser

e = {'test': False, 'min': 15*60, 'max': 60*60, 'forced': False, 'offline': False}

def main():
    try:
        options = getopt.gnu_getopt (sys.argv[1:], 'tofm:M:')
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
        
    for o, v in options[0]:
        if o == "-t":
            e['test'] = True
        elif o == "-m":
            e['min'] = int(v)
        elif o == "-M":
            e['max'] = int(v)
        elif o == "-f":
            e['forced'] = True
        elif o == "-o":
            e['offline'] = True



    api = None 
    print('Starting...')
    if (not e['offline']):
        config = ConfigParser.RawConfigParser()
        config.read('bot.cfg')
        api = twitter.Api(config.get('Authorization', 'consumer_key'),
                    config.get('Authorization', 'consumer_secret'),
                    config.get('Authorization', 'access_token_key'),
                    config.get('Authorization', 'access_token_secret'))
        print 'Friends: %s' % ([u.screen_name for u in api.GetFriends()])
        print 'Followers: %s' % ([u.screen_name for u in api.GetFollowers()])

    
    os.environ['TZ'] = 'Europe/Moscow'
    while 1 == 1:
        hour = time.localtime().tm_hour
        if e['forced'] or (hour >= 7 and hour <= 24):
            doPost(api)

        time.sleep(random.randint(e['min'], e['max']))



def doPost(api):
    quotesFile = open("./quotes.txt")
    quote = random.choice(quotesFile.readlines())
    try:
        user = random.choice(list(set(api.GetFriends() + api.GetFollowers()))).screen_name
    except:
        user = "TEST"
    message = '@'+user+' '+quote.decode('utf-8', 'ignore')
    if not e['test'] and not e['offline']:
        api.PostUpdate(message)

    print "Time: "+time.strftime("%Y.%m.%d %H:%M:%S", time.localtime()) + \
        ", Test: "+repr(e['test']) + \
        ", Message: "+message
    
    quotesFile.close()
        
if __name__ == "__main__":
    main()
