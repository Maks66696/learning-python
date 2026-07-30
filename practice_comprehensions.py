# Задание 1: Фильтрация и умножение (List Comprehension):

numbers = [12, 5, 8, 19, 21, 4, 10]
result= [x * 2 for x in numbers if x > 10]
print(result)

# Задание 2: Оценки и статус (If-Else в Comprehension):

scores = [85, 42, 90, 58, 73]
statuses = ["Pass" if x>=60 else "Fail" for x in scores]
print(statuses)


# Задание 3: Словарь длин слов (Dict Comprehension):

words = ["python", "code", "script", "api"]
word_lengths={word: len(word) for word in words}
print(word_lengths)