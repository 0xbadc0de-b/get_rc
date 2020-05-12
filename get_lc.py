#!python3
# -*- coding: utf-8 -*-
# usage : get_lc.py [uid]
# date  : 2020-03-09
# update: 2020-03-19 Add 'mp3_download'
# update: 2020-03-25 Add 'file_parsing'
# update: 2020-05-12 Mod 'mp3_download'
import sys
import re
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) < 2:
        print('usage : get_lc.py <date>')
        sys.exit()

    questionNum = sys.argv[1]
    lc_url = 'https://www.hackers.co.kr/?c=s_toeic/toeic_study/dlc&front=dailytoeic&category=LC&result=Y&uid='
    lc_url = lc_url + questionNum

    solve_info = {
        'r': 'hackers',
        'm': 'contents',
        'a': 'dailytoeic/solve',
        # 'uid': '6246',
        'category': 'LC',
        'totaluser': '2712',
        'answer': 'Y',
        'event_pop': '',
        'part[]': 'p2_1',
        'p2_1_a': 'A',
        'p2_1_ua': 'A',
        'part[]': 'p4_1',
        'p4_1_a': 'A',
        'p4_1_ua': 'A',
        'part[]': 'p4_2',
        'p4_2_a': 'A',
        'p4_2_ua': 'A',
        'part[]': 'p4_3',
        'p4_3_a': 'A',
        'p4_3_ua': 'A'
    }
    solve_info['uid'] = questionNum

    fileName = questionNum + '_LC.txt'
    f = open(fileName, 'w', -1, 'utf-8')

    with requests.Session() as s:
        req = s.post(lc_url, data=solve_info)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        # solveStrings = soup.select('[class="td_font type1"]')
        # solveStrings = soup.select('.MsoNormal')
        solveStrings = soup.select('.ico_part')
        # solveStrings = soup.select('td')
        # solveStrings = soup.select('.ico_part > table > tr > td > strong')
        
        for solvStr in solveStrings:
            # print(solvStr.text)
            f.write(solvStr.text)
            # print(solvStr.text.encode('utf-8'))

    f.close()
    print('[+] Make: ' + fileName)
    file_parsing(questionNum)
    mp3_download(html)
    
def mp3_download(html):
    p = re.compile(".*file:.*mp3'")
    lines = p.findall(html)
    
    for line in lines:
        line = line.strip()
        url = line.split('\'')[1]
        mp3file = url.split('/')[-1]

        with open(mp3file, 'wb') as mp3:
                response = requests.get(url)
                mp3.write(response.content)
                print('[+] Down: ' + mp3file)

def file_parsing(questionNum):
    inputFile = questionNum + '_LC.txt'
    outputFile = questionNum + '_LC_parsing.txt'
    qestion_URL = 'https://www.hackers.co.kr/?c=s_toeic/toeic_study/dlc&front=dailytoeic&category=LC&uid=' + questionNum + '\n'
    
    f = open(inputFile, 'r', -1, 'utf-8')
    lines = f.readlines()
    f.close()
    
    f = open(outputFile, 'w', -1, 'utf-8')
    f.write(qestion_URL+'\n')
    
    writeFlag = False
    
    for line in lines:
        line = line.strip()
        if line == '':
            continue

        if ' 발음' in line:
            writeFlag = True
        elif '반복재생' in line:
            writeFlag = False
        elif '해  석' in line:
            writeFlag = True
        elif '· 총 참여자수' in line:
            writeFlag = False            
            
        if writeFlag == True:
            f.write(line+'\n')

    print('[+] Make: ' + outputFile)    
    f.close()
        
if __name__=="__main__":
    main()
    