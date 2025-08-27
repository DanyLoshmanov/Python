#Калькулятор.
num_1 = float(input("Введите первое число: "))
operator = str(input("Введите оператор +, -, *, / : "))
num_2 = float(input("Введите второе число: "))

if operator == "+":
    print(num_1 + num_2)
elif operator == "-":
    print(num_1 - num_2)
elif operator == "*":
    print (num_1 * num_2)
elif operator == "/":
    print(num_1 / num_2)
else:
    print("Неизвестная ошибка!")
