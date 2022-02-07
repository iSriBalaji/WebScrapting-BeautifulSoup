from bs4 import BeautifulSoup as bs
import requests
import re
import io
import os
import csv

path = os.path.dirname(__file__)
csv_path = os.path.join(path,"solar.csv")

#defining regex
website_regex = "^((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9_-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?$"
#getting the source code of webpage
#url = 'https://coreyms.com/'
url = 'https://www.enfsolar.com/7e-future-energy'
html_output_name = 'enfSOLAR.txt'

#Opening CSV file
csv_file = open(csv_path,"w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Company Name','Phone Number','Address','Website'])

req = requests.get(url, 'html.parser')
#print(req.status_code)
#print(req.text)
# with io.open(html_output_name, 'w', encoding="utf-8") as f:
#     f.write(req.text)
#     f.close()

#reading html file and giving it to beautifulsoup (to create object)
# with open('enfSOLAR.txt') as content:
soup = bs(req.text,'lxml')

# To Beautify the HTML
#print(soup.prettify())

#To match a specific tag - First tag content
headings = soup.title.text
#print(headings)

#Using find to pass parameters wile matching
fin = soup.find('div',class_='enf-company-profile-info-main')
#print(fin)

#Getting Company Name
company = fin.h1.text.strip()
print("Company Name is: "+ company)

#Getting Phone Number
phone_no = fin.find('td',class_='ar:number-direction')
contact_no = phone_no.a.text.strip()
print("Phone Number is: "+ contact_no)

#Getting Address
address = fin.div.tr.text.strip()
print("Address is: "+ address)

#Getting Website
website = None
for row in fin.find_all('td'):
    url = re.search(website_regex,row.text.strip())
    if(url!=None):
        website = url.group(0)
        break

if(website!=None):
    print("Website is: "+ website.strip())

csv_writer.writerow([company,contact_no,address,website])
csv_file.close()