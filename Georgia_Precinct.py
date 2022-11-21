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
def get_candidate_precinct(candidate,xpath):
   
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Appling/115467/313148/reports/detailxml.zip",xpath,'Appling')) 
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Atkinson/115468/313060/reports/detailxml.zip",xpath,'Atkinson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bacon/115469/313083/reports/detailxml.zip",xpath,'Bacon'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Baker/115470/312544/reports/detailxml.zip",xpath,'Baker'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Baldwin/115471/313143/reports/detailxml.zip",xpath,'Baldwin'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Banks/115472/313336/reports/detailxml.zip",xpath,'Banks'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Barrow/115473/313176/reports/detailxml.zip",xpath,'Barrow'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bartow/115474/312982/reports/detailxml.zip",xpath,'Bartow'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Ben_Hill/115475/313377/reports/detailxml.zip",xpath,'Ben Hill'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Berrien/115476/313071/reports/detailxml.zip",xpath,'Berrien'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bibb/115477/313347/reports/detailxml.zip",xpath,'Bibb'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bleckley/115478/312961/reports/detailxml.zip",xpath,'Bleckley'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Brantley/115479/313211/reports/detailxml.zip",xpath,'Brantley'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Brooks/115480/312999/reports/detailxml.zip",xpath,'Brooks'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bryan/115481/313138/reports/detailxml.zip",xpath,'Bryan'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bulloch/115482/313241/reports/detailxml.zip",xpath,'Bulloch'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Burke/115483/312983/reports/detailxml.zip",xpath,'Burke'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Butts/115484/313669/reports/detailxml.zip",xpath,'Butts'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Calhoun/115485/313024/reports/detailxml.zip",xpath,'Calhoun'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Camden/115486/313152/reports/detailxml.zip",xpath,'Camden'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Candler/115487/313095/reports/detailxml.zip",xpath,'Candler'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Carroll/115488/312948/reports/detailxml.zip",xpath,'Carroll'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Catoosa/115489/313017/reports/detailxml.zip",xpath,'Catoosa'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Charlton/115490/313365/reports/detailxml.zip",xpath,'Charlton'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Chatham/115491/313201/reports/detailxml.zip",xpath,'Chatham'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Chattahoochee/115492/313403/reports/detailxml.zip",xpath,'Chattahoochee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Chattooga/115493/313121/reports/detailxml.zip",xpath,'Chattooga'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Cherokee/115494/313291/reports/detailxml.zip",xpath,'Cherokee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Clarke/115495/313043/reports/detailxml.zip",xpath,'Clarke'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Clay/115496/312762/reports/detailxml.zip",xpath,'Clay'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Clayton/115497/313014/reports/detailxml.zip",xpath,'Clayton'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Clinch/115498/312798/reports/detailxml.zip",xpath,'Clinch'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Cobb/115499/313474/reports/detailxml.zip",xpath,'Cobb'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Coffee/115500/313061/reports/detailxml.zip",xpath,'Coffee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Colquitt/115501/312927/reports/detailxml.zip",xpath,'Colquitt'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Columbia/115502/313348/reports/detailxml.zip",xpath,'Columbia'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Cook/115503/313311/reports/detailxml.zip",xpath,'Cook'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Coweta/115504/313172/reports/detailxml.zip",xpath,'Coweta'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Crawford/115505/313309/reports/detailxml.zip",xpath,'Crawford'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Crisp/115506/313115/reports/detailxml.zip",xpath,'Crisp'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dade/115507/313147/reports/detailxml.zip",xpath,'Dade'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dawson/115508/313260/reports/detailxml.zip",xpath,'Dawson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Decatur/115509/313465/reports/detailxml.zip",xpath,'Decatur'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/DeKalb/115510/313262/reports/detailxml.zip",xpath,'DeKalb'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dodge/115511/313125/reports/detailxml.zip",xpath,'Dodge'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dooly/115512/313116/reports/detailxml.zip",xpath,'Dooly'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dougherty/115513/313180/reports/detailxml.zip",xpath,'Dougherty'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Douglas/115514/313287/reports/detailxml.zip",xpath,'Douglas'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Early/115515/313240/reports/detailxml.zip",xpath,'Early'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Echols/115516/313126/reports/detailxml.zip",xpath,'Echols'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Effingham/115517/313118/reports/detailxml.zip",xpath,'Effingham'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Elbert/115518/313330/reports/detailxml.zip",xpath,'Elbert'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Emanuel/115519/313280/reports/detailxml.zip",xpath,'Emanuel'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Evans/115520/313493/reports/detailxml.zip",xpath,'Evans'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Fannin/115521/312974/reports/detailxml.zip",xpath,'Fannin'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Fayette/115522/313021/reports/detailxml.zip",xpath,'Fayette'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Floyd/115523/313114/reports/detailxml.zip",xpath,'Floyd'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Forsyth/115524/313319/reports/detailxml.zip",xpath,'Forsyth'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Franklin/115525/313153/reports/detailxml.zip",xpath,'Franklin'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Fulton/115526/313235/reports/detailxml.zip",xpath,'Fulton'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Gilmer/115527/313111/reports/detailxml.zip",xpath,'Gilmer'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Glascock/115528/312225/reports/detailxml.zip",xpath,'Glascock'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Glynn/115529/313275/reports/detailxml.zip",xpath,'Glynn'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Gordon/115530/313299/reports/detailxml.zip",xpath,'Gordon'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Grady/115531/312782/reports/detailxml.zip",xpath,'Grady'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Greene/115532/313104/reports/detailxml.zip",xpath,'Greene'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Gwinnett/115533/313157/reports/detailxml.zip",xpath,'Gwinnett'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Habersham/115534/314003/reports/detailxml.zip",xpath,'Habersham'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Hall/115535/313325/reports/detailxml.zip",xpath,'Hall'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Hancock/115536/313243/reports/detailxml.zip",xpath,'Hancock'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Haralson/115537/313092/reports/detailxml.zip",xpath,'Haralson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Harris/115538/313390/reports/detailxml.zip",xpath,'Harris'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Hart/115539/312909/reports/detailxml.zip",xpath,'Hart'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Heard/115540/313217/reports/detailxml.zip",xpath,'Heard'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Henry/115541/313290/reports/detailxml.zip",xpath,'Henry'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Houston/115542/313392/reports/detailxml.zip",xpath,'Houston'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Irwin/115543/313103/reports/detailxml.zip",xpath,'Irwin'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Jackson/115544/313099/reports/detailxml.zip",xpath,'Jackson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Jasper/115545/313160/reports/detailxml.zip",xpath,'Jasper'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Jeff_Davis/115546/313102/reports/detailxml.zip",xpath,'Jeff Davis'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Jefferson/115547/312994/reports/detailxml.zip",xpath,'Jefferson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Jenkins/115548/313171/reports/detailxml.zip",xpath,'Jenkins'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Johnson/115549/312792/reports/detailxml.zip",xpath,'Johnson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Jones/115550/313142/reports/detailxml.zip",xpath,'Jones'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Lamar/115551/313081/reports/detailxml.zip",xpath,'Lamar'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Lanier/115552/313366/reports/detailxml.zip",xpath,'Lanier'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Laurens/115553/313141/reports/detailxml.zip",xpath,'Laurens'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Lee/115554/312793/reports/detailxml.zip",xpath,'Lee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Liberty/115555/314012/reports/detailxml.zip",xpath,'Liberty'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Lincoln/115556/312678/reports/detailxml.zip",xpath,'Lincoln'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Long/115557/313222/reports/detailxml.zip",xpath,'Long'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Lowndes/115558/313361/reports/detailxml.zip",xpath,'Lowndes'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Lumpkin/115559/313310/reports/detailxml.zip",xpath,'Lumpkin'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Macon/115560/313088/reports/detailxml.zip",xpath,'Macon'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Madison/115561/313228/reports/detailxml.zip",xpath,'Madison'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Marion/115562/313370/reports/detailxml.zip",xpath,'Marion'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/McDuffie/115563/312733/reports/detailxml.zip",xpath,'McDuffie'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/McIntosh/115564/313393/reports/detailxml.zip",xpath,'McIntosh'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Meriwether/115565/313212/reports/detailxml.zip",xpath,'Meriwether'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Miller/115566/312527/reports/detailxml.zip",xpath,'Miller'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Mitchell/115567/312509/reports/detailxml.zip",xpath,'Mitchell'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Monroe/115568/312791/reports/detailxml.zip",xpath,'Monroe'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Montgomery/115569/312808/reports/detailxml.zip",xpath,'Montgomery'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Morgan/115570/313218/reports/detailxml.zip",xpath,'Morgan'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Murray/115571/312962/reports/detailxml.zip",xpath,'Murray'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Muscogee/115572/313372/reports/detailxml.zip",xpath,'Muscogee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Newton/115573/314019/reports/detailxml.zip",xpath,'Newton'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Oconee/115574/313350/reports/detailxml.zip",xpath,'Oconee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Oglethorpe/115575/313205/reports/detailxml.zip",xpath,'Oglethorpe'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Paulding/115576/313185/reports/detailxml.zip",xpath,'Paulding'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Peach/115577/313412/reports/detailxml.zip",xpath,'Peach'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Pickens/115578/313289/reports/detailxml.zip",xpath,'Pickens'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Pierce/115579/312755/reports/detailxml.zip",xpath,'Pierce'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Pike/115580/313062/reports/detailxml.zip",xpath,'Pike'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Polk/115581/313253/reports/detailxml.zip",xpath,'Polk'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Pulaski/115582/312711/reports/detailxml.zip",xpath,'Pulaski'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Putnam/115583/312997/reports/detailxml.zip",xpath,'Putnam'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Quitman/115584/313477/reports/detailxml.zip",xpath,'Quitman'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Rabun/115585/313098/reports/detailxml.zip",xpath,'Rabun'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Randolph/115586/312652/reports/detailxml.zip",xpath,'Randolph'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Richmond/115587/313312/reports/detailxml.zip",xpath,'Richmond'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Rockdale/115588/313006/reports/detailxml.zip",xpath,'Rockdale'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Schley/115589/313073/reports/detailxml.zip",xpath,'Schley'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Screven/115590/313382/reports/detailxml.zip",xpath,'Screven'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Seminole/115591/313135/reports/detailxml.zip",xpath,'Seminole'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Spalding/115592/313396/reports/detailxml.zip",xpath,'Spalding'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Stephens/115593/312943/reports/detailxml.zip",xpath,'Stephens'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Stewart/115594/313112/reports/detailxml.zip",xpath,'Stewart'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Sumter/115595/312761/reports/detailxml.zip",xpath,'Sumter'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Talbot/115596/312116/reports/detailxml.zip",xpath,'Talbot'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Taliaferro/115597/313463/reports/detailxml.zip",xpath,'Taliaferro'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Tattnall/115598/313250/reports/detailxml.zip",xpath,'Tattnall'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Taylor/115599/313324/reports/detailxml.zip",xpath,'Taylor'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Telfair/115600/313001/reports/detailxml.zip",xpath,'Telfair'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Terrell/115601/312865/reports/detailxml.zip",xpath,'Terrell'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Thomas/115602/312710/reports/detailxml.zip",xpath,'Thomas'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Tift/115603/312783/reports/detailxml.zip",xpath,'Tift'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Toombs/115604/313065/reports/detailxml.zip",xpath,'Toombs'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Towns/115605/313022/reports/detailxml.zip",xpath,'Towns'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Treutlen/115606/313087/reports/detailxml.zip",xpath,'Treutlen'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Troup/115607/313117/reports/detailxml.zip",xpath,'Troup'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Turner/115608/312786/reports/detailxml.zip",xpath,'Turner'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Twiggs/115609/313129/reports/detailxml.zip",xpath,'Twiggs'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Union/115610/313268/reports/detailxml.zip",xpath,'Union'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Upson/115611/313234/reports/detailxml.zip",xpath,'Upson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Walker/115612/312926/reports/detailxml.zip",xpath,'Walker'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Walton/115613/313357/reports/detailxml.zip",xpath,'Walton'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Ware/115614/313013/reports/detailxml.zip",xpath,'Ware'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Warren/115615/312965/reports/detailxml.zip",xpath,'Warren'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Washington/115616/313239/reports/detailxml.zip",xpath,'Washington'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Wayne/115617/313064/reports/detailxml.zip",xpath,'Wayne'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Webster/115618/313191/reports/detailxml.zip",xpath,'Webster'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Wheeler/115619/312204/reports/detailxml.zip",xpath,'Wheeler'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/White/115620/313473/reports/detailxml.zip",xpath,'White'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Whitfield/115621/312996/reports/detailxml.zip",xpath,'Whitefield'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Wilcox/115622/313059/reports/detailxml.zip",xpath,'Wilcox'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Wilkes/115623/312279/reports/detailxml.zip",xpath,'Wilkes'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Wilkinson/115624/313155/reports/detailxml.zip",xpath,'Wilkenson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Worth/115625/312978/reports/detailxml.zip",xpath,'Worth'))
    candidate=pd.concat(candidate)
    return candidate

Warnock=[]

Warnock = get_candidate_precinct(Warnock,".//Choice[@text='Raphael Warnock (I) (Dem)']")


Warnock.to_csv("Warnock.csv",index=False)
print(Warnock)

