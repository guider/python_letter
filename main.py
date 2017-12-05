from time import sleep

import requests
import json
import sql_helper
from sql_helper import MySQLClient
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Referer': 'https://servicewechat.com/wx38be548c581f8c61/10/page-frame.html',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6',
    'If-None-Match': '"3ce9f2-4a29c-548f423b77900"',
    'If-Modified-Since': 'Mon, 20 Feb 2017 10:58:12 GMT'
}

url = 'https://rayscloud.chubanyun.net/api/Writing/WritingCommon/writingBiShunByWords'
baseImageUrl = 'http://image.chubanyun.net/images/writing/fontimage/'


def fetchData(letter):
    response = requests.post(url, headers=headers, params={'word': letter}, verify=False)
    resp = response.json()
    print(resp)

    downloadImage(resp['data']['imgurl'])
    # resoObj= json.loads(response.json())
    client = MySQLClient()
    if resp['success']:
        resArgs = resp['data']
        # content','chinese_word','imgurl','id
        print(resArgs)
        client.insertLetter(resArgs)
        client.close()


"""
     fetchData()
"""


def getLetters():
    with open('resource/letters.txt', 'r', encoding='utf-8') as f:
        letters = f.read()
        arrLetters = list(letters.replace(' ', '').replace('\n', ''))
        print(arrLetters)
        return letters


def downloadImage(txt):
    imgurl = 'https://xinhuazidian.18dao.cn/bishun/'+txt+'.gif'
    print(imgurl)
    from contextlib import closing
    with closing(requests.get(imgurl, headers=headers, stream=True)) as response:
        with open('./gifs/' + txt + '.gif', 'wb') as fd:
            for chunk in response.iter_content(256):
                fd.write(chunk)


if __name__ == '__main__':
    for index, item in enumerate(getLetters()):
        print(item)

        try:
            print(item)
            if item.strip() == '':
                continue

            downloadImage(item)
            # fetchData(item)
            time.sleep(0.5)
        except BaseException:
            print('error')
