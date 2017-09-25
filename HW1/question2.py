import numpy as np 

string1 = "Wild brown trout are elusive"

#implementing using split function - creates required list called 'words':
words = string1.split()
print words

#implementing without split() function:
list1=[]
current_word = ""
for character in string1:
	if character == ' ':
		list1.append(current_word)
		current_word = ""
	else:
		current_word += character

if current_word:
	list1.append(current_word)

print list1