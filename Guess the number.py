import random

# 1. Компьютер загадывает число
secret_number = random.randint(1, 100)

# 2. Счётчик попыток
attempts = 0

# 3. Цикл игры
while True:
    guess = int(input("Введите число от 1 до 100: "))
    attempts += 1

    if guess < secret_number:
        print("Слишком маленькое число!")
    elif guess > secret_number:
        print("Слишком большое число!")
    else:
        print(f"Поздравляю! Вы угадали число {secret_number} за {attempts} попыток.")
        break

