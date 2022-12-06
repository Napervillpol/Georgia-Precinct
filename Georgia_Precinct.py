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

    zip = ZipFile('detailxml.zip')
    zip.extractall()

    
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
    
    reporting_precincts =reporting('.//Precincts')
   
    
    df = df.merge(reporting_precincts,left_on="Counties",right_on="County")
    df =df.drop(['County'], axis=1)
    
    return df

def safediv(x,y):
    try:
        return x/y
    except ZeroDivisionError:
        return 0

def write_to_excel(race,race_name):
    writer = pd.ExcelWriter('GA_'+race_name+ '.xlsx', engine='xlsxwriter')

    race.mail.to_excel(writer,sheet_name="Mail",index=False)
    race.eday.to_excel(writer,sheet_name="Election Day",index=False)
    race.advance.to_excel(writer,sheet_name="Advance",index=False)
    race.prov.to_excel(writer,sheet_name="Provisonal",index=False)
    race.total.to_excel(writer,sheet_name="Total",index=False)

    writer.save()
class race:
    mail=[]
    eday=[]
    advance=[];
    prov=[]
    total=[]
    def __init__(self, mail,eday,advance,prov,total):
        self.mail=mail
        self.eday=eday
        self.advance=advance
        self.prov=prov
        self.total=total

def assign_race(Dem,Rep,Dem_name,Rep_name):
       
    #Mail 
    Dem_mail = Dem[['ID','Absentee by Mail Votes']]
    Dem_mail.columns=['County',Dem_name]

    Rep_mail = Rep[['ID','Absentee by Mail Votes']]
    Rep_mail.columns=['County',Rep_name]
    mail = Dem_mail.merge(Rep_mail, on='County')
    calculations(mail,Dem_name,Rep_name)
   
    #Election day
    Dem_eday = Dem[['ID','Election Day Votes']]
    Dem_eday.columns=['County',Dem_name]

    Rep_eday = Rep[['ID','Election Day Votes']]
    Rep_eday.columns=['County',Rep_name]
    eday = Dem_eday.merge(Rep_eday, on='County')
    calculations(eday,Dem_name,Rep_name)

    #Advance
    Dem_advance = Dem[['ID','Advance Voting Votes']]
    Dem_advance.columns=['County',Dem_name]

    Rep_advance  = Rep[['ID','Advance Voting Votes']]
    Rep_advance.columns=['County',Rep_name]
    advance = Dem_advance.merge(Rep_advance, on='County')
    calculations(advance,Dem_name,Rep_name)

    #Provisonal
    Dem_prov= Dem[['ID','Provisional Votes']]
    Dem_prov.columns=['County',Dem_name]

    Rep_prov = Rep[['ID','Provisional Votes']]
    Rep_prov.columns=['County',Rep_name]
    prov = Dem_prov.merge(Rep_prov, on='County')
    calculations(prov,Dem_name,Rep_name)

     #Total
    Dem_total= Dem[['ID','Total']]
    Dem_total.columns=['County',Dem_name]

    Rep_total = Rep[['ID','Total']]
    Rep_total.columns=['County',Rep_name]
    total = Dem_total.merge(Rep_total, on='County')
    calculations(total,Dem_name,Rep_name)

    Race = race(mail,eday,advance,prov,total)
    return Race;

def calculations(df,Dem_name,Rep_name):
   
    df[Dem_name]=df[Dem_name].astype(str)
    df[Rep_name]=df[Rep_name].astype(str)
    
    df[Dem_name]=df[Dem_name].str.replace(',','')
    df[Rep_name]=df[Rep_name].str.replace(',','')

    df[Dem_name]=df[Dem_name].astype(int)
    df[Rep_name]=df[Rep_name].astype(int)
    
    df.insert(3, "Total", df[Dem_name]+df[Rep_name])
    df.insert(4, "Net Votes", df[Dem_name]-df[Rep_name])
    df.insert(5, Dem_name+" Pct", df[Dem_name]/(df[Dem_name]+df[Rep_name]))
    df.insert(6, Rep_name+" Pct", df[Rep_name]/(df[Dem_name]+df[Rep_name]))
    df.insert(7, "Margin",(df[Dem_name]/(df[Dem_name]+df[Rep_name])) -(df[Rep_name]/(df[Dem_name]+df[Rep_name])))

def calculate_shift(df_2022,df_2020):
     
     df_2022.mail.insert(8, "Pct Shift",df_2022.mail["Margin"]-df_2020.mail["Margin"])
     df_2022.mail.insert(9, "Turnout",df_2022.mail["Total"]/df_2020.mail["Total"])

     df_2022.eday.insert(8, "Pct Shift",df_2022.eday["Margin"]-df_2020.eday["Margin"])
     df_2022.eday.insert(9, "Turnout",df_2022.eday["Total"]/df_2020.eday["Total"])

     df_2022.advance.insert(8, "Pct Shift",df_2022.advance["Margin"]-df_2020.advance["Margin"])
     df_2022.advance.insert(9, "Turnout",df_2022.advance["Total"]/df_2020.advance["Total"])

     df_2022.prov.insert(8, "Pct Shift",df_2022.prov["Margin"]-df_2020.prov["Margin"])
     df_2022.prov.insert(9, "Turnout",df_2022.prov["Total"]/df_2020.prov["Total"])

     df_2022.total.insert(8, "Pct Shift",df_2022.total["Margin"]-df_2020.total["Margin"])
     df_2022.total.insert(9, "Turnout",df_2022.total["Total"]/df_2020.total["Total"])

