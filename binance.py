
import requests


while True:
    print("[1]-Узнать курс монеты")
    print("[2]-Выйти из программы")
    print("------------------------")
    choice = input("Введите номер: ")
    if choice == "1":
        response = requests.get('https://api.binance.com/api/v3/ticker/price')
        data = response.json()
        found = False
        coin=input("Введите название монеты: ").upper()
        for i in data:
            if i['symbol'] == coin:
                price=float(i['price'])
                print(price)
                found=True
                break
        if not found:
            print("Ошибка: Монета не найдена. Проверьте правильность названия!")
    elif choice == "2":
        break
    else:
        print("Введите правильный номер!")
            
        