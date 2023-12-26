
import re

def get_temp(s):

    matches = re.findall(r'[-+]?\d+°', s)

    # Вилучаємо знак градуса та повертаємо перше числове значення (якщо вони є)
    return int(matches[0][:-1]) if matches else None


print(get_temp('+1°'))