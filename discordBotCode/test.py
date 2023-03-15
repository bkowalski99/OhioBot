import re

text = "Let's play at 1 EST"
text = text.lower()
text = text.replace(":", "")
match = re.search(r'\d+ est', text)
number = match.group(0)[0:-4]
if len(number) == 4:
    value = str(((9 + int(number[0:2]))%12))+":" + (number[2:4]) 
elif len(number) == 3:
    value = str(((9 + int(number[0:1]))%12))+":" + (number[1:3])
elif len(number) == 2:
    value = str((9 + int(number))%12)+ ":00"
else:
    value = str((9 + int(number)))+ ":00"  


print(value)