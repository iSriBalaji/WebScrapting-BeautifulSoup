from bs4 import BeautifulSoup as bs
import requests
import re
import io
import os
import time
import csv
import random

path = os.path.dirname(__file__)
csv_path = os.path.join(path,"solarInstaller.csv")

#defining regex
website_regex = "^((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9_-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?$"

#Opening CSV file
# csv_file = open(csv_path,"w")
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['Company Name','Phone Number','Address','Website'])

proxylist = ["50.206.25.104:80","196.15.221.200:80","88.198.50.103:3128","198.50.163.192:3129","203.33.113.34:80","51.68.206.76:999","41.79.191.183:80","5.252.161.48:8080","101.32.191.99:22225","198.199.86.11:8080","122.154.100.210:80","154.86.146.203:6666","103.99.3.181:30150","186.0.176.147:443","88.198.50.103:8080","176.9.75.42:3128","51.222.21.92:32768","170.244.210.107:999","159.203.61.169:3128","51.222.21.94:32768","46.4.96.137:3128","209.97.150.167:8080","46.5.252.52:8080","124.83.75.239:8080","51.81.82.175:2003","128.199.202.122:3128","128.199.239.230:8080","221.141.130.183:33741","77.73.241.154:80","160.19.232.85:3128","52.78.172.171:80","139.59.1.14:3128","213.230.97.10:3128","192.162.193.243:36910","103.89.136.77:3128","78.111.97.181:3141","103.26.130.156:55443","209.97.150.167:3128","88.82.95.146:3128","51.81.82.175:80","134.122.93.93:8080","119.82.252.25:42914","88.198.24.108:8080","43.129.186.179:8080","103.156.57.66:3127","5.149.219.201:8080","88.198.24.108:3128","79.119.154.182:53281","118.174.146.131:80","89.140.125.17:80","198.199.86.11:3128","170.82.115.196:999","68.185.57.66:80","161.35.70.249:8080","5.16.0.77:1256","103.99.3.181:30172","46.4.96.137:8080","5.252.161.48:3128","82.202.249.158:8181","193.117.138.126:44805","81.19.0.135:3128","118.70.109.148:55443","23.251.138.105:8080","161.35.70.249:3128","182.93.10.83:8090","79.143.87.140:9090","170.254.18.38:8888","103.161.165.12:8181","103.102.60.81:8080","157.65.169.201:3128","138.68.60.8:8080","202.180.54.97:8080","103.199.84.122:8080","181.78.11.219:999","91.194.53.21:9090","24.113.42.177:48678","149.126.98.162:9090","46.5.252.70:3128","102.129.249.120:8080","186.211.177.161:8082","190.1.201.58:8080","95.216.106.38:3128","173.249.38.220:80","136.228.141.154:80","154.0.155.205:8080","212.77.138.161:41258","77.242.22.14:8088","49.231.174.182:8080","160.154.48.46:8080","89.232.195.157:6000","139.162.78.109:3128","51.222.21.95:32768","50.206.25.106:80","45.156.31.30:9090","144.76.60.10:3128","13.86.159.104:3128","191.96.71.118:8080","119.18.151.49:8080","193.150.117.102:8000","103.99.3.181:30076","201.132.105.30:8080","179.189.27.37:8080","193.193.240.37:45944","104.238.195.10:80","50.206.25.111:80","92.204.129.161:80","140.227.31.223:6000","50.206.25.110:80","85.15.152.39:3128","176.9.119.170:3128","128.199.214.87:3128","140.227.32.79:6000","102.129.249.120:3128","136.228.141.154:8080","152.67.0.123:80","140.227.73.61:3128","179.49.161.74:999","140.227.80.43:3128","176.9.119.170:8080","167.71.5.83:3128","85.26.146.169:80","181.129.52.155:42648","206.161.234.197:80","223.25.99.115:9999","78.45.30.184:8080","88.255.234.197:80","79.143.87.117:9090","138.68.60.8:3128","51.159.154.37:3128","185.38.111.1:8080","47.241.17.89:8888","193.164.6.20:9999","196.15.221.205:80","149.172.255.12:8080","154.16.63.16:3128","182.237.16.7:83","50.206.25.109:80","159.69.66.224:8080","171.99.131.78:8080","41.223.119.156:3128","131.161.68.37:31264","95.216.10.237:5008","66.119.169.237:80","68.188.59.198:80","177.93.33.219:999","203.33.113.46:80","139.59.1.14:8080","119.28.68.91:8080","154.86.147.227:6666","190.217.100.64:8182","05.252.161.48:8080","175.111.181.26:56297","178.47.139.151:35102","176.9.75.42:8080","154.16.63.16:8080","159.203.61.169:8080","167.71.5.83:8080","191.252.194.68:3128","178.219.31.252:8080","177.71.77.202:20183","191.96.42.80:8080","103.102.14.8:3127","191.96.71.118:3128","191.96.42.80:3128","218.111.228.178:80","191.102.125.245:8080","82.64.183.22:8080","139.162.78.109:8080","79.173.64.46:3128","203.33.113.43:80","110.164.59.98:8080","128.199.202.122:8080","37.228.65.107:32052","47.243.68.117:8080","91.233.111.49:1080","218.102.106.139:3128","12.239.213.215:8080","103.99.8.106:83","186.159.3.43:30334","5.252.195.253:3128","190.120.249.248:999","45.42.177.21:3128","88.255.234.198:80","103.145.185.123:8080","91.206.148.243:61410","45.80.47.205:8080","203.33.113.62:80"]
#defining a request function
def extract(url,time_out,proxy):
    prox = random.choice(proxy)
    try:
        r = requests.get(url, 'html.parser',proxies={'http' : str(prox)}, timeout=time_out)
        print(r.status_code)
        if(r.status_code==200):
            return r
        else:
            return None
    except Exception as e:
        print(e)
        return None

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
        
        #req = requests.get(url, 'html.parser', timeout=5)
        req = extract(url,5,proxylist)
        while(1):
            if req!=None:
                soup = bs(req.text,'lxml')

                fin = soup.find('tbody')
                for tr in fin.find_all('tr'):
                    link_com = tr.td.a
                    # print(link_com.strip())
                    proxy = random.choice(proxylist)
                    main_req = requests.get(link_com['href'], 'html.parser',proxies={'http' : str(proxy)}, timeout=5)
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
                    try:
                        for row in fin.find_all('td'):
                            url = re.search(website_regex,row.text.strip())
                            if(url!=None):
                                website = url.group(0)
                                break
                    except Exception as e:
                        website = None
                    
                    print(company+" "+str(j))

                    csv_writer.writerow([company,contact_no,address,website])
                    #time.sleep(5)
            else:
                time.sleep(10)
                req = extract(url,5,proxylist)

        csv_file.close()



