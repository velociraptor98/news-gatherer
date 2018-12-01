import bs4
import urllib
from collections import deque
import json

Hindu={} 
DailyMail={}
MoneyControl={}

def CrawlHindu():
    global Hindu
    HinduList=[]
    url='https://www.thehindu.com/todays-paper/'
    originallength=len(url)
    source=urllib.request.urlopen(url).read()
    soup=bs4.BeautifulSoup(source , 'html.parser')
    for temp in  soup.find_all('a',href=True):
        if(temp.get('href').startswith('https://www.thehindu.com/todays-paper/') and  not (temp.get('href').startswith('https://www.thehindu.com/todays-paper/tp-'))):
            HinduList.append(temp.get('href'))
    for li in HinduList:
        if(len(li)==originallength):
            continue
        else:
            head=urllib.request.urlopen(li).read()
            soup=bs4.BeautifulSoup(head,'html.parser')
            str=soup.title.string
            str2=str.replace('\n','').replace('- Today\'s Paper - The Hindu','').replace(',','')
            #str2=str.replace('- Today\'s Paper - The Hindu','')
            Hindu[str2]=[li,"The Hindu"]

def CrawlDailyMail():
    daily=set()
    global DailyMail
    url='https://www.dailymail.co.uk/home/latest/index.html#news'
    source=urllib.request.urlopen(url).read()
    soup=bs4.BeautifulSoup(source,'html.parser')
    for i in soup.find_all('a',href=True):
        if(i.get('href').startswith('/news/') and not (i.get('href').endswith('/index.html'))):
            str = ('https://www.dailymail.co.uk'+i.get('href'))
            daily.add(str)
    for i in daily:
        head=urllib.request.urlopen(i).read()
        soup=bs4.BeautifulSoup(head,'html.parser')
        str=soup.title.string
        str=str.replace('| Daily Mail Online','').replace(',','')
        DailyMail[str]=[i,'The Daily Mail']


def CrawlMoneyControl():
    global MoneyControl
    url='https://www.moneycontrol.com/news/news-all/'
    source=urllib.request.urlopen(url).read()
    soup=bs4.BeautifulSoup(source,'html.parser')
    relevant = soup.find_all('a',href=True)
    for i in relevant:
        if(i.get('href').startswith('https://www.moneycontrol.com/news/') and i.get('href').endswith('.html')):
                link=i.get('href')
                head=i.get('title').replace(',','')
                if(head=='See More'or head=='Opinion' or head=='Startups'):
                    continue
                MoneyControl[head]=[link,'Money Control']

def crawl():
    print('Collecting data from the hindu')
    CrawlHindu()
    print('Data fetched from Hindu')
    print('Headlines from the hindu: ',len(Hindu))
    print('Collecting data from dailyMail')
    CrawlDailyMail()
    print('Data Fetched From The daily Mail')
    print('Headlines from Daily Mail',len(DailyMail))
    print('Collecting Data from moneycontrol')
    CrawlMoneyControl()
    print('Data Collected from money control')
    print('Headlines from money control:',len(MoneyControl))
    Hindu.update(MoneyControl)
    Hindu.update(DailyMail) 
    with open('data.json','w') as fp:
            json.dump(Hindu,fp)   
    print('Analyzing the data ')

