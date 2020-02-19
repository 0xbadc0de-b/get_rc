# -*- coding: utf-8 -*-
#!python2
# date : 2019-10-19
# usage : get_rc.py [uid]
import sys
import requests
from bs4 import BeautifulSoup

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

with requests.Session() as s:
    req = s.post(rc_url, data=solve_info)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    solveStrings = soup.select('[class=td_font]')
    
    for solvStr in solveStrings:
        print(solvStr.text.encode('utf-8'))
