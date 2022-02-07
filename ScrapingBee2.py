#  Install the Python Requests library:
# `pip install requests`
import requests

def send_request():
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': 'GDNNWD22POJ03YGAM3T08S2F9Z90OWGFMBQGV423Z3MWFDFKFNHM24CRLCHOSQWTO7UXEQRJRTKXMHRR',
            'url': 'http://httpbin.org/anything?json',  
        },
        
    )
    print('Response HTTP Status Code: ', response.status_code)
    print('Response HTTP Response Body: ', response.content)
send_request()
