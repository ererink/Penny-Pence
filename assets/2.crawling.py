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
from time import sleep # 대기시간

def start_selenium(sectors):
    
    browser = webdriver.Chrome("./chromedriver.exe")
    browser.get("https://finance.naver.com/news/news_search.naver?rcdate=&q=%BB%EF%BC%BA%C0%FC%C0%DA&x=12&y=14&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd=2023-02-12")

    # 검색어 입력
    element = browser.find_element(By.CLASS_NAME, "inputTxt")
    element.clear()
    element.send_keys(sectors)

    # 제목 검색 클릭
    title_click = browser.find_element(By.XPATH, '//*[@id="schoption02"]')
    title_click.click()

    # 날짜 입력
    start_date = browser.find_element(By.NAME, 'stDateStart')
    start_date.clear()
    sleep(0.5)
    start_date.send_keys('2010-01-01')
    sleep(0.5)
    end_date = browser.find_element(By.NAME, 'stDateEnd')
    sleep(0.5)
    end_date.clear()
    sleep(0.5)
    end_date.send_keys('2019-12-31')

    # 검색버튼 클릭
    search = browser.find_element(By.XPATH, '//*[@id="contentarea_left"]/form/div/div/div/input[2]')
    search.click()

    # 맨 끝페이지로 이동
    end = browser.find_element(By.XPATH, '//*[@id="contentarea_left"]/table/tbody/tr/td[12]')
    end.click()

    # 현재 url 가져오기
    url = browser.current_url
    # url = stDateStart=2010-01-01&stDateEnd=2019-12-31&page=11 
    index = url.find("page=") # page= 뒤에 숫자를 가져오기 위해 index 저장

    page_range = url[index+5:] # page= 숫자 저장

    url = url.replace(f'{url[index:]}', '') # page 제거

    scrape_sector_news(url, page_range)



# soup 분리하기
def create_soup(page_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
    res = requests.get(page_url, headers=headers) # url 입력
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    
    return soup

def scrape_sector_news(url, page_range):
    
    # 날짜 변환
    # url = "https://finance.naver.com/news/news_search.naver?rcdate=&q=%C4%AB%C4%AB%BF%C0&x=18&y=11&sm=all.basic&pd=1&stDateStart=" + DateStart + "&stDateEnd=" + DateEnd
    # url = url.replace("1997-01-01", "2010-01-01")
    # url = url.replace("2023-02-17", "2019-12-31") # 오늘날짜 기준

    page_range = int(page_range)
    # 기본 url
    base_url = "https://finance.naver.com/"
    if page_range > 200:
        page_range = 200

    for i in range(page_range, 0, -1):
        
        # 최신순으로 가져오기 위해 거꾸로 탐색
        page_url = url + f'page={i}'
        print(page_url)
        # create_soup 함수 사용
        soup = create_soup(page_url) 

        # 뉴스 리스트 가져오기
        news_li = soup.find_all('dl', attrs={"class":"newsList"})

        for news in news_li:
            # 뉴스제목, 내용, 날짜 출력
            test_title = news.find('dd', attrs={"class" : "articleSubject"})
            test_content = news.find('dd', attrs={"class": "articleSummary"})
            test_date = news.find('dd', attrs={"class": "articleSummary"})
            test_link = news.find('dd', attrs={"class": "articleSubject"})
            
            # None값 필터링
            if test_title and test_content and test_date and test_link is not None:
                title = test_title.find('a').get_text().strip()
                content = test_content.get_text().strip()
                date = test_date.find('span', attrs={"class": "wdate"}).get_text().strip()
                link = base_url + test_link.find('a')['href']
                year_month = date[:7] # 필터 걸어줄 날짜

                # 중복 제목, 거래량 뉴스 필터링 and 한 달에 한개만 가져올 수 있도록 조건문 설정
                if (title not in news_title_list and filter_list.count(year_month) < 1 
                    and "한국경제TV" not in content):

                    news_title_list.append(title)
                    news_content_list.append(content)
                    news_date_list.append(date) 
                    news_link_list.append(link)
                    filter_list.append(year_month) # 2019-12
            else:
                title = "No title"

            

if __name__ == "__main__":
    
    # 크롤링할 기업리스트
    queue_list = ["카카오", '포스코ICT', "현대차", '기아', '현대모비스', 'NC소프트', '컴투스', '위메이드', 'JYP', 'YG플러스', 'SM']
    # 크롤링 완료
    # ["삼성전자 반도체", "하이닉스", 'LG디스플레이', '셀트리온', '유한양행', '신풍제약', '네이버', ]
    queue = deque()

    for i in queue_list:
        queue.append(i)

    while queue:
        news_title_list = []
        news_content_list = []
        news_date_list = []
        news_link_list = []
        filter_list = []
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
        news_df.to_csv('{}_{}.csv'.format(sectors, now.strftime('%Y%m%d_%H시%M분%S초')),
                      columns=['date', 'title', 'link', 'content'],  # 열 순서를 지정
                      encoding='utf-8-sig',  # 인코딩 설정
                      index=False)  # 인덱스를 CSV 파일에 포함하지 않음



