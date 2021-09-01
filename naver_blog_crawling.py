from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

#블로그 url 크롤링
url_list = []
for i in range(1,8) :
    url2 = f'https://blog.naver.com/PostSearchList.naver?blogId=jjong0496&categoryNo=0&SearchText=%EA%B5%AD%EB%82%B4+%EA%B4%91%EA%B3%A0+%EC%B9%B4%ED%94%BC+%EB%AA%A8%EC%9D%8C&orderBy=date&term=&startDate=&endDate=&range=all&cpage={i}'

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url2, headers=headers)
    res.raise_for_status() # 문제시 프로그램 종료
    soup = BeautifulSoup(res.text, "lxml")

    links = soup.select('a.s_link')

    for l in links :
        link = l.get('href')
        url_list.append(link)
print(len(url_list))


# 네이버 블로그 iframe 제거 함수
def delete_iframe(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()  # 문제시 프로그램 종료
    soup = BeautifulSoup(res.text, "lxml")

    src_url = "https://blog.naver.com/" + soup.iframe["src"]  # iframe 안에 있는 src 부분을 가져옴

    return src_url


# 네이버 블로그 글 크롤링 함수
def text_scraping(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()  # 문제시 프로그램 종료
    soup = BeautifulSoup(res.text, "lxml")

    if soup.select_one('div.se-main-container'):
        text = soup.select_one('div.se-main-container').text
        text = text.replace('\n', '')
        # print("블로그")
        return text
    elif soup.select_one('div#postViewArea'):
        text = soup.select_one('div#postViewArea').text
        text = text.replace('\n', '')
        # print('블로그 2.0')
        return text
    else:
        return "확인불가"


#네이버 블로그 글 크롤링
import requests
import re #추가
from bs4 import BeautifulSoup
from urllib.parse import quote

blog_list =[]
for i in url_list :
    post_link = i
    blog_text = text_scraping(delete_iframe(post_link))
    blog_list.append(blog_text)
    print('#',end='')
print('완료')

#회사, 문구, 카테고리 나누기
cnt = 0 #오류 확인용 카운트
copy_list = []
company_list = []
category_list = []
for b in blog_list:
    print(cnt, end=',')

    text = b.split('<')
    text.pop(0)  # 처음 공백 제거

    for i in text:  # 카테고리 분류
        try:
            i = i.split('>')
            category = i[0]
            # print(category)
            copy_ = i[1].split(')')
            copy_.pop(len(copy_) - 1)  # 마지막 공백 제거
        except:
            print('카테고리 오류', end='/')
            continue

        for j in copy_:  # copy 분류
            try:
                j = j.split('(')
                # print(j)
                copy = j[0]
                company = j[1]

                copy_list.append(copy)
                company_list.append(company)
                category_list.append(category)
            except:
                print('인덱싱 오류', end='/')

    cnt += 1
print('나누기 완료')
df = pd.DataFrame({'company': company_list, 'copy': copy_list, 'category': category_list})
df.info()
df.to_csv('company_and_copy2.csv', encoding='utf-8-sig')
print('저장 완료')


