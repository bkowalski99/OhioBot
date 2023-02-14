import re


text = "645 est"
match = re.search(r'\d+ est', text)
number = match.group(0)[0:-4]
if len(number) == 4:
    number = ((9 + int(number[0:2]))%12)*100 + int(number[2:4])
    value =  int(number) 
elif len(number) == 3:
    number = ((9 + int(number[0:1]))%12)*100 + int(number[1:3])
    value =  int(number)
elif len(number) == 2:
    number = number[0]
    value = (9 + int(number))%12 
else:
    value = (9 + int(number))%12 

print(str(value))