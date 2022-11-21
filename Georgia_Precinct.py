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
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Gilmer/115527/313111/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Gilmer'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Glascock/115528/312225/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Glascock'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Glynn/115529/313275/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Glynn'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Gordon/115530/313299/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Gordon'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Grady/115531/312782/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Grady'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Greene/115532/313104/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Greene'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Gwinnett/115533/313157/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Gwinnett'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Habersham/115534/314003/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Habersham'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Hall/115535/313325/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Hall'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Hancock/115536/313243/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Hancock'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Haralson/115537/313092/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Haralson'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Harris/115538/313390/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Harris'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Hart/115539/312909/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Hart'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Heard/115540/313217/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Heard'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Henry/115541/313290/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Henry'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Houston/115542/313392/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Houston'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Irwin/115543/313103/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Irwin'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Jackson/115544/313099/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Jackson'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Jasper/115545/313160/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Jasper'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Jeff_Davis/115546/313102/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Jeff Davis'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Jefferson/115547/312994/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Jefferson'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Jenkins/115548/313171/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Jenkins'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Johnson/115549/312792/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Johnson'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Jones/115550/313142/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Jones'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Lamar/115551/313081/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Lamar'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Lanier/115552/313366/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Lanier'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Laurens/115553/313141/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Laurens'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Lee/115554/312793/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Lee'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Liberty/115555/314012/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Liberty'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Lincoln/115556/312678/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Lincoln'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Long/115557/313222/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Long'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Lowndes/115558/313361/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Lowndes'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Lumpkin/115559/313310/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Lumpkin'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Macon/115560/313088/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Macon'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Madison/115561/313228/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Madison'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Marion/115562/313370/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'Marion'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/McDuffie/115563/312733/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'McDuffie'))
Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/McIntosh/115564/313393/reports/detailxml.zip",".//Choice[@text='Raphael Warnock (I) (Dem)']",'McIntosh'))





#Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/Fulton/115526/313235/reports/detailxml.zip",".//Choice[@key='54']",'Fulton'))
#Warnock.append(get_data( "https://results.enr.clarityelections.com//GA/DeKalb/115510/313262/reports/detailxml.zip",".//Choice[@key='2']",'DeKalb'))  

Warnock=pd.concat(Warnock)
print(Warnock)

