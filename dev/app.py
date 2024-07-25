from flask import Flask, render_template, request, send_from_directory
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Setting to get Pics folder right
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'pics')

@app.route('/pics/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        items = request.form.getlist('games')
        items = [i for i in items if i.strip()]  # Remove empty or whitespace-only items
        
        if not items:
            return render_template('index.html', message="No se ha insertado ningún juego para buscar.")

        us_urls = [f"https://psdeals.net/us-store/search?search_query={i.replace(' ', '+')}" for i in items]
        tr_urls = [f"https://psdeals.net/tr-store/search?search_query={i.replace(' ', '+')}" for i in items]

        us_games_info = fetch_game_info(us_urls, items, 'USD')
        tr_games_info = fetch_game_info(tr_urls, items, 'TRY')

        for game, details in tr_games_info.items():
            for detail in details:
                for us_detail in us_games_info.get(game, []):
                    if detail['Platform'] == us_detail['Platform']:
                        detail['Price (USD)'] = us_detail['Price (USD)']

        data = []
        for game, details in tr_games_info.items():
            if details:  # Check if details list is not empty
                for detail in details:
                    detail['Game'] = game
                    data.append(detail)
            else:
                data.append({'Game': game, 'Platform': 'N/A', 'Price (TRY)': 'N/A', 'Price (USD)': 'N/A'})

        if not data:
            return render_template('index.html', message="No se han encontrado resultados para los juegos buscados.")

        df = pd.json_normalize(data)

        url = "https://www.google.com/search?q=lira+turca+a+dolar&oq=lira+turca+a+dolar&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARAuGEDSAQgyMzU4ajBqMagCALACAA&sourceid=chrome&ie=UTF-8"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'identity',
            'Connection': 'keep-alive'
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        requested_price = soup.find_all("span", class_="DFlfde SwHCTb")
        dolar_tr = [price['data-value'] for price in requested_price]
        dolar_tr = float(dolar_tr[0])
        print("A dolar is equal to {} TRY".format(dolar_tr))

        # Clean and convert price columns
        df["Price (TRY)"] = df["Price (TRY)"].str.replace("TL", "").str.replace("FREE", "0").str.replace(",", "").replace('N/A', '0')
        df["Price (USD)"] = df["Price (USD)"].str.replace("FREE", "0").str.replace("$", "").replace('N/A', '0')

        df["Price (USD)"] = pd.to_numeric(df["Price (USD)"], errors='coerce').fillna(0)
        df["Price (TRY)"] = pd.to_numeric(df["Price (TRY)"], errors='coerce').fillna(0)
        
        df["Price (TRY - USD)"] = round(df["Price (TRY)"] * dolar_tr, 2)
        df["Difference (US store - TR store)"] = round(df["Price (USD)"] - df["Price (TRY)"] * dolar_tr, 2)
        df = df.iloc[:, [0, 1, 3, 5, 6, 2]]

        return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    return render_template('index.html')

def fetch_game_info(urls, items, region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'identity',
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
                        'Name': name,
                        f'Price ({region})': price,
                        'Platform': platform
                    })

            if not product_details:
                product_details.append({
                    'Name': 'Not found',
                    f'Price ({region})': 'N/A',
                    'Platform': 'N/A'
                })

            games_info[item] = product_details

        except requests.RequestException as e:
            print(f"Error fetching data for {item} ({region}): {e}")
            if item not in games_info:
                games_info[item] = [{
                    'Name': 'No encontrado',
                    f'Price ({region})': 'N/A',
                    'Platform': 'N/A'
                }]

    return games_info

if __name__ == '__main__':
    # Using any IP to connect to this data when deployed
    app.run(host='0.0.0.0', port=5000, debug=True)
