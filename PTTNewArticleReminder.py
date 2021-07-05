# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 17:23:39 2021

@author: Arthur

# Python網頁爬蟲結合LINE Notify打造自動化訊息通知服務
# https://www.learncodewithmike.com/2020/06/python-line-notify.html

"""

from bs4 import BeautifulSoup
import requests
import time

# TOKEN 設定
codeJobTOKEN = "Put Your Token Here"
sohoTOKEN = "Put Your Token Here"

# 看板設定
codeJob = "https://www.ptt.cc/bbs/CodeJob/index.html"
soho = "https://www.ptt.cc/bbs/soho/index.html"


# 寫log檔用
def writeLog(inputString):
    f = open("log.txt", "a")
    f.write(inputString) # log
    f.close()

writeLog("[Info] Program start : " + time.asctime() ) # log





# 獲取文章
def getTopic(target_url,keyword):
    
    #爬取網頁資訊，try catch 預防斷線造成程式終止
    try:
        result = requests.get(target_url)
    except:
        writeLog("[warning] Network errer : " + time.asctime() )
        return []
    
    
    # 預防斷線沒status code造成程式終止
    try:
        if(result.status_code != 200):
            writeLog("[warning] Status error : " + str(result.status_code))
    except:
        return []
    
    
    #網頁資訊並給bs4解析，選出符合的區段給temp
    soup = BeautifulSoup(result.text,'lxml')
    temp = soup.select("div.title a") #這是有所有文章的list
    
    # 用來暫存符合的文章
    tempTopicList = []
    
    #找該頁不含re(回文)且符合[發案]開頭的文章，並存起來
    for i in range(len(temp)):
        if '['+keyword+']' in temp[i].text and 'Re' not in temp[i].text:
            tempTopicList.append( temp[i].text + "\nhttps://www.ptt.cc" + temp[i].attrs['href'] ) #temp[0].text --> '[問卦] 黎清波的八卦' & temp[0].attrs['href'] --> '/bbs/Gossiping/M.1623312990.A.963.html'

    return tempTopicList 





def checkThisBoard(board,keyword,token):
    
    
    # line notify post require headers
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    if isInit:
        #初始化文章列表
        oldTopicList = getTopic(board,keyword)
    
    # 抓取新文章
    newTopicList = getTopic(board,keyword)
    
    # 新舊文章轉換為set
    oldTopicSet = set(oldTopicList)
    newTopicSet = set(newTopicList)
    
    # 用set聯集、差級等操作方式，找出與前次相比新的文章
    articles_to_send = list( (oldTopicSet | newTopicSet) - oldTopicSet )
    
    # 每個新文章都發一個訊息
    for i in range(len(articles_to_send)):
        writeLog("[Info] Send a message : " + time.asctime() )
        params = {"message": articles_to_send[i]} 
        
        try:
            requests.post(
                "https://notify-api.line.me/api/notify",
                headers=headers, 
                params=params)
        except:
            writeLog("[warning] Network or token error : " + time.asctime() )
    
    # 舊文章List以新的覆蓋
    oldTopicList = newTopicList
    
    # 休息2.5分鐘
    time.sleep(150)



isInit = True

#不斷執行的部分
while True:
    
    checkThisBoard(codeJob,'發案',codeJobTOKEN)
    checkThisBoard(soho,'徵才',sohoTOKEN)
    isInit = False