#Задания:
# Фильтрация: С помощью filter() и отдельной функции-условия оставьте только те товары, которые есть в наличии (in_stock == True) и стоят дешевле 400.
# Сортировка: С помощью sorted() и функции key отсортируйте полученный список доступных товаров сначала по рейтингу (по убыванию), а если рейтинг одинаковый — по цене (по возрастанию). 

products = [
    {"name": "Телефон", "price": 500, "rating": 4.5, "in_stock": True},
    {"name": "Чехол", "price": 15, "rating": 4.8, "in_stock": True},
    {"name": "Наушники", "price": 150, "rating": 4.8, "in_stock": False},
    {"name": "Клавиатура", "price": 80, "rating": 4.2, "in_stock": True},
    {"name": "Монитор", "price": 300, "rating": 4.8, "in_stock": True},
    {"name": "Мышь", "price": 30, "rating": 4.5, "in_stock": True},
]

def in_stock_filter(n):
    return  n['in_stock'] == True and n['price'] < 400 

def func_sorted(n):
    return (-n['rating'], n['price'])
    

filtered_produts = list(filter(in_stock_filter, products))
print(filtered_produts)

sorted_products = sorted(filtered_produts, key=func_sorted)
print("Результат: ")
for item in sorted_products:
    print(item)
 