import requests #引入函式庫
from bs4 import BeautifulSoup

def exchangeRate():
    '''
    抓到最新台銀匯率資料
    '''
    
    # 爬下com
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')
    trs = table.find_all('tr')
    
    myStr = "";
    
    for idx, tr in enumerate(trs):
        if idx == 2:
            tds = tr.find_all('td')
            myStr +="幣別:美金(USD) =>" + " 即期買入：" + tds[3].text + "/即期賣出：" + tds[4].text + "\n"
            
        if idx == 9:
            tds = tr.find_all('td')
            myStr +="幣別:日圓(JPY) =>"  + " 即期買入：" + tds[3].text + "/即期賣出：" + tds[4].text + "\n"

        if idx == 16:
            tds = tr.find_all('td')
            myStr +="幣別:歐元(EUR) =>"  + " 即期買入：" + tds[3].text + "/即期賣出：" + tds[4].text
    #此表格是牌告匯率，表格分為七直欄，第一直欄是幣別，
    #第四直欄是本行買入即期匯率，第五直欄是本行賣出即期匯率
    return myStr
