
import requests
from pprint import pprint
from typing import List
    
from scripts.config import settings

def get_data() -> List:
    API_KEY = settings.COINGECKO_API_KEY
    url = "https://api.coingecko.com/api/v3/coins/markets"

    headers = { 
        'x-cg-demo-api-key': API_KEY,
        'accept': 'application/json'
        }

    params = { 
            'vs_currency': 'usd',
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)


if __name__ == "__main__":
    data_test = get_data()
    print(type(data_test))
    #pprint(data_test)