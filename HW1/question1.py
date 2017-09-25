import numpy as np 
sent = ['she', 'sells', 'sea', 'shells', 'by', 'the', 'sea', 'shore']

#for part 1: printing all words beginnign with 'sh'
print 'Words starting with "sh" are:'
for word in sent:
	if str(word).startswith('sh'):
		print word

print '\n'

#for part2: printing all words longer than four characters
print 'Words longer than four characters are:'
for word in sent:
	if len(word)>4:
		print word