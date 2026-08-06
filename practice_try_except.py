def find_result(number,number_user):
    return number / number_user


try:
    number = 100
    user_input = input("Введите число: ")
    number_user = float(user_input)
    result = find_result(number, number_user)
    print("Результат: ", result)
except ValueError:
    print("Вы ввели буквы. Введите число")
except ZeroDivisionError:
    print("На ноль нельзя делить, введите число")

