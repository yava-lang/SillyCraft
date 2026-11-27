import os
# import winsound
import time
import random

# Get AppData path and create/copy folders
appdata_path = os.getenv('APPDATA')
myapp_path = os.path.join(appdata_path, 'sillycraft')
# Create folder if it doesn't exist
os.makedirs(myapp_path, exist_ok=True)

#То ли тюнебл переменные, то ли что-то другое, хз
h, w = 100, 100 # h = x, w = y
debug, slowmode = False, False
materialtiles = ['s', 'wd', 't', '`']
setpieceblockingtiles = ['s', 'w', 'wd']

#Константы
s = h*w

#Пустышки
ch1, cw1 = 0, 0
ch2, cw2 = 0, 0
i3,i4,i5,i6 = 0, 0, 0, 0
tilecolortext = ''
CurrentWorld = ''
generated = 0
blocked = True
forced = False
dontactfor = 0

#Functions
def savethedata():
	with open(f'{myapp_path}/{save}/Overworld.txt', 'w+') as Overworld_savedata:
		Overworld_savedata.write(str(Overworld).replace("[[", '').replace("]]", '').replace("'", ''))

	with open(f'{myapp_path}/{save}/char.txt', 'w+') as char_savedata:
		char_savedata.writelines([
			f'{char[0]} {char[1]}\n',
			f'{seed}']
			)
	print(f'{char[0]} {char[1]}')
def worldgen_Overworld():
	global Overworld; global char
	Overworld = [['d' for x in range(w)] for y in range(h)]
	char = [random.randint(1,h), random.randint(1,w)]
	while Overworld[char[0]-1][char[1]-1] in materialtiles:
		char = [random.randint(1,h), random.randint(1,w)]
	worldgen_grass(Overworld)
	worldgen_cleandirt(Overworld)
	worldgen_voidborders(Overworld)
	worldgen_lilbitstone(Overworld)
	worldgen_trees(Overworld)
	worldgen_setpieces(Overworld)
