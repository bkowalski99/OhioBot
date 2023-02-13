import re


text = "a est"
match = re.search(r'\d+ est', text)
number = match.group(0)[0:2]
if number[1] == ' ':
    number = number[0]

value = (9 + int(number))%12 
if value == 0:
    value = 12
print(str(value))