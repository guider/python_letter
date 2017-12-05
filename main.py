from time import sleep

import requests
import json
import sql_helper
from sql_helper import MySQLClient
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
                  + 'Mobile/14G60 MicroMessenger/6.5.23 NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx38be548c581f8c61/10/page-frame.html',
    'Content-Type': 'application/json',
    'X-AspNet-Version': '4.0.30319',
    'X-Powered-By': 'ASP.NET'
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


def downloadImage(imgid):
    imgurl = baseImageUrl + imgid + '.png'
    from contextlib import closing
    with closing(requests.get(imgurl, headers=headers, stream=True)) as response:
        with open('./images/' + imgid + '.png', 'wb') as fd:
            for chunk in response.iter_content(256):
                fd.write(chunk)


if __name__ == '__main__':
    for index, item in enumerate(getLetters()[2400:]):
        print(item)

        try:
            print(item)
            if item.strip() == '':
                continue
            fetchData(item)
            time.sleep(0.5)
        except BaseException:
            print('error')
