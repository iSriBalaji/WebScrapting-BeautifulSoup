#  Install the Python ScrapingBee library:
# `pip install scrapingbee`
from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='GDNNWD22POJ03YGAM3T08S2F9Z90OWGFMBQGV423Z3MWFDFKFNHM24CRLCHOSQWTO7UXEQRJRTKXMHRR')
response = client.get(
    'http://httpbin.org/anything?json',
      
)
print('Response HTTP Status Code: ', response.status_code)
print('Response HTTP Response Body: ', response.content)