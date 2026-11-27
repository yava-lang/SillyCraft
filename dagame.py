import os

h, w = 59, 27
Matrix = [['# ' for x in range(w)] for y in range(h)]
char = [5, 2]
debug = False
#каким-то образом потом оно поменялось и w стало y, а h стало x

while True:
	os.system('cls' if os.name == 'nt' else 'clear')

	#Дебаг
	if debug:
		print(f'DEBUG INFO: x={char[0]} y={char[1]}')
	else:
		print('')

	#Дисплей
	for i2 in range(w):
		for i1 in range(h):
			if [char[0]-1, char[1]-1] == [i1, i2]: print('\033[47m'+(Matrix[i1][i2])[0]+'\033[0m'+' ', end='')
			else: print(Matrix[i1][i2], end='')
		print('\n', end='')

	#Действия
	action = input()
	if 'сво' in action and debug: debug = False
	if 'сво' in action and not debug: debug = True
	if ('w' or 'ц') in action and char[1] > 1: char[1] -= 1
	if 's' in action and char[1] < w: char[1] += 1
	if 'a' in action and char[0] > 1: char[0] -= 1
	if 'd' in action and char[0] < h: char[0] += 1
