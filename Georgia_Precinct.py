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



#Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Fulton/115526/313235/reports/detailxml.zip",".//Choice[@key='54']",'Fulton'))
#Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/DeKalb/115510/313262/reports/detailxml.zip",".//Choice[@key='2']",'DeKalb'))  

Warnock=pd.concat(Warnock)
print(Warnock)