def reporting(xpath):
    header=[]
    pct_reporting=[]
    
    tree = etree.parse('detail.xml')
    root = tree.getroot()
    
    for Counties in root.find(xpath):
        header.append(Counties.attrib['name'])
        pct_reporting.append(Counties.attrib['percentReporting'])
    df2 = pd.DataFrame( pct_reporting,columns=['percentReporting'])

    df = pd.DataFrame(header,columns=['County'])
    df=df.join(df2, how='outer')
    return df

def Statmodels(Previous_race,Current_race,Previous_name,Current_name,Title,w):
    
    plt.title(Title)
    plt.xlabel(Previous_name)
    plt.ylabel(Current_name)
    
    merged = Current_race.merge(Previous_race,on="County")
    merged =  merged.loc[(Previous_race["Total"]!=0) & (Current_race["Total"]!=0) & (Current_race["percentReporting"].astype(int)>2)]
    
    x = merged[Previous_name]
    y = merged[Current_name]
    z = merged["Total_y"]/1000
   
    
    plt.scatter(x,y,z)

    wls_model = sm.WLS(y,x,z)
    results = wls_model.fit()
    
    
    plt.plot(x,results.fittedvalues,'-g')
    
    xpoint = pd.DataFrame(x, columns=['Warnock Pct'])
    ypoint = pd.DataFrame(results.fittedvalues, columns=['expected'])
    newline = pd.merge(xpoint, ypoint, left_index=True, right_index=True)
    newline =newline.sort_values(by=['expected']).reset_index(drop=True)
    
    swing = (newline.iloc[0][1] - newline.iloc[0][0] + newline.iloc[-1][1] - newline.iloc[-1][0])
    print("{} swing: {:.1%}".format(Title,swing))
    x = np.linspace(0,1,5)
    y = x
   
    plt.grid()
    plt.plot(x, y, '-r', label='y=x+1')

    plt.show()


