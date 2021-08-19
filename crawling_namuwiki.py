from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException #오류가 있을 때 지나간다
import time
import chromedriver_autoinstaller
import subprocess
import shutil
import numpy as np

try:
    shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

#봇이 아닌 사람으로 인식하는 코드 / 자신의 크롬 위치 입력
subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)

driver.implicitly_wait(3)
start = time.time()

#파일 열기
df = pd.read_csv('./datasets/clean_data.csv',index_col=0)
df2 = pd.read_csv('./datasets/no_search.csv')
df2 = list(np.array(df2.no_search.tolist()))

explanes = []

count=0
for row in df.company[8000:]:
    print(row)

    #지역, 정부부처, 기타 캠페인 등 관련 없는 기업명은 제외
    if row in df2:
        other = 'other'
        explanes.append(other)

    else:
        url = f"https://namu.wiki/w/{row}"
        driver.get(url)

        try:
            same = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/article/div[3]/div[1]/ul/li/a').text

            #동음이의어가 존재할 경우 원하는 정보를 긁어오지 않음, 예외로 뺴기 (분류에 동음이의어/* 여부)
            if '동음이의어' in same:
                explane = 'same'
                explanes.append(explane)

            #아닐 경우 그대로 진행
            else :
               try:
                    explane = driver.find_element_by_css_selector('div.wiki-heading-content').text
                    explanes.append(explane)
                    #print(explane)

                except:
                    explane = 'NaN'
                    explanes.append(explane)

        #분류에 동음이의어가 없을 경우 원래대로 진행행
        except:
           try:
                explane = driver.find_element_by_css_selector('div.wiki-heading-content').text
                explanes.append(explane)
                #print(explane)

            except:
                explane = 'NaN'
                explanes.append(explane)
    count += 1
    if count % 100 == 0 :
        print('.',end='')
    if count % 500 == 0 :
        print('/', end='')
        df = pd.DataFrame({'explanes': explanes})
        df.to_csv('explanes_8000.csv')

print('완료')
df = pd.DataFrame({'explanes':explanes})
df.info()
df.to_csv('explanes_8000.csv')