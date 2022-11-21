import requests
import json
import pandas as pd
from lxml import etree

from zipfile import ZipFile
from urllib.request import urlopen

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm





def get_data(url,xpath,name):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url,headers=headers) 
    with open("detailxml.zip",'wb') as f:
        f.write(r.content)

    filename = url.split('/')[-1]  # this will take only -1 splitted part of the url

    with open(filename, 'wb') as output_file:
        output_file.write(r.content)
    
    zf = ZipFile('detailxml.zip', 'r')
    zf.extractall()
    zf.close()

    return get_candidate(xpath,name)

def get_candidate(xpath,name):
    header = []
    rows = []
    counties = []

    tree = etree.parse('detail.xml')
    root = tree.getroot()

    for VoteType in root.find(xpath):

        columns = []
        header.append(VoteType.attrib['name'])
        
        for County in VoteType:
            columns.append(County.attrib['votes'])

            if VoteType.attrib['name'] == "Election Day Votes":
                counties.append(County.attrib['name'])

        rows.append(columns)

    df = pd.DataFrame(rows)
    df = df.T
    df.columns = header


    df.insert(0, "Counties", counties)
    df.insert(5, 'Total', df['Absentee by Mail Votes'].astype(int) + df['Election Day Votes'].astype(int)+df['Advance Voting Votes'].astype(int)+df['Provisional Votes'].astype(int))
    df.insert(0, "ID", name +" " +df['Counties'])

    return df

Warnock =[]

Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Appling/115467/313148/reports/detailxml.zip",".//Choice[@key='2']",'Appling')) 
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Atkinson/115468/313060/reports/detailxml.zip",".//Choice[@key='2']",'Atkinson'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bacon/115469/313083/reports/detailxml.zip",".//Choice[@key='2']",'Bacon'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Baker/115470/312544/reports/detailxml.zip",".//Choice[@key='2']",'Baker'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Baldwin/115471/313143/reports/detailxml.zip",".//Choice[@key='2']",'Baldwin'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Banks/115472/313336/reports/detailxml.zip",".//Choice[@key='2']",'Banks'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Barrow/115473/313176/reports/detailxml.zip",".//Choice[@key='2']",'Barrow'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bartow/115474/312982/reports/detailxml.zip",".//Choice[@key='54']",'Bartow'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Ben_Hill/115475/313377/reports/detailxml.zip",".//Choice[@key='2']",'Ben Hill'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Berrien/115476/313071/reports/detailxml.zip",".//Choice[@key='2']",'Berrien'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bibb/115477/313347/reports/detailxml.zip",".//Choice[@key='2']",'Bibb'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bleckley/115478/312961/reports/detailxml.zip",".//Choice[@key='2']",'Bleckley'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Brantley/115479/313211/reports/detailxml.zip",".//Choice[@key='2']",'Brantley'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Brooks/115480/312999/reports/detailxml.zip",".//Choice[@key='2']",'Brooks'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bryan/115481/313138/reports/detailxml.zip",".//Choice[@key='2']",'Bryan'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bulloch/115482/313241/reports/detailxml.zip",".//Choice[@key='2']",'Bulloch'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Burke/115483/312983/reports/detailxml.zip",".//Choice[@key='2']",'Burke'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Butts/115484/313669/reports/detailxml.zip",".//Choice[@key='2']",'Butts'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Calhoun/115485/313024/reports/detailxml.zip",".//Choice[@key='2']",'Calhoun'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Camden/115486/313152/reports/detailxml.zip",".//Choice[@key='2']",'Camden'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Candler/115487/313095/reports/detailxml.zip",".//Choice[@key='2']",'Candler'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Carroll/115488/312948/reports/detailxml.zip",".//Choice[@key='54']",'Carroll'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Catoosa/115489/313017/reports/detailxml.zip",".//Choice[@key='54']",'Catoosa'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Charlton/115490/313365/reports/detailxml.zip",".//Choice[@key='2']",'Charlton'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Chatham/115491/313201/reports/detailxml.zip",".//Choice[@key='2']",'Chatham'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Chattahoochee/115492/313403/reports/detailxml.zip",".//Choice[@key='54']",'Chattahoochee'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Chattooga/115493/313121/reports/detailxml.zip",".//Choice[@key='54']",'Chattooga'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Cherokee/115494/313291/reports/detailxml.zip",".//Choice[@key='54']",'Cherokee'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Clarke/115495/313043/reports/detailxml.zip",".//Choice[@key='2']",'Clarke'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Clay/115496/312762/reports/detailxml.zip",".//Choice[@key='2']",'Clay'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Clayton/115497/313014/reports/detailxml.zip",".//Choice[@key='54']",'Clayton'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Clinch/115498/312798/reports/detailxml.zip",".//Choice[@key='2']",'Clinch'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Cobb/115499/313474/reports/detailxml.zip",".//Choice[@key='2']",'Cobb'))



#Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Fulton/115526/313235/reports/detailxml.zip",".//Choice[@key='54']",'Fulton'))
#Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/DeKalb/115510/313262/reports/detailxml.zip",".//Choice[@key='2']",'DeKalb'))  

Warnock=pd.concat(Warnock)
print(Warnock)

