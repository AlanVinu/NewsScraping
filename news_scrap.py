import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import os.path

new_news=0

##Manorama
front_page=requests.get("https://www.onmanorama.com/home.html")
soup = BeautifulSoup(front_page.content, 'html.parser')

main_news = soup.find_all('figcaption',attrs={'class':'image-overlay-bottom'})

if os.path.isfile('C:/Users/Alan/Desktop/NewsData.csv'):
    df = pd.read_csv('C:/Users/Alan/Desktop/NewsData.csv')
    main_news_headlines=list(df['Headline'])
    main_news_body=list(df['Body'])
    links=list(df['Link'])
    date=list(df['Date'])
    time=list(df['Time'])
    authors=list(df['Author'])
    source=list(df['Source'])
    #main_news_body=[news.strip() for news in main_news_body]
else:
    main_news_headlines=[]
    main_news_body=[]
    links=[]
    date=[]
    time=[]
    authors=[]
    source=[]

for news in main_news:
    if news.find('h3',attrs={'class':'para-mediunm-ml'}) is not None:
        headlines=news.find('h3',attrs={'class':'para-mediunm-ml'})
        link=news.find('a').get('href')
        if link not in links:
            new_news=1
            main_news_headlines.append(headlines.text.strip())
            links.append(link)
            source.append("Manorama")
            print("\n",headlines.text.strip(), sep='')
            print("Link :",link)
            report=requests.get(link)
            report_soup=BeautifulSoup(report.content, 'html.parser')
            if report_soup.find('span',attrs={'class':'story-author-name'}) is not None:
                author=report_soup.find('span',attrs={'class':'story-author-name'})
                author=author.find('span',attrs={'itemprop':'name'})
                authors.append(author.text)
            else:
                authors.append('')
            datentime=report_soup.find('time',attrs={'class':'story-author-date'}).get('content')
            date.append(datetime.fromisoformat(datentime).date())
            time.append(datetime.fromisoformat(datentime).time())
            if report_soup.find('div',attrs={'class':'article rte-article'}) is not None:
                paras=report_soup.find('div',attrs={'class':'article rte-article'})
                paras=paras.find_all('p',text=None)
                news_body=str()
                for para in paras:
                    try:
                        news_body+=' '+para.text.strip()
                    except:
                        pass
                news_body=news_body.replace(' ','',1)
                main_news_body.append(news_body)
print("\n\t\t\t TOP NEWS\n")
if soup.find('div',attrs={'class':'news-list-ml'}) is not None:
    top_news = soup.find('div',attrs={'class':'news-list-ml'}).find_all('a')
    for news in top_news:
        link=news.get('href')
        if link not in links:
            new_news=1
            main_news_headlines.append(news.get('title'))
            links.append(link)
            source.append("Manorama")
            print("\n",news.get('title'), sep='')
            print("Link :",link)
            report=requests.get(link)
            report_soup=BeautifulSoup(report.content, 'html.parser')
            if report_soup.find('span',attrs={'class':'story-author-name'}) is not None:
                author=report_soup.find('span',attrs={'class':'story-author-name'})
                author=author.find('span',attrs={'itemprop':'name'})
                authors.append(author.text)
            else:
                authors.append('')
            print(author.text)
            datentime=report_soup.find('time',attrs={'class':'story-author-date'}).get('content')
            date.append(datetime.fromisoformat(datentime).date())
            time.append(datetime.fromisoformat(datentime).time())
            if report_soup.find('div',attrs={'class':'article rte-article'}) is not None:
                paras=report_soup.find('div',attrs={'class':'article rte-article'})
                paras=paras.find_all('p',text=None)
                news_body=str()
                for para in paras:
                    try:
                        news_body+=' '+para.text
                    except:
                        pass
                news_body=news_body.replace(' ','',1)
                main_news_body.append(news_body)

##Mathrubhumi

##print("Date Length\t:",len(date))
##print("Time Length\t:",len(time))
##print("Authors Length  :",len(authors))
##print("Headline Length :",len(main_news_headlines))
##print("Body Length     :",len(main_news_body))
##print("Source Length   :",len(source))
##print("Link Length\t:",len(links))

if new_news==1:
    df = pd.DataFrame(list(zip(date,time,authors,main_news_headlines,main_news_body,source,links)),
                      columns =['Date','Time','Author','Headline', 'Body', 'Source','Link'])
    df = df.drop_duplicates(subset='Link', keep='last')
    df.to_csv('NewsData.csv', index = False)
print("\n\n\t\t\tEND")
input()
#df['Date']=datetime.now().date()
#df['Time']=datetime.now().time().isoformat('seconds')
