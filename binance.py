import json
import requests
coins_keys={}

while True:
    print("[1]-Узнать курс монеты")
    print("[2]-Записать значения монет в json")
    print("[3]-Выйти из программы")
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
                coins_keys[coin] = price
                break
        if not found:
            print("Ошибка: Монета не найдена. Проверьте правильность названия!")


    elif choice == "2":
       if not coins_keys:
           print("Сначала найдите хотя бы одну монету через пункт [1]!")
       else:
            with open("coins_keys.json", "w") as file:
                json.dump(coins_keys, file, indent=4)
                print("Данные успешно сохранены в coins_keys.json!")
    elif choice == "3":
        break

    else:
        print("Введите правильный номер!")
            
        