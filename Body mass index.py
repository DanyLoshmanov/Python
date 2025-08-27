#1. Запрашиваем вес и рост.
Weight_input = input("Введите ваш вес в киллограммах: ")
Height_input = input("Введите ваш рост в сантиметрах: ")

#2. Преобразуем данные в float.
Weight = float(Weight_input)
Height_m = float(Height_input) / 100 #Рост в метрах

#3. Рассчитываем ИМТ.
bmi = Weight / (Height_m ** 2) #Формула ИМТ (Масса тела поделенная на рост(в метрах) во второй степени)

#4. Отчет.
bmi_value = f"{bmi:.1f}" # ИМТ с одним знаком после запятой (строка)
report = f"Вес:{Weight}кг. | Рост:{Height_m}м. | ИМТ:{bmi_value}"
print(report)

#5. Интерпретация результата.
if bmi < 18.5:
    print("Недостаточный вес")
elif 18.5 <= bmi < 25:
    print("Нормально")
elif 25 <= bmi < 30:
    print("Избыточный вес")
else:
    print("Ожирение")

#6. Ввыводим типы переменных.
print(type(Weight))
print(type(Height_m))
print(type(bmi))
print(type(bmi_value))