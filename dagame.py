import os
import time
import random

h, w = 1000, 1000
ch1, cw1 = 0, 0
ch2, cw2 = 0, 0
char = [random.randint(0,h),random.randint(0,w)]
for i in range(h):
	if ch2 < 60: ch2 += 1
for i in range(w):
	if cw2 < 26: cw2 += 1
#оптимальное разрешение экрана: 60, 27
while ch2 < (char[0]+30) and ch2 < h:
		ch1 += 1
		ch2 += 1
while cw2 < (char[1]+13) and cw2 < w:
		cw1 += 1
		cw2 += 1
Matrix = [['d' for x in range(w)] for y in range(h)]
debug, slowmode = False, False
i3,i4,i5,i6,tilecolortext = 0,0,0,0,''
#каким-то образом потом оно поменялось и w стало y, а h стало x

for i in range((h+1)*(w+1)//3):
	Matrix[random.randint(0,h-1)][random.randint(0,w-1)] = "gs"
for i in range((h+1)*(w+1)//3):
	Matrix[random.randint(0,h-1)][random.randint(0,w-1)] = "gs"
for i2 in range(w-1):
	for i1 in range(h-1):
		if i1 < h: i3 = i1 + 1
		if i2 < w: i4 = i2 + 1
		if Matrix[i3][i4] == "gs": Matrix[i1][i2] = "g"
		if Matrix[i3][i2] == "gs": Matrix[i1][i2] = "g"
		if Matrix[i1][i2] == "gs": Matrix[i1][i2] = "g"
Matrix[0][0] = "g"



while True:
	os.system('cls' if os.name == 'nt' else 'clear')

	#Дебаг
	if debug:
		print(f'DEBUG INFO: x{char[0]} y{char[1]} cw1_{cw1} cw2_{cw2} ch1_{ch1} ch2_{ch2} m_{Matrix[char[0]-1][char[1]-1]}')
	else:
		print('')

	#Выбор цвета тайла
	def tilecolor(forchar):
		#выбор цвета и принт буквы в зависимости от тайла
		if Matrix[i1][i2] == 'd': tilecolortext = '\033[41m'+'d'
		elif Matrix[i1][i2] == 'g': tilecolortext = '\033[42m'+'g'
		elif Matrix[i1][i2] == 'gs': tilecolortext = '\033[42m'+'g'
		#принтим ли букву? (если на тайле перс, то нет, ведь там перс)
		if forchar: return(tilecolortext[:-1])
		else: return(tilecolortext)

	#Дисплей
	print('\033[0m'+'', end='')
	if char[0] == (ch2-29) and char[0] < (h-29):
		ch1 += 1
		ch2 += 1
	if char[0] == (ch1+29) and char[0] > 29:
		ch1 -= 1
		ch2 -= 1

	if char[1] == (cw2-13) and char[1] < (w-13):
		cw1 += 1
		cw2 += 1
	if char[1] == (cw1+11) and char[1] > 11:
		cw1 -= 1
		cw2 -= 1
	'''if w > 60 and cw1 < (cw2-60): cw1 += 1
	elif w > 60 and cw1 == (cw2-60): break
	elif w > 60 and cw1 > (cw2-60): cw1 -=1'''
	for i2 in range(cw1, cw2):
		for i1 in range(ch1, ch2):
			#если это не последний гориз. тайл: i3 = гориз + 1
			if i1 < h: i3 = i1 + 1
			#если на этом тайле персонаж, то
			if [char[0]-1, char[1]-1] == [i1, i2]:
				#принтим персонажа (белый квадрат малевича)
				print('\033[47m'+'#', end='')
				#используем функцию отрисовки тайла, но без буквы (ибо вместо неё стоит персонаж)
				print(tilecolor(True), end='')
			#если на тайле не персонаж, то юзаем функцию отрисовки тайла
			else: print(tilecolor(False), end='')
			#если это последний гориз. тайл или тайлы разные, то рисуем пустоту
			if i1 == h-1: print('\033[0m'+' ', end='')
			elif not (Matrix[i1][i2] == Matrix[i3][i2]): print('\033[0m'+' ', end='')
			#иначе пробел с тем же цветом
			else: print(' ', end='')
		#переход на новую строчку после каждой строчки гориз тайлов
		print('\n', end='')
		#пашалковый режим когда каждая строчка пишется с задержкой
		if slowmode: time.sleep(0.05)
	#обнуление цвета для ввода
	print('\033[0m'+'', end='')

	#Действия
	action = input()
	if 'сво' in action and not debug: debug = True
	elif 'сво' in action and debug: debug = False

	if 'квинка' in action and not slowmode: slowmode = True
	elif 'квинка' in action and slowmode: slowmode = False

	if 'w' in action and char[1] > 1: char[1] -= 1
	elif 'ц' in action and char[1] > 1: char[1] -= 1

	if 'a' in action and char[0] > 1: char[0] -= 1
	elif 'ф' in action and char[0] > 1: char[0] -= 1

	if 's' in action and char[1] < w: char[1] += 1
	elif 'ы' in action and char[1] < w: char[1] += 1

	if 'd' in action and char[0] < h: char[0] += 1
	elif not 'квинка' in action and not 'сво' in action and 'в' in action and char[0] < h: char[0] += 1