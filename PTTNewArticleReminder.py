# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 17:23:39 2021

@author: Arthur
"""

# Python網頁爬蟲結合LINE Notify打造自動化訊息通知服務
# https://www.learncodewithmike.com/2020/06/python-line-notify.html

TOKEN = "Put Your Token Here"
target_url = "https://www.ptt.cc/bbs/CodeJob/index.html"

from bs4 import BeautifulSoup
import requests
import time


oldTopicList = [] #用來存舊的文章列表

# line notify post require headers
headers = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/x-www-form-urlencoded"
}

# 獲取文章
def getTopic():
    
    #爬取網頁資訊並給bs4解析，選出符合的區段給temp
    result = requests.get(target_url)
    soup = BeautifulSoup(result.text,'lxml')
    temp = soup.select("div.title a") #這是有所有文章的list
    
    # 用來暫存符合的文章
    tempTopicList = []
    
    #找該頁不含re(回文)且符合[發案]開頭的文章，並存起來
    for i in range(len(temp)):
        if '[發案]' in temp[i].text and 'Re' not in temp[i].text:
            tempTopicList.append( temp[i].text + "\nhttps://www.ptt.cc" + temp[i].attrs['href'] ) #temp[0].text --> '[問卦] 黎清波的八卦' & temp[0].attrs['href'] --> '/bbs/Gossiping/M.1623312990.A.963.html'
    return tempTopicList 


#初始化文章列表
oldTopicList = getTopic()

#不斷執行的部分
while True:
    
    # 抓取新文章
    newTopicList = getTopic()
    
    # 新舊文章轉換為set
    oldTopicSet = set(oldTopicList)
    newTopicSet = set(newTopicList)
    
    # 用set聯集、差級等操作方式，找出與前次相比新的文章
    articles_to_send = list( (oldTopicSet | newTopicSet) - oldTopicSet )
    
    # 每個新文章都發一個訊息
    for i in range(len(articles_to_send)):
        params = {"message": articles_to_send[i]} 
        r = requests.post(
            "https://notify-api.line.me/api/notify",
            headers=headers, 
            params=params)
    
    # 舊文章List以新的覆蓋
    oldTopicList = newTopicList
    
    # 休息五分鐘
    time.sleep(300)


