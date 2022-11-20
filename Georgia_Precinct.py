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
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Baker/115470/312544/reports/detailxml.zip",".//Choice[@key='2']",'Baker')) 

Warnock=pd.concat(Warnock)
print(Warnock)

