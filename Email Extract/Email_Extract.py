from bs4 import BeautifulSoup as bs
import requests
import re
import sys
import os
import time
import csv
import random

def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url

#defining email regex
email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
e_re = "\S+@\S+"
e_ree = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

user_agent = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"}
def extract(url,time_out):
    try:
        r = requests.get(url, 'html.parser', headers = user_agent, timeout=time_out)
        print(r.status_code)
        if(r.status_code==200):
            return r
        else:
            return None
    except Exception as e:
        print(e)
        return None

path = os.path.dirname(__file__)
csv_path = os.path.join(path,"solarProject.csv")
csv_file = open(csv_path,"r", newline='', encoding='utf-8')
csv_reader = csv.reader(csv_file, delimiter=",")

csv_path2 = os.path.join(path,"solarAustria_CN.csv")
csv_file2 = open(csv_path2,"w", newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file2, delimiter=",")
for n,i in enumerate(csv_reader):
    print("At Index: "+str(n))
    if(n in [0]):
        csv_writer.writerow(['Company Name','Phone Number','Website','Country','Email'])
        continue
    vul = formaturl(i[2])
    print(vul)
    req = extract(vul,7)
    if(req!=None):
        ls=[]
        #soup = bs(req.text,'lxml')
        #print(req.text)
        #url = re.search(email_regex,soup.text)
        url = re.search(email_regex,req.text)
        print("email list = "+ str(url))
        if(url!=None):
            email = url.group(0)
        else:
            email = None
    else:
        email = None
    print("EMAIL: "+ str(email))
    print("|-----------------------------------------|")
    csv_writer.writerow(i+[email])

csv_file.close()
