from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import requests
from bs4 import BeautifulSoup
import pandas as pd

class ScraperApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.input_game = TextInput(hint_text='Insert a game')
        self.layout.add_widget(self.input_game)
        
        self.submit_btn = Button(text='Submit')
        self.submit_btn.bind(on_press=self.search_games)
        self.layout.add_widget(self.submit_btn)
        
        self.result_label = Label(text='')
        self.layout.add_widget(self.result_label)
        
        return self.layout
    
    def search_games(self, instance):
        game = self.input_game.text
        if game:
            self.result_label.text = f"Searching for {game}..."
            self.fetch_game_info([game])
    
    def fetch_game_info(self, games):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        us_base_url = "https://psdeals.net/us-store/search?search_query="
        tr_base_url = "https://psdeals.net/tr-store/search?search_query="
        
        us_urls = [us_base_url + game.replace(" ", "+") for game in games]
        tr_urls = [tr_base_url + game.replace(" ", "+") for game in games]
        
        us_games_info = self.fetch_prices(us_urls, games, 'USD')
        tr_games_info = self.fetch_prices(tr_urls, games, 'TRY')
        
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
                detail['Game'] = game
                data.append(detail)
        
        df = pd.json_normalize(data)
        df.to_csv("/mnt/sdcard/games_data.csv", index=False)
        self.result_label.text = "Data saved to games_data.csv"

    def fetch_prices(self, urls, games, region):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        games_info = {}
        for url, game in zip(urls, games):
            try:
                r = requests.get(url, headers=headers)
                r.raise_for_status()
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
                
                games_info[game] = product_details
            
            except requests.RequestException as e:
                print(f"Error fetching data for {game} ({region}): {e}")
                if game not in games_info:
                    games_info[game] = []
        
        return games_info

if __name__ == '__main__':
    ScraperApp().run()
