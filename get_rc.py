#!python3
# -*- coding: utf-8 -*-
# usage  : get_rc.py [uid]
# date   : 2019-10-19
# update : 
import sys
import re
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) < 2:
        print('usage : get_rc.py <date>')
        sys.exit()

    questionNum = sys.argv[1]
    rc_url = 'https://www.hackers.co.kr/?c=s_toeic/toeic_study/drc&front=dailytoeic&category=RC&result=Y&uid='
    rc_url = rc_url + questionNum

    solve_info = {
        'r': 'hackers',
        'm': 'contents',
        'a': 'dailytoeic/solve',
        # 'uid': '6246',
        'category': 'RC',
        'totaluser': '3877',
        'answer': 'Y',
        'event_pop': '',
        'part[]': 'p5_1',
        'p5_1_a': 'A',
        'p5_1_ua': 'A',
        'part[]': 'p5_2',
        'p5_2_a': 'A',
        'p5_2_ua': 'A',
        'part[]': 'p5_3',
        'p5_3_a': 'A',
        'p5_3_ua': 'A'
    }
    solve_info['uid'] = questionNum

    fileName = questionNum + '.txt'
    f = open(fileName, 'w', -1, 'utf-8')

    with requests.Session() as s:
        req = s.post(rc_url, data=solve_info)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        # solveStrings = soup.select('[class=td_font]')
        solveStrings = soup.select('td')
        
        for solvStr in solveStrings:
            # print(solvStr.text)
            f.write(solvStr.text)
            # print(solvStr.text.encode('utf-8'))

    f.close()
    print('[+] Make: ' + fileName)    

def file_parsing(fileName):
    f = open(fileName, 'r', -1, 'utf-8')
    lines = f.readlines()
    f.close()
    
    lineNum = 0
    parsing_list = []
    for line in lines:
        lineNum = lineNum + 1
        line = line.strip()
        if re.search('^[123][.][A-Z]', line) and line not in parsing_list:
            print(line)
            parsing_list.append(line)
        elif re.search('\([ABCD]\) [a-zA-Z]', line) and line not in parsing_list:
            print(line)
            parsing_list.append(line)            
        elif re.search('해  석$', line) and lines[lineNum] not in parsing_list:
            print(lines[lineNum])
            parsing_list.append(lines[lineNum])
        elif re.search('해  설$', line) and lines[lineNum] not in parsing_list:
            print(lines[lineNum])
            parsing_list.append(lines[lineNum])            
        elif re.search('어  휘$', line) and lines[lineNum] not in parsing_list:
            print(lines[lineNum])
            parsing_list.append(lines[lineNum])            
        elif re.search('정  답$', line) and lines[lineNum] not in parsing_list:
            print(lines[lineNum])
            parsing_list.append(lines[lineNum])
        
if __name__=="__main__":
    # main()
    fileName = '6589.txt'
    file_parsing(fileName)