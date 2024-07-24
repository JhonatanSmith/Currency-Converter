import requests
from bs4 import BeautifulSoup
import certifi
import chardet
url = "https://www.google.com/search?q=lira+turca+a+dolar&oq=lira+turca+a+dolar&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARAuGEDSAQgyMzU4ajBqMagCALACAA&sourceid=chrome&ie=UTF-8"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'identity',
    'Connection': 'keep-alive'
}
r = requests.get(url, headers=headers)
print(r.text)
soup = BeautifulSoup(r.text, "lxml")
requested_price = soup.find_all("span", class_="DFlfde SwHCTb")
dolar_tr = [price['data-value'] for price in requested_price]
dolar_tr = float(dolar_tr[0])
print("A dolar is equal to {} TRY".format(dolar_tr))