# Web scrapying
from bs4 import BeautifulSoup # modulo de BeautifulSoup
import requests
import ssl
import json

# Data manipulation
import pandas as pd
import numpy as np

# # 1st step: We will ask for the games we are interested in
def search_games():
    """
    Generates search URLs for the given items.

    Args: 
        None. The games' names are provided by the user through the console.

    Returns:
        List[str]: A list of URLs to search for the specified games.
    """
    items = []
    while True:
        game = input("Insert a game (or press enter to finish): ")
        if game == "":
            break
        items.append(game)

    base_url = "https://psdeals.net/tr-store/search?search_query="
    urls = [base_url + i.replace(" ", "+") for i in items]

    us_base_url = "https://psdeals.net/us-store/search?search_query="
    us_urls = [us_base_url + i.replace(" ", "+") for i in items]

    print("You asked for: {}".format(", ".join(items)))
    return us_urls, urls, items

def fetch_game_info(urls, items, region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    games_info = {}
    for url, item in zip(urls, items):
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            print(f"Fetched data for {item} ({region}): Status code {r.status_code}")
            
            soup = BeautifulSoup(r.text, "lxml")
            product_details = []

            products = soup.find_all('div', class_='game-collection-item')

            for product in products:
                name_tag = product.find('span', class_='game-collection-item-details-title')
                price_tag = product.find('span', class_='game-collection-item-price')
                platform_tag = product.find('span', class_='game-collection-item-top-platform')

                if name_tag and price_tag and platform_tag:
                    name = name_tag.get_text(strip=True) 
                    price = price_tag.get_text(strip=True)  
                    platform = platform_tag.get_text(strip=True)  
                    product_details.append({
                        'Name': name,  # Keep the name for later merge
                        f'Price ({region})': price,
                        'Platform': platform
                    })
            
            games_info[item] = product_details

        except requests.RequestException as e:
            print(f"Error fetching data for {item} ({region}): {e}")
            if item not in games_info:
                games_info[item] = []

    return games_info

# Get the names and the URLs
us_urls, tr_urls, items = search_games()

# Fetch the game information from Turkey store
tr_games_info = fetch_game_info(tr_urls, items, 'TRY')

# Fetch the game information from US store
us_games_info = fetch_game_info(us_urls, items, 'USD')

# Merge the information
for game, details in tr_games_info.items():
    for detail in details:
        for us_detail in us_games_info.get(game, []):
            if detail['Platform'] == us_detail['Platform']:
                detail['Price (USD)'] = us_detail['Price (USD)']

# Convert the dictionary to a DataFrame
data = []
for game, details in tr_games_info.items():
    for detail in details:
        detail['Game'] = game  # Ensure the game name from the Turkish store is kept
        data.append(detail)

df = pd.json_normalize(data)

# This URL will be the same so it requieres no changes
url = "https://www.google.com/search?q=lira+turca+a+dolar&oq=lira+turca+a+dolar&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARAuGEDSAQgyMzU4ajBqMagCALACAA&sourceid=chrome&ie=UTF-8"
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "lxml")
requested_price = soup.find_all("span",class_="DFlfde SwHCTb")
dolar_tr = [price['data-value'] for price in requested_price]
dolar_tr = float(dolar_tr[0])
print("A dolar is equal to {} TRY".format(dolar_tr))
df["Price (TRY)"]=df["Price (TRY)"].str.replace("TL", "")
df["Price (TRY)"]=df["Price (TRY)"].str.replace("FREE", "0")
df["Price (TRY)"]=df["Price (TRY)"].str.replace(",", "")
df["Price (USD)"]=df["Price (USD)"].str.replace("$", "")
df["Price (USD)"] = df["Price (USD)"].astype(float)
df["Price (TRY)"] = df["Price (TRY)"].astype(float)
df["Price (TRY - USD)"] = round(df["Price (TRY)"] * dolar_tr,2)
df["Difference (US tore- TR store)"] = round( df["Price (USD)"] -df["Price (TRY)"] * dolar_tr,2)
df = df.iloc[:,[0,1,3,5,6,2]]
print(df)
df.to_csv("../data/processed/games_data.csv", index=False)