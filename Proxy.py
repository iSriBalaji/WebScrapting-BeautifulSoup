import random
from bs4 import BeautifulSoup as bs
import requests
import re
import io
import os
import time
import csv

#get the list of free proxies
def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = bs(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies

def extract(proxy,url):
    #this was for when we took a list into the function, without conc futures.
    proxy = random.choice(proxylist)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        #change the url to https://httpbin.org/ip that doesnt block anything
        r = requests.get(url, headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=1)
        print(r.status_code)
        return r
    except:
        pass
    return None

proxylist = getProxies()

path = os.path.dirname(__file__)
csv_path = os.path.join(path,"solarInstaller.csv")

#defining regex
website_regex = "^((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9_-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?$"

#Opening CSV file
# csv_file = open(csv_path,"w")
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['Company Name','Phone Number','Address','Website'])

countries = ["Austria","Belgium","Czech Republic","Denmark","France","Germany","Greece","Italy","Netherlands","Poland","Portugal","Spain","Switzerland","United Kingdom","other_europe","Australia","China","India","Japan","other_apac","Brazil","Canada","Mexico","United States","other_americas","Africa","Middle East"]
pag = [6,8,3,3,8,27,3,21,20,5,2,10,6,23,15,29,4,34,26,15,17,8,4,71,6,16,9]

for n,i in enumerate(countries):
    pages = pag[n]
    for j in range(1,pages+1):
        csv_file = open(csv_path,"w")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Company Name','Phone Number','Address','Website'])
        site = 'https://www.enfsolar.com/directory/installer/'
        url = site+i+"?page="+str(j)
        
        # req = requests.get(url, 'html.parser', timeout=5)
        req = extract(proxylist,url)
        soup = bs(req.text,'lxml')

        fin = soup.find('tbody')
        for tr in fin.find_all('tr'):
            link_com = tr.td.a
            # print(link_com.strip())
            # main_req = requests.get(link_com['href'], 'html.parser', timeout=5)
    
            
            main_req = extract(proxylist,link_com['href'])
            print(main_req.status_code)
            soup2 = bs(main_req.text,'lxml')
            fin = soup2.find('div',class_='enf-company-profile-info-main')

            #Getting Company Name
            try:
                company = fin.h1.text.strip()
                print("At company: "+company)
            except Exception as e:
                company = None

            #Getting Phone Number
            try:
                phone_no = fin.find('td',class_='ar:number-direction')
                contact_no = phone_no.a.text.strip()
            except Exception as e:
                contact_no = None
            
            #Getting Address
            try:
                address = fin.div.tr.text.strip()
            except Exception as e:
                address = None

            #Getting Website
            website = None
            for row in fin.find_all('td'):
                url = re.search(website_regex,row.text.strip())
                if(url!=None):
                    website = url.group(0)
                    break
            
            print(company+" "+str(j))

            csv_writer.writerow([company,contact_no,address,website])
            #time.sleep(5)
        csv_file.close()



