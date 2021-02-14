from django.shortcuts import render
import tweepy 
import json
from datetime import date 
from datetime import timedelta 
import os
import subprocess
import multiprocessing
from multiprocessing import Process,Pool
import base64

consumer_key = "Gev6j79CMF18IYTgMepO1IlJV" 
consumer_secret = "DqbksdWSNXYvIMBFMXzvYHlD7HfJs0X5OhTqtg7SUgJ64DEgMu" 
access_token = "926819010288656387-WTeeYlVeV0IdE2q83BrRUClgtRPnfwC" 
access_token_secret = "zJs1khFyE2HXuPhViOy7C5uDDogkEonE5snqlPq435J8I"

consumer_key1="ppGPO0Z5JekRF15V596TraNNL"
consumer_secret1="P3svmqEQnvcDAkN8dXsgoPQmFvAtuiWWNW30QvcJhzyHagOxUA"
access_token1="926819010288656387-vFkenC2ya8nekSiF0RbHykYzrg9Edjz"
access_token_secret1="6UZASrp3nL5VegGIYhEuxvxO9Yg41Z82zfVvEOyJVKOl7"


def getTrends():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 
    woeid=2295386
    trends=api.trends_place(woeid)
    tr=[]
    for i in range(10):
        print(trends[0]['trends'][i]['name'])
        tr.append(trends[0]['trends'][i]['name'])
    return tr

def startpage(request):
    tr=getTrends()
    return render(request,'index.html',{ 'trend': tr})

def pagerank(request):
    if(request.POST):
        hashtag=list(request.POST)[1]
        filename="--file="+hashtag+".json"
        test = subprocess.Popen(["python3","main.py",filename,], stdout=subprocess.PIPE)
        output = test.communicate()[0]
        print("fsfsklfjs")
        r=str(output.decode('utf-8'))
        ranks=r.split("\n")
        print(ranks)
        name=[]
        score=[]
        ans=[]
        for i in ranks[:-2]:
            print(i)
            l=i.split(" ")
            k=[]
            k.append(l[1])
            k.append(l[3])
            ans.append(k)
            name.append(l[1])
            score.append(l[3])
        tr=getTrends()
        filename=str(hashtag+".png")
#        with open(filename, "rb") as image_file:
#            image_data = base64.b64encode(image_file.read()).decode('utf-8')
#        ctx = image_data
        return render(request,'pageranked.html',{'rank':ans,'trend':tr,'hashtag':hashtag })
        
def startcrawler(request):

    tr=getTrends()
    tr1=tr[:2]
    tr2=tr[2:4]
    tr3=tr[4:6]
    tr4=tr[6:8]
    tr5=tr[8:]
    trs=[]
    trs.append(tr1)
    trs.append(tr2)
    trs.append(tr3)
    trs.append(tr4)
    trs.append(tr5)
    pool=multiprocessing.Pool()
    output=pool.map(crawler,trs)
    print(output)

def crawler(tr):
    print(tr)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth)

    auth1=tweepy.OAuthHandler(consumer_key1, consumer_secret1)
    auth1.set_access_token(access_token1, access_token_secret1) 
    api1=tweepy.API(auth1)

    hashtag=tr[0]
    today = date.today() 
    yesterday = today - timedelta(days = 1) 
    date_since=yesterday

    filename=hashtag+".json"
    
    print("start")
    tweets = tweepy.Cursor(api.search, q=hashtag, lang="en", since=date_since, tweet_mode='extended').items(1000) 
    f=open(filename,'w')

    for i in tweets:
        js=json.dumps(i._json)
        f.write(js+"\n") 

    hashtag1=tr[1] 
    today = date.today() 
    yesterday = today - timedelta(days = 1) 
    date_since=yesterday

    filename1=hashtag1+".json"
    
    print("start")
    tweets1 = tweepy.Cursor(api1.search, q=hashtag1, lang="en", since=date_since, tweet_mode='extended').items(1000) 
        
    f1=open(filename1,'w')

    for i in tweets1:
        js=json.dumps(i._json)
        f1.write(js+"\n") 
    
    return 1





'''def check(request):
    if(request.POST):
        print(list(request.POST)[1])
        hashtag=list(request.POST)[1]
        print(hashtag)
        today = date.today() 
        yesterday = today - timedelta(days = 1) 
        date_since=yesterday

        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)     
        auth.set_access_token(access_token, access_token_secret) 
        api = tweepy.API(auth) 

        print("start")
        tweets = tweepy.Cursor(api.search, q=hashtag, lang="en", since=date_since, tweet_mode='extended').items(1000) 

        for i in tweets:
            tw=i._json
            print(i._json)
            break
        print(tw["full_text"])
        print(tw['created_at'])
        print(tw['entities']['user_mentions'])
        print(tw['entities']['hashtags'])
        print(tw['entities']['urls'])
        print(tw['user'])
        print(tw['retweet_count'])
        print(tw['id'])

        f=open('newsample.json','w')

        for i in tweets:
            js=json.dumps(i._json)
            f.write(js+"\n")
        
        return render(request,'pageranked.html')        
'''    
'''
def getdetails(request):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
        
    auth.set_access_token(access_token, access_token_secret) 
    

    api = tweepy.API(auth) 
    woeid=2295386
    trends=api.trends_place(woeid)
    tr=[]
    for i in range(10):
        print(trends[0]['trends'][i]['name'])
        tr.append(trends[0]['trends'][i]['name'])

    for i in tr:
        hashtag=i
        today = date.today() 
        yesterday = today - timedelta(days = 1) 
        date_since=yesterday

        filename=hashtag+".json"
        if(os.path.isfile(filename)):
            print("fileexist")
        else:
            print("start")
            tweets = tweepy.Cursor(api.search, q=hashtag, lang="en", since=date_since, tweet_mode='extended').items(1000) 
            
            f=open(filename,'w')

            for i in tweets:
                js=json.dumps(i._json)
                f.write(js+"\n")
    return 1

'''
