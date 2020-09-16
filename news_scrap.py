import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import os.path
from dateutil import parser,tz
import warnings
warnings.filterwarnings("ignore")

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
#print("\n\t\t\t TOP NEWS\n")
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
            #print(author.text)
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

def getreport(link):
    main_report = requests.get(link)
    main_report_soup = BeautifulSoup(main_report.content, 'html.parser')
    news_body=str()
    if main_report_soup.find('div',{'class':'col-md-9 col-sm-9 col-xs-12 col-md-offset-3 col-sm-offset-3 articleBody common_text'}) is not None:
        paras = main_report_soup.find('div',
                                      {'class':'col-md-9 col-sm-9 col-xs-12 col-md-offset-3 col-sm-offset-3 articleBody common_text'})
        paras = paras.find('div',{'class':'col-md-12 col-sm-12 col-xs-12'})
        paras = paras.find_all('p')
        for para in paras:
            try:
                news_body+=' '+para.text
            except:
                pass
        news_body=news_body.replace(' ','',1)
    datentime = str()
    if main_report_soup.find('div',{'class':'common_text_en date_outer'}) is not None:
        datentime = main_report_soup.find('div',{'class':'common_text_en date_outer'})
        #print(datentime)
        datentime = datentime.text.strip('\n')
        default_date=datetime(2020,9,15,tzinfo=tz.gettz('Asia/Calcutta'))
        datentime = parser.parse(datentime,default=default_date)
    author = str()
    if main_report_soup.find('div',{'class':'common_text author_text'}) is not None:
        author = main_report_soup.find('div',{'class':'common_text author_text'}).text.strip().strip('# ')
    
    return news_body, datentime, author
    
front_page=requests.get("https://english.mathrubhumi.com/")
soup = BeautifulSoup(front_page.content, 'html.parser')

main = soup.find('div',{'class':'topSt'})
main_title = main.find('a',{'class':'common_text maintitle'}).get_text().strip()
link = 'https://english.mathrubhumi.com'+main.find('a').get('href')
if link not in links:
    new_news=1
    main_news_headlines.append(main_title)
    links.append(link)
    source.append("Mathrubhumi")
    print("\n",main_title, sep='')
    print("Link :",link)
    news_body, datentime, author = getreport(link)
    main_news_body.append(news_body)
    authors.append(author)
    if datentime is not str():
        date.append(datentime.date())
        time.append(datentime.time())
    else:
        date.append('')
        time.append('')
all_news = soup.find('ul',{'class':'bullets'})
all_news = all_news.find_all('a',{'class':'common_text bulletpoints'})
side_panel = soup.find('div',{'class':'col-md-4 col-sm-4 col-xs-12 ipadmaincol'})
side_panel_news = side_panel.find_all('a',{'class':'common_text bulletpoints'})
#print("\n\n",all_news)
all_news.extend(side_panel_news)
#print("\n\n",all_news)
for news in all_news:
    link = "https://english.mathrubhumi.com"+news.get('href')
    title = news.text.strip()
    if link not in links:
        new_news=1
        main_news_headlines.append(title)
        links.append(link)
        source.append("Mathrubhumi")
        print("\n",title, sep='')
        print("Link :",link)
        news_body, datentime, author = getreport(link)
        main_news_body.append(news_body)
        authors.append(author)
        if datentime is not str():
            date.append(datentime.date())
            time.append(datentime.time())
        else:
            date.append('')
            time.append('')
        
##Output

if new_news==1:
    df = pd.DataFrame(list(zip(date,time,authors,main_news_headlines,main_news_body,source,links)),
                      columns =['Date','Time','Author','Headline', 'Body', 'Source','Link'])
    df = df.drop_duplicates(subset='Link', keep='last')
    df.to_csv('NewsData.csv', index = False)
print("\n\n\t\t\tEND")
input()
#df['Date']=datetime.now().date()
#df['Time']=datetime.now().time().isoformat('seconds')
