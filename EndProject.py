import requests
import pymysql
import re
from bs4 import BeautifulSoup
state = input('please enter name of a state in Germany in lowercase for example berlin: ')
city = input('please enter name of a city in Germany in lowercase for example berlin: ')
found = requests.get('https://www.immobilienscout24.de/Suche/de/%s/%s/wohnung-kaufen?pagenumber=1' %(state,city))
soup = BeautifulSoup(found.text, 'html.parser')
numpages = soup.find('div', attrs = {'class':"select-input-wrapper"})
x = '12345678910111213'
page = 1
if (numpages != None) and (x in numpages.text):
    page = 14
    cnx = pymysql.connect('localhost','root','','learn')
    cursr = cnx.cursor()
    for f in range(1,page):
        findings = requests.get('https://www.immobilienscout24.de/Suche/de/%s/%s/wohnung-kaufen?pagenumber=%i' %(state,city,f))    
        soup2 = BeautifulSoup(findings.text, 'html.parser')
        pricsizroomn = soup2.find_all('dd', attrs = {'class':'font-nowrap'})
        for specif in pricsizroomn:
            gheymat = re.findall(r'.+€',specif.text)
            for unitpric in gheymat:
                unitpric = re.sub(r' €' ,'', unitpric)
                unitpric = re.sub(r'\.*','',unitpric)
                unitpric = float(unitpric)            
            sizeapp = re.findall(r'.+m²',specif.text)
            for size in sizeapp:
                size = re.sub(r' m²' ,'', size)
                size = re.sub(r',','.',size)
                size = float(size)
            roomsnumb = re.findall(r'Zi.+',specif.text)
            for rooms in roomsnumb:
                rooms = re.sub(r'Zi\.','', rooms)
                rooms = re.sub(r',','.',rooms) 
                rooms = float(rooms)
                cursr.execute('INSERT INTO houses VALUES (\'%s\',%f,%f,%f)' %(city,unitpric,size,rooms))
                cnx.commit()
    cursr2 = cnx.cursor()
    inx =[]
    cursr3 = cnx.cursor()
    outy = []
    from sklearn import tree
    clf = tree.DecisionTreeClassifier()
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    f = le.fit([city])
    city = le.transform([city])
    cursr2.execute('SELECT %i, size, roomnumber FROM houses'%city)
    for row in cursr2:
        inx.append(row)
    cursr3.execute('SELECT price FROM houses')
    for row in cursr3:
        outy.append(row)
    clf = clf.fit(inx,outy)
    newsize = input('please enter size of a house: ')
    newroomnumber = input('please enter roomnumber: ')
    newsize = float(newsize)
    newroomnumber = float(newroomnumber)
    newdata = [[city,newsize,newroomnumber]]
    answer = clf.predict(newdata)
    print(answer[0])
    cnx.close()
else:
    print('there are not enough data, please enter another city')