import requests
from bs4 import BeautifulSoup
import urllib
import datetime

# 데이터 프레임 엑셀 생성
from collections import deque
import pandas as pd

# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # 키입력

def start_selenium(sectors):
    
    browser = webdriver.Chrome("./chromedriver.exe")
    browser.get("https://finance.naver.com/news/news_search.naver?rcdate=&q=%BB%EF%BC%BA%C0%FC%C0%DA&x=12&y=14&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd=2023-02-12")

    element = browser.find_element(By.CLASS_NAME, "inputTxt")
    element.clear()
    element.send_keys(sectors)

    search = browser.find_element(By.XPATH, '//*[@id="contentarea_left"]/form/div/div/div/input[2]')
    search.click()

    # 현재 url 가져오기
    url = browser.current_url
    scrape_sector_news(url)



# soup 분리하기
def create_soup(page_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
    res = requests.get(page_url, headers=headers) # url 입력
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    
    return soup

def scrape_sector_news(url):
    # 검색하고자 하는 섹터 url
    DateStart = "2010-01-01"
    DateEnd = "2019-12-31"
    
    # 날짜 변환
    # url = "https://finance.naver.com/news/news_search.naver?rcdate=&q=%C4%AB%C4%AB%BF%C0&x=18&y=11&sm=all.basic&pd=1&stDateStart=" + DateStart + "&stDateEnd=" + DateEnd
    url = url.replace("1997-01-01", "2010-01-01")
    url = url.replace("2023-02-13", "2019-12-31") # 오늘날짜 기준
    url = url.replace("all", "title") # 제목에 해당하는 것만 필터링


    # 기본 url
    base_url = "https://finance.naver.com/"

    for i in range(2, 30):
        
        page_url = url + f"&page={i}"
        # create_soup 함수 사용
        soup = create_soup(page_url) 

        # 뉴스 리스트 가져오기
        news_li = soup.find_all('dl', attrs={"class":"newsList"})

        for news in enumerate(news_li):
          # 뉴스제목, 내용, 날짜 출력
          title = news.find('dd', attrs={"class" : "articleSubject"}).find('a').get_text().strip()
          content = news.find('dd', attrs={"class": "articleSummary"}).get_text().strip()
          date = news.find('dd', attrs={"class": "articleSummary"}).find('span', attrs={"class": "wdate"}).get_text().strip()
          link = base_url + news.find('dd', attrs={"class": "articleSubject"}).find('a')['href']
          
          # 중복 뉴스 필터링
          if title not in news_title_list:
              
              news_title_list.append(title)
              news_content_list.append(content)
              news_date_list.append(date)
              news_link_list.append(link)

if __name__ == "__main__":
    
    # 크롤링할 기업리스트
    queue_list = ["삼성전자", "하이닉스", 'LG디스플레이', '셀트리온', '유한양행', '신풍제약', '네이버', "카카오", '포스코ICT', "현대차", '기아', '현대모비스', 'NC소프트', '컴투스', '위메이드', 'JYP', 'YG플러스', 'SM']
    queue = deque()

    for i in queue_list:
        queue.append(i)

    while queue:
        news_title_list = []
        news_content_list = []
        news_date_list = []
        news_link_list = []
        sectors = queue.popleft()

        # selenium 시작
        start_selenium(sectors)

        #데이터 프레임 만들기
        news_df = pd.DataFrame({'date':news_date_list, 'title':news_title_list, 'link':news_link_list, 'content':news_content_list})

        #중복 행 지우기
        news_df = news_df.drop_duplicates(keep='first',ignore_index=True)
        print("중복 제거 후 행 개수: ",len(news_df))

        #데이터 프레임 저장
        now = datetime.datetime.now() 
        news_df.to_csv('{}_{}.csv'.format(sectors, now.strftime('%Y%m%d_%H시%M분%S초')), encoding='utf-8-sig',index=False)