def get_candidate_precinct(candidate,xpath):
   
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Appling/116566/314864/reports/detailxml.zip",xpath,'Appling')) 
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Atkinson/116567/314865/reports/detailxml.zip",xpath,'Atkinson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bacon/116568/314866/reports/detailxml.zip",xpath,'Bacon'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Baker/116569/314867/reports/detailxml.zip",xpath,'Baker'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Baldwin/116570/314868/reports/detailxml.zip",xpath,'Baldwin'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Banks/116571/314869/reports/detailxml.zip",xpath,'Banks'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Barrow/116572/314870/reports/detailxml.zip",xpath,'Barrow'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bartow/116573/314871/reports/detailxml.zip",xpath,'Bartow'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Ben_Hill/116574/314872/reports/detailxml.zip",xpath,'Ben Hill'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Berrien/116575/314873/reports/detailxml.zip",xpath,'Berrien'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bibb/116576/314875/reports/detailxml.zip",xpath,'Bibb'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bleckley/116577/314876/reports/detailxml.zip",xpath,'Bleckley'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Brantley/116578/314877/reports/detailxml.zip",xpath,'Brantley'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Brooks/116579/314878/reports/detailxml.zip",xpath,'Brooks'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bryan/116580/314879/reports/detailxml.zip",xpath,'Bryan'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Bulloch/116581/314880/reports/detailxml.zip",xpath,'Bulloch'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Burke/116582/315053/reports/detailxml.zip",xpath,'Burke'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Butts/116583/314882/reports/detailxml.zip",xpath,'Butts'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Calhoun/116584/314883/reports/detailxml.zip",xpath,'Calhoun'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Camden/116585/314884/reports/detailxml.zip",xpath,'Camden'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Candler/116586/314885/reports/detailxml.zip",xpath,'Candler'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Carroll/116587/315054/reports/detailxml.zip",xpath,'Carroll'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Catoosa/116588/314887/reports/detailxml.zip",xpath,'Catoosa'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Charlton/116589/314888/reports/detailxml.zip",xpath,'Charlton'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Chatham/116590/314889/reports/detailxml.zip",xpath,'Chatham'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Chattahoochee/116591/314890/reports/detailxml.zip",xpath,'Chattahoochee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Chattooga/116592/314891/reports/detailxml.zip",xpath,'Chattooga'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Cherokee/116593/314892/reports/detailxml.zip",xpath,'Cherokee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Clarke/116594/314893/reports/detailxml.zip",xpath,'Clarke'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Clay/116595/314894/reports/detailxml.zip",xpath,'Clay'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Clayton/116596/314895/reports/detailxml.zip",xpath,'Clayton'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Clinch/116597/314896/reports/detailxml.zip",xpath,'Clinch'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Cobb/116598/314897/reports/detailxml.zip",xpath,'Cobb'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Coffee/116599/314898/reports/detailxml.zip",xpath,'Coffee'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Colquitt/116600/314899/reports/detailxml.zip",xpath,'Colquitt'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Columbia/116601/314900/reports/detailxml.zip",xpath,'Columbia'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Cook/116602/314901/reports/detailxml.zip",xpath,'Cook'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Coweta/116603/314902/reports/detailxml.zip",xpath,'Coweta'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Crawford/116604/314903/reports/detailxml.zip",xpath,'Crawford'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Crisp/116605/314904/reports/detailxml.zip",xpath,'Crisp'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dade/116606/314906/reports/detailxml.zip",xpath,'Dade'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dawson/116607/314907/reports/detailxml.zip",xpath,'Dawson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Decatur/116608/314908/reports/detailxml.zip",xpath,'Decatur'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/DeKalb/116609/314909/reports/detailxml.zip",xpath,'DeKalb'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dodge/116610/314910/reports/detailxml.zip",xpath,'Dodge'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dooly/116611/314911/reports/detailxml.zip",xpath,'Dooly'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Dougherty/116612/314912/reports/detailxml.zip",xpath,'Dougherty'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Douglas/116613/314913/reports/detailxml.zip",xpath,'Douglas'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Early/116614/314914/reports/detailxml.zip",xpath,'Early'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Echols/116615/314915/reports/detailxml.zip",xpath,'Echols'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Effingham/116616/314916/reports/detailxml.zip",xpath,'Effingham'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Elbert/116617/314917/reports/detailxml.zip",xpath,'Elbert'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Emanuel/116618/314918/reports/detailxml.zip",xpath,'Emanuel'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Evans/116619/314919/reports/detailxml.zip",xpath,'Evans'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Fannin/116620/314922/reports/detailxml.zip",xpath,'Fannin'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Fayette/116621/315049/reports/detailxml.zip",xpath,'Fayette'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Floyd/115523/313114/reports/detailxml.zip",xpath,'Floyd'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Forsyth/116623/315055/reports/detailxml.zip",xpath,'Forsyth'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Franklin/116624/314926/reports/detailxml.zip",xpath,'Franklin'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Fulton/116625/315067/reports/detailxml.zip",xpath,'Fulton'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Gilmer/116626/314928/reports/detailxml.zip",xpath,'Gilmer'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Glascock/116627/314929/reports/detailxml.zip",xpath,'Glascock'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Glynn/116628/314930/reports/detailxml.zip",xpath,'Glynn'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Gordon/116629/314931/reports/detailxml.zip",xpath,'Gordon'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Grady/116630/314932/reports/detailxml.zip",xpath,'Grady'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Greene/116631/314933/reports/detailxml.zip",xpath,'Greene'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Gwinnett/116632/314934/reports/detailxml.zip",xpath,'Gwinnett'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Habersham/116633/314936/reports/detailxml.zip",xpath,'Habersham'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Hall/116634/314937/reports/detailxml.zip",xpath,'Hall'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Hancock/116635/314938/reports/detailxml.zip",xpath,'Hancock'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Haralson/116636/314939/reports/detailxml.zip",xpath,'Haralson'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Harris/116637/314940/reports/detailxml.zip",xpath,'Harris'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Hart/116638/314941/reports/detailxml.zip",xpath,'Hart'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Heard/116639/314942/reports/detailxml.zip",xpath,'Heard'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Henry/116640/314943/reports/detailxml.zip",xpath,'Henry'))
    candidate.append(get_data( "https://results.enr.clarityelections.com//GA/Houston/116641/314944/reports/detailxml.zip",xpath,'Houston'))
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

Warnock = pd.read_csv("Data/Warnock.csv")
Walker = pd.read_csv("Data/Walker.csv")
Abrams = pd.read_csv("Data/Abrams.csv")
Kemp = pd.read_csv("Data/Kemp.csv")

Warnock =[]
Walker=[]

Warnock = get_candidate_precinct(Warnock,'.//Choice[@text="Raphael Warnock (I) (Dem)"]')
Walker = get_candidate_precinct(Walker,'.//Choice[@text="Herschel Junior Walker (Rep)"]')

reporting_precincts=Warnock.drop(['Counties','Absentee by Mail Votes','Advance Voting Votes', 'Election Day Votes', 'Provisional Votes',  'Total'], axis=1)


Senate =assign_race(Warnock,Walker,"Warnock","Walker")
Governor =assign_race(Abrams,Kemp,"Abrams","Kemp")
calculate_shift(Governor,Senate)

#Governor.total=Governor.total.merge(reporting_precincts,left_on="County",right_on="ID")
#Governor.total=Governor.total.drop(['ID'], axis=1)

#write_to_excel(Governor,"Governor")

#Statmodels(Senate.total,Governor.total,"Warnock Pct","Abrams Pct","GA",Senate.total['Total']/1000)
