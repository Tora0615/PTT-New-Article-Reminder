# PTT New Article Reminder

將爬蟲結合 Line Notify，實現自動化訊息通知。


本程式預設會定期爬取 PTT 的 codejob 版，看是否有新的案子可以接。


### 如何使用 ? 
去 Line Notify 申請權杖填入後，直接執行就好
* [Line Notify 教學](https://www.learncodewithmike.com/2020/06/python-line-notify.html)

### 其他使用方法 ? 
可更改 target_url，追蹤自己有興趣的板。

### 注意事項
PTT 八卦版 ( gossiping ) 或其他有 18 歲限制的板，沒辦法直接使用，需要使用 session & playload 等。

改天有寫再更新上來。

#### TODO
* 18 歲限制的版也適用
* 多版同時監控
    * 將功能封裝
    * 需要申請並設定多Token