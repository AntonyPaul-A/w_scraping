import pandas as pd
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.width', 1000)                         #To prevent the output from wrapping weirdly, you can also set:

import requests
from bs4 import BeautifulSoup
import time
import numpy as np
from openpyxl.workbook import Workbook
import re
url='https://en.wikipedia.org/wiki/List_of_dinosaur_genera'
html=requests.get(url)
# print(html)
soup=BeautifulSoup(html.text,'html.parser')
# print(soup)
filtr=soup.find_all('a',href=True)
# print(filtr)
urlname=[(i['href'],i.text) for i in filtr]
# print(urlname)
wikki=[urlname[link] for link in range(len(urlname)) if urlname[link][0].startswith("/wiki/")]
wikki=wikki[:2317:]
# print(wikki)
dinodf=pd.DataFrame(wikki,columns=["URL","Dinosaur"])
# print(dinodf)
dinodf["Dinosaur"]=dinodf["Dinosaur"].replace("",None)
# print(dinodf)
dinodf=dinodf.dropna(axis=0,subset=['Dinosaur'])
# print(dinodf)
wikki=dinodf.set_index('URL')['Dinosaur'].to_dict()
# print(wikki)
dino_data=[('https://en.wikipedia.org'+ URL,Dinosaur) for URL,Dinosaur in wikki.items()]
# print(dino_data)
dino_data=dino_data[33::]
# print(dino_data)
iter=[element for pair in dino_data for element in pair if element.startswith("https://en.wikipedia.org")]
# print(iter)
datainfo=[]
progress=0
for url in range(100):
    html=requests.get(iter[url])
    soup=BeautifulSoup(html.text,'html.parser')
    para=soup.find_all('p')
    cleanpara=[paracleaned.text.strip() for paracleaned in para]
    # print(cleanpara)
    cleanpara=cleanpara[:4:]
    datainfo.append(" ".join(cleanpara))
# print(datainfo)
# print(dinodf)
datainfodf=pd.DataFrame(datainfo,columns=["info"])
concat_df=pd.concat([dinodf,datainfodf],axis=1)
# # # print(concat_df)
filepath=r'C:\Users\Public\practice_file\dinothunder.xlsx'
concat_df.to_excel(filepath)
print("excel file uploaded")
dinodf=pd.read_excel(filepath)
# print(dinodf)
dinodf.drop('Unnamed: 0',inplace=True,axis=1)
# print(dinodf)
dinodf.columns=['URL','Dinosaur','Info']
# print(dinodf)
dino_info=dinodf['Info'].to_dict()
# print(dino_info)
dino_info=dino_info.values()
# print(dino_info)

heights_clean=[]
weights_clean=[]

for i in dino_info:
    text=str(i)
    heights=re.findall(r'\d+\smeters',text)
    # print(heights)
    if heights:
        heights_clean.append(heights[0])

    else:
        heights_clean.append("-")


    weights=re.findall(r'\d+\stonnes|\d+\skilograms',text)

    if weights:
        weights_clean.append(weights[0])
    else:
        weights_clean.append('-')
# print(heights_clean)
# print(weights_clean)
dinodf.drop('Info',inplace=True,axis=1)

dinodf['Heights']=heights_clean

dinodf['Weights']=weights_clean


filename=r'C:\Users\Public\practice_file\dinoresult.xlsx'
dinodf.to_excel(filename)
print("excel file uploaded")


