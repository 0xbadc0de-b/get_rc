#!python3
# -*- coding: utf-8 -*-
# usage  : get_rc.py [uid]
# date   : 2019-10-19
# update : 2020-03-23 (Add) 결과파싱
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

    fileName = questionNum + '_RC.txt'
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
    file_parsing(questionNum)

def file_parsing(questionNum):
    inputFile = questionNum + '_RC.txt'
    outputFile = questionNum + '_RC_parsing.txt'
    qestion_URL = 'https://www.hackers.co.kr/?c=s_toeic/toeic_study/drc&front=dailytoeic&category=RC&uid=' + questionNum + '\n'
    
    f = open(inputFile, 'r', -1, 'utf-8')
    lines = f.readlines()
    f.close()
    
    f = open(outputFile, 'w', -1, 'utf-8')
    f.write(qestion_URL+'\n')
    
    lineNum = 0
    parsing_list = []
    for line in lines:
        lineNum = lineNum + 1        
        line = line.strip()
        if line in parsing_list:
            continue
        if re.search('^[123][.][A-Z|-]', line):
            parsing_list.append(line)
            f.write(line+'\n')            
        elif re.search('^\([ABCD]\) [a-zA-Z]', line):
            parsing_list.append(line)            
            f.write(line+'\n')
        elif re.search('해  석$', line) and lines[lineNum].strip() not in parsing_list:
            parsing_list.append(lines[lineNum].strip())
            f.write(lines[lineNum].strip()+'\n')
        elif re.search('해  설$', line) and lines[lineNum].strip() not in parsing_list:
            parsing_list.append(lines[lineNum].strip())
            f.write(lines[lineNum].strip()+'\n')
        elif re.search('어  휘$', line) and lines[lineNum].strip() not in parsing_list:
            parsing_list.append(lines[lineNum].strip())
            f.write(lines[lineNum].strip()+'\n')
        elif re.search('정  답$', line) and lines[lineNum].strip() not in parsing_list:
            parsing_list.append(lines[lineNum].strip())
            f.write(lines[lineNum].strip()+'\n')
    print('[+] Make: ' + outputFile)    
    f.close()
        
if __name__=="__main__":
    main()
    # fileName = '6610.txt'
    # file_parsing(fileName)