def worldgen_grass(World):
	print('генерация травы...')
	for _ in range(s//3*2):
		(World)[random.randint(0,h-1)][random.randint(0,w-1)] = "gs"
	for i2 in range(w-1):
		for i1 in range(h-1):
			if i1 < h: i3 = i1 + 1
			else: i3 = i1 - 1
			if i2 < w: i4 = i2 + 1
			else: i4 = i2 - 1
			if World[i3][i4] == "gs": (World)[i1][i2] = "gs"
			if World[i3][i2] == "gs": (World)[i1][i2] = "gs"
	for i2 in range(w-1):
		for i1 in range(h-1):
			if i1 < h: i3 = i1 + 1
			else: i3 = i1 - 1
			if i2 < w: i4 = i2 + 1
			else: i4 = i2 - 1
			if World[i3][i4] == "gs": (World)[i1][i2] = "g"
			if World[i3][i2] == "gs": (World)[i1][i2] = "g"
			if World[i1][i2] == "gs": (World)[i1][i2] = "g"
def worldgen_cleandirt(World):
	print('уборка лишней земли...')
	for i2 in range(w-1):
		for i1 in range(h-1):
			if i1 < h: i3 = i1 + 1
			else: i3 = i1
			if i1 > 0: i4 = i1 - 1
			else: i4 = i1
			if World[i3][i2] == "g" and World[i4][i2] == "g" and random.randint(1,2) == 1: World[i1][i2] = "g"
def worldgen_voidborders(World):
	print('превращение земли на краях мира в камень')
	for i2 in range(w):
		for i1 in range(h):
			if i1 < 2 or i2 < 2 or i1 >= h-2 or i2 >= w-2:
				if World[i1][i2] == "d": World[i1][i2] = "`"
			if i1 == 0 or i2 == 0:
				if random.randint(1, 2) == 1:
					World[i1][i2] = "`"
			if i1 == 1:
				if random.randint(1, 2) == 1:
					if World[i1-1][i2] == "`": World[i1][i2] = "`"
			elif i2 == 1:
				if random.randint(1, 2) == 1:
					if World[i1][i2-1] == "`": World[i1][i2] = "`"
			elif i2 == w-2:
				if random.randint(1, 2) == 1:
					if World[i1][i2+1] == "`": World[i1][i2] = "`"
def worldgen_lilbitstone(World):
	print('генерация камней...')
	for _ in range(s//1000*1):
		(World)[random.randint(0,h-1)][random.randint(0,w-1)] = "d"

def worldgen_trees(World):
	print('генерация деревьев...')
	for _ in range(s//10000*1):
		treespawnchance = random.randint(1,10)
		tg1 = random.randint(0,h-50)
		tg2 = random.randint(0,w-50)
		for i2 in range(50):
			for i1 in range(50):
				if not random.randint(1,1000) > treespawnchance:
					World[tg1+i2-1][tg2+i1-1] = "t"
					treespawnchance = random.randint(1,10)
				elif treespawnchance > 3: treespawnchance += random.randint(-3,3)
				else: treespawnchance = 5
def worldgen_setpieces(World):
	print('Генерация структур...')
	worldgen_setpiece_1(World, 10, False)
	worldgen_setpiece_2(World, 3, False)
	worldgen_setpiece_3(World, 5, False)
	worldgen_setpiece_3(World, 1, False)
def woldgen_place_setpieces(World, needed, forced, setpiece):
	generated = 0
	while generated < needed:
		blocked = True
		for _ in range(1000):
			blocked = False
			#spg = setpiece_generator
			spg1 = random.randint(40,h-len(setpiece[0]))
			spg2 = random.randint(20,w-len(setpiece))
			for i2 in range(spg1, spg1+len(setpiece[0])):
				for i1 in range(spg2, spg2+len(setpiece)):
					if World[i2][i1] in setpieceblockingtiles: blocked = True
			if not blocked: break
		if not blocked or forced:
			for i1 in range(len(setpiece)):
				for i2 in range(len(setpiece[i1])):
					if not (setpiece[i1][i2] == ' '): World[spg1+i2-1][spg2+i1-1] = setpiece[i1][i2]
		generated += 1
def worldgen_setpiece_1(World, needed, forced):
	setpiece = [[' ', ' ', 'w', 'w', 'w', ' ', ' '],
			 	[' ', 'w', 'wd','wd','wd','w', ' '],
				['w', 'wd','wd','wd','wd','wd','w'],
				['w', 'wd','wd','wd','wd','wd','w'],
				['w', 'wd','wd','wd','wd','wd','w'],
				[' ', 'w', 'wd','wd','wd','w', ' '],
				[' ', ' ', 'w', 'w', 'w', ' ', ' ']]
	woldgen_place_setpieces(World, needed, forced, setpiece)
def worldgen_setpiece_2(World, needed, forced):
	setpiece = [[' ', ' ', 'd', 'd', 'd', ' ', ' '],
			 	[' ', 'd', 's', 's', 's', 'd', ' '],
				['d', 's', 's', 's', 's', 's', 'd'],
				['d', 's', 's', 's', 's', 's', 'd'],
				['d', 's', 's', 's', 's', 's', 'd'],
				[' ', 'd', 's', 's', 's', 'd', ' '],
				[' ', ' ', 'd', 'd', 'd', ' ', ' ']]
	woldgen_place_setpieces(World, needed, forced, setpiece)
def worldgen_setpiece_3(World, needed, forced):
	setpiece = [[' ', ' ', 'd', 'd', 'd', ' ', ' '],
			 	[' ', 'd', 'd', 'd', 'd', 'd', ' '],
				['d', 'd', 'd', 'd', 'd', 'd', 'd'],
				['d', 'd', 'd', 'd', 'd', 'd', 'd'],
				['d', 'd', 'd', 'd', 'd', 'd', 'd'],
				[' ', 'd', 'd', 'd', 'd', 'd', ' '],
				[' ', ' ', 'd', 'd', 'd', ' ', ' ']]
	woldgen_place_setpieces(World, needed, forced, setpiece)
def worldgen_setpiece_4(World, needed, forced):
	setpiece = [['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],
			 	['s', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd'],
				['s', 'd', 'd', 'd', 'd', 's', 's', 's', 's', 's'],
				['s', 'd', 'd', 'd', 'd', 's', 'd', 'd', 'd', 's'],
				['s', 'd', 'd', 'd', 'd', 's', 'd', 'd', 'd', 's'],
				['s', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 's'],
				['s', 's', 's', 's', 's', 's', 's', 's', 's', 's']]
	woldgen_place_setpieces(World, needed, forced, setpiece)

# GAME START
save = int(input('Выберите сохранение: '))
#save = 463
if os.path.exists(f'{myapp_path}/{save}'):
	Overworld_savedata = open(f'{myapp_path}/{save}/Overworld.txt', 'r')
	global Overworld; global char; global seed
	Overworld = []
	# Overworld = [line.split() for line in Overworld_savedata]
	# Overworld = str(Overworld_savedata.readline()).replace('], [', '\n')
	Overworldloading = str(Overworld_savedata.readline()).split('], [')
	for i1 in range(len(Overworldloading)):
		Overworld.append(Overworldloading[i1].split(', '))
	with open(f'{myapp_path}/{save}/char.txt', 'r') as char_savedata:
		char = list(map(int, char_savedata.readline().replace("\n", "").split(' ')))
		seed = char_savedata.readline()
else:
	while True:
		allow = False
		seed = input('Выберите сид мира (x для случайного): ')
		if seed == 'x':
			seed = random.randint(0, 999999)
			allow = True
		else:
			try:
				seed = int(seed)
				if seed >= 0 and seed < 1000000: allow = True
				else: print('Ошибка: Сид мира не входит в диапазон >=0 и < 999999')
			except: print('Ошибка: Сид мира не является целым числом (int)')
		if allow:
			random.seed(seed)
			break

	os.makedirs(f'{myapp_path}/{save}/')

	worldgen_Overworld()
	savethedata()

for _ in range(h):
	if ch2 < 60: ch2 += 1
for _ in range(w):
	if cw2 < 26: cw2 += 1
#оптимальное разрешение экрана: 60, 27
while ch2 < (char[0]+30) and ch2 < h:
		ch1 += 1
		ch2 += 1
while cw2 < (char[1]+13) and cw2 < w:
		cw1 += 1
		cw2 += 1

CurrentWorld = Overworld
# winsound.PlaySound('Jungle.wav', winsound.SND_LOOP | winsound.SND_ASYNC)




#Выбор цвета тайла
def tilecolor(forchar):
	#выбор цвета и принт буквы в зависимости от тайла
	if Overworld[i1][i2] == 'd': tilecolortext = '\033[41m'+'d' # dirt
	elif Overworld[i1][i2] == 'g': tilecolortext = '\033[42m'+'g' # grass
	elif Overworld[i1][i2] == 'gs': tilecolortext = '\033[42m'+'g' # grass spawner
	elif Overworld[i1][i2] == 's': tilecolortext = '\033[37m'+'s' # stone
	elif Overworld[i1][i2] == 'w': tilecolortext = '\033[44m'+'w' # water
	elif Overworld[i1][i2] == 'wd': tilecolortext = '\033[44m'+'w' # water deep
	elif Overworld[i1][i2] == 'p': tilecolortext = '\033[40m'+'\033[33m'+'p' # fg planks
	elif Overworld[i1][i2] == 't': tilecolortext = '\033[40m'+'\033[33m'+'t' # tree
	elif Overworld[i1][i2] == '`': tilecolortext = ' ' # void
	elif (Overworld[i1][i2])[:1] == 'tp': tilecolortext = '\033[35m'+'w' # teleporter - wormhole
	else: tilecolortext = '\033[47m'+'-' #буква, которая появляется если тайл не является обозначенной выше буквой, нужен чтобы не крашилось при отображении не обозначенного тайла
	#принтим ли букву? (если на тайле перс, то нет, ведь там перс)
	if forchar: return(tilecolortext[:-1])
	else: return(tilecolortext)

while True:
	os.system('cls' if os.name == 'nt' else 'clear')

	#Дебаг
	if debug:
		print(f'DEBUG INFO: x{char[0]} y{char[1]} cw1_{cw1} cw2_{cw2} ch1_{ch1} ch2_{ch2} m_{Overworld[char[0]-1][char[1]-1]} s_{seed}')
	else:
		print('')

	#Дисплей
	print('\033[0m'+'', end='') #Бесполезная строчка?? Не знаю, лень проверять
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
			elif not (Overworld[i1][i2][0] == Overworld[i3][i2][0]): print('\033[0m'+' ', end='')
			#иначе пробел с тем же цветом
			else: print(' ', end='')
		#переход на новую строчку после каждой строчки гориз тайлов
		print('\033[0m'+'\n', end='')
		#пашалковый режим когда каждая строчка пишется с задержкой
		if slowmode: time.sleep(0.05)
	#обнуление цвета для ввода
	print('\033[0m'+'', end='')

	#Действия
	if dontactfor > 0:
		dontactfor -= 1
	else:
		action = input().lower()

	dontactfor_temp = ''
	action_temp = ''
	#несколько действий за раз
	for i in action[::-1]:
		if dontactfor > 0:
			action_temp += i
		else:
			if i not in ['*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
				break
			if i != '*':
				dontactfor_temp += i
			else:
				try:
					dontactfor = int(dontactfor_temp[::-1])
					if dontactfor > 100: dontactfor = 100
				except:
					input('somethin broke when trying to multiply action')
	if action_temp != '': action = action_temp
	if 'сво' in action and not debug: debug = True
	elif 'сво' in action and debug: debug = False

	if 'квинка' in action and not slowmode: slowmode = True
	elif 'квинка' in action and slowmode: slowmode = False

	if 'save' in action or 'ыфму' in action:
		with open(f'{myapp_path}/{save}/char.txt', 'w+') as char_savedata: char_savedata.write(f'{char[0]} {char[1]}')

	if not action in ['квинка', 'сво', 'ыфму', 'save']:
		if 'w' in action and char[1] > 1 and not CurrentWorld[char[0]-1][char[1]-2] in materialtiles: char[1] -= 1
		elif 'ц' in action and char[1] > 1 and not CurrentWorld[char[0]-1][char[1]-2] in materialtiles: char[1] -= 1

		if 'a' in action and char[0] > 1 and not CurrentWorld[char[0]-2][char[1]-1] in materialtiles: char[0] -= 1
		elif 'ф' in action and char[0] > 1 and not CurrentWorld[char[0]-2][char[1]-1] in materialtiles: char[0] -= 1

		if 's' in action and char[1] < w and not CurrentWorld[char[0]-1][char[1]] in materialtiles: char[1] += 1
		elif 'ы' in action and char[1] < w and not CurrentWorld[char[0]-1][char[1]] in materialtiles: char[1] += 1

		if 'd' in action and char[0] < h and not CurrentWorld[char[0]][char[1]-1] in materialtiles: char[0] += 1
		elif 'в' in action and char[0] < h and not CurrentWorld[char[0]][char[1]-1] in materialtiles: char[0] += 1