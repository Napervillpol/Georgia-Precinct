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
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Appling/115467/313148/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Appling')) 
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Atkinson/115468/313060/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Atkinson'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bacon/115469/313083/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Bacon'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Baker/115470/312544/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Baker'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Baldwin/115471/313143/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Baldwin'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Banks/115472/313336/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Banks'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Barrow/115473/313176/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Barrow'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bartow/115474/312982/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Bartow'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Ben_Hill/115475/313377/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Ben Hill'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Berrien/115476/313071/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Berrien'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bibb/115477/313347/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Bibb'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bleckley/115478/312961/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Bleckley'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Brantley/115479/313211/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Brantley'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Brooks/115480/312999/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Brooks'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bryan/115481/313138/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Bryan'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Bulloch/115482/313241/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Bulloch'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Burke/115483/312983/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Burke'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Butts/115484/313669/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Butts'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Calhoun/115485/313024/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Calhoun'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Camden/115486/313152/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Camden'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Candler/115487/313095/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Candler'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Carroll/115488/312948/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Carroll'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Catoosa/115489/313017/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Catoosa'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Charlton/115490/313365/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Charlton'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Chatham/115491/313201/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Chatham'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Chattahoochee/115492/313403/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Chattahoochee'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Chattooga/115493/313121/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Chattooga'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Cherokee/115494/313291/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Cherokee'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Clarke/115495/313043/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Clarke'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Clay/115496/312762/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Clay'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Clayton/115497/313014/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Clayton'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Clinch/115498/312798/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Clinch'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Cobb/115499/313474/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Cobb'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Coffee/115500/313061/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Coffee'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Colquitt/115501/312927/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Colquitt'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Columbia/115502/313348/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Columbia'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Cook/115503/313311/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Cook'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Coweta/115504/313172/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Coweta'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Crawford/115505/313309/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Crawford'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Crisp/115506/313115/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Crisp'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Dade/115507/313147/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Dade'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Dawson/115508/313260/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Dawson'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Decatur/115509/313465/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Decatur'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/DeKalb/115510/313262/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'DeKalb'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Dodge/115511/313125/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Dodge'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Dooly/115512/313116/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Dooly'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Dougherty/115513/313180/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Dougherty'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Douglas/115514/313287/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Douglas'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Early/115515/313240/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Early'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Echols/115516/313126/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Echols'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Effingham/115517/313118/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Effingham'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Elbert/115518/313330/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Elbert'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Emanuel/115519/313280/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Emanuel'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Evans/115520/313493/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Evans'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Fannin/115521/312974/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Fannin'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Fayette/115522/313021/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Fayette'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Floyd/115523/313114/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Floyd'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Forsyth/115524/313319/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Forsyth'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Franklin/115525/313153/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Franklin'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Fulton/115526/313235/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Fulton'))





#Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Fulton/115526/313235/reports/detailxml.zip",".//Choice[@key='54']",'Fulton'))
#Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/DeKalb/115510/313262/reports/detailxml.zip",".//Choice[@key='2']",'DeKalb'))  

Warnock=pd.concat(Warnock)
print(Warnock)

