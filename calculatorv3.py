while True:
    user_input = input("Введите выражение (или введите 'выход' для выхода): ").strip() # Просим пользователя ввести выражение
    
    if user_input.lower() == "выход":
        print("Программа завершена, до свидания!")
        break
    
    try:
        result = eval(user_input) # Используем eval для вычисления выражения
        print(f"Результат: {result}")
    
    except:
        print("Ошибка: неверный формат выражения")
        
    