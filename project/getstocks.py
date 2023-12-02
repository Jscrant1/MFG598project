import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def getstocks(symbols=['AAPL'], startdate=str(datetime.date.isoformat(datetime.date.today())), enddate=str(datetime.date.isoformat(datetime.date.today()))):
    api_key =  'hTLKlMuw5ldrrTAjP0V8znziycvnbqP_' # This is the api key for polygon.io a stock api  
    for symbol in symbols:
        try:
            response = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{startdate}/{enddate}?adjusted=true&sort=asc&limit=120&apiKey={api_key}')
            data = response.json()
            print(data)
            if 'results' in data:
                results = data['results']
                df = pd.DataFrame(results)
                df['t'] = pd.to_datetime(df['t'], unit='ms')
                df.set_index('t', inplace=True)
                print(df)
            else:
                print(f"No results for {symbol}")
        except Exception as e:
            print(f'Error occurred while fetching {symbol}: {e}')
    return df 

if __name__ == "__main__":
    symbol = ['AAPL', 'GOOGL']
    startdate = '2023-01-05'
    enddate = '2023-01-09'
    getstocks(symbol,startdate,enddate)