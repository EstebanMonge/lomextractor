import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, request
from flask_restful import Resource, Api
from pprint import pprint
import os
import re

app = Flask(__name__)
api = Api(app)

f = open("lom.csv", "w")
f.write('"medicine","group"\n')
base_url = 'https://www.ccss.sa.cr'
page = urllib.request.urlopen(base_url + "/lom?pagina=1&s=6&t=3")
soup = BeautifulSoup(page,'html.parser')
root = soup.findAll('div', attrs = {"class":"page-number pull-right"})
'''
Extracting all anime Urls and appending them in anime_links[]
'''
pages_num = int(re.findall(r'de (.*?)$',root[0].string)[0])

page_num = 1
while page_num <= pages_num:
    page = urllib.request.urlopen(base_url + "/lom?pagina="+str(page_num)+"&s=6&t=3")
    soup = BeautifulSoup(page,'html.parser')
    root = soup.findAll('div', attrs = {"title":"Ver más detalles del medicamento"})
    for title in root:
        medicine = re.findall(r'\|\ (.*?)</h4>',str(title))
        group = re.findall('Grupo</b>(.*?)<br(.*?)>',str(title))
        if len(medicine) > 0:
            f.write('"'+medicine[0]+'","'+group[0][0].replace(":","").strip()+'"\n')
            print('"'+medicine[0]+'","'+group[0][0].replace(":","").strip()+'"')
    page_num = page_num + 1
f.close()
