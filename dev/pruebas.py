import requests
from bs4 import BeautifulSoup
import certifi
import chardet

# URL de prueba en httpbin para capturar detalles de la solicitud
test_url = "https://httpbin.org/anything"
real_url = "https://www.google.com/search?q=lira+turca+a+dolar"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'identity',  # Cambiado para deshabilitar la compresión
    'Connection': 'keep-alive'
}

# Realizar la solicitud de prueba
response = requests.get(test_url, headers=headers, verify=certifi.where())
print("Test URL Response:")
print(response.json())

# Realizar la solicitud real
r = requests.get(real_url, headers=headers, verify=certifi.where())
detected_encoding = chardet.detect(r.content)['encoding']
if detected_encoding is None:
    detected_encoding = 'utf-8'  # Valor predeterminado si no se detecta la codificación
print("Detected Encoding:", detected_encoding)

try:
    content = r.content.decode(detected_encoding)  # Decodificación automática
except UnicodeDecodeError:
    content = r.content.decode('ISO-8859-1')  # Intentar con una codificación alternativa

print("Content (first 1000 chars):", content[:1000])

soup = BeautifulSoup(content, "html5lib")
requested_price = soup.find_all("span", class_="DFlfde SwHCTb")
dolar_tr = [price['data-value'] for price in requested_price]

if dolar_tr:
    dolar_tr = float(dolar_tr[0])
    print("A dolar is equal to {} TRY".format(dolar_tr))
else:
    print("No exchange rate found")
