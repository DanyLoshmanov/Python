import random
import string

chars = string.ascii_letters + string.digits + string.punctuation
password = ''

x = int(input('Введите длину пароля: '))
for i in range(x):
    password += random.choice(chars)
print(password)