import requests
import time 
import json

def timer(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Запрос выполнился за {duration:.2f}")
        return result
    return wrapper


def save_to_json(func):
    def wrapper(*args, **kwargs):
        result=func(*args, **kwargs)
        with open("crypto.json" , "w") as f:
            json.dump(result, f, indent=4)
        print("Записано в json файл")
        return result
    return wrapper

@timer
@save_to_json
def get_crypto_price(symbol: str):
    response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}")
    price_data=response.json()
    return price_data
    
price_data = get_crypto_price("BTCUSDT")
print(price_data)

