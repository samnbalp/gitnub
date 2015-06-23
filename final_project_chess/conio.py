from __future__ import print_function
import os
import colorama
from colorama import Fore, Back, Style
import msvcrt
import struct
import random

# 請先安裝colorama => pip install -U colorama

__keyBase__ = b''
__chess__x__ = 1
__chess__y__ = 1

# constant value
KEY_ARROW = "KEY_ARROW"
KEY_UP = "KEY_UP"
KEY_DOWN = "KEY_DOWN"
KEY_LEFT = "KEY_LEFT"
KEY_RIGHT = "KEY_RIGHT"

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

Enter = '\r'
BackSpace = '\x08'
NonASCII = '\xff'

ACTIVE = (Fore.WHITE, Style.NORMAL, Back.YELLOW, Style.BRIGHT)
INACTIVE = (Fore.BLACK, Style.NORMAL, Back.WHITE, Style.NORMAL)

# format : code : symbol level group
CHESSMAN = {
	1 : (u'將', 10, True),
	2 : (u'士', 9, True),
	3 : (u'士', 9, True),
	4 : (u'象', 8, True),
	5 : (u'象', 8, True),
	6 : (u'車', 7, True),
	7 : (u'車', 7, True),
	8 : (u'馬', 6, True),
	9 : (u'馬', 6, True),
	10 : (u'包', 5, True),
	11 : (u'包', 5, True),
	12 : (u'卒', 4, True),
	13 : (u'卒', 4, True),
	14 : (u'卒', 4, True),
	15 : (u'卒', 4, True),
	16 : (u'卒', 4, True),
	17 : (u'帥', 10, False),
	18 : (u'仕', 9, False),
	19 : (u'仕', 9, False),
	20 : (u'相', 8, False),
	21 : (u'相', 8, False),
	22 : (u'俥', 7, False),
	23 : (u'俥', 7, False),
	24 : (u'傌', 6, False),
	25 : (u'傌', 6, False),
	26 : (u'炮', 5, False),
	27 : (u'炮', 5, False),
	28 : (u'兵', 4, False),
	29 : (u'兵', 4, False),
	30 : (u'兵', 4, False),
	31 : (u'兵', 4, False),
	32 : (u'兵', 4, False)
}

def putch(c) :
	if len(c) <= 5 and ord(c) >= 0 and ord(c) <= 255 :
		msvcrt.putch(struct.pack('!B', ord(c)))
		
def putstr(string) :
	for c in string :
		putch(c)

def getch() :
	return msvcrt.getch()
	
def kbhit() :
	return msvcrt.kbhit()
	

def getKey() : # python windows function call
	global __keyBase__
	kbValue = struct.pack('!B', ord(NonASCII))
	if kbhit() :
		kbValue = getch()
	if kbValue == b'\xe0' :
		__keyBase__ = kbValue
		# print('arrow key base')
		return KEY_ARROW
	else :
		if __keyBase__ == b'\xe0' :
			if kbValue == b'H' : # up
				# print('up')
				__keyBase__ = b''
				return KEY_UP
			elif kbValue == b'P' : # down
				# print('down')
				__keyBase__ = b''
				return KEY_DOWN
			elif kbValue == b'K' : # left
				# print('left')
				__keyBase__ = b''
				return KEY_LEFT
			elif kbValue == b'M' : # right
				# print('right')
				__keyBase__ = b''
				return KEY_RIGHT
			else :
				# print(kbValue)
				__keyBase__ = b''
		elif __keyBase__ == b'\x00' :
			pass
		else :
			# print(kbValue, end = '')
			# print(chr(struct.unpack("!B", kbValue)[0]))
			return chr(struct.unpack("!B", kbValue)[0])

def initscr() :
	colorama.init()
			
def setFGColor(color = Fore.WHITE, style = Style.NORMAL) :
	if color in FORES and style in STYLES:
		print("%s%s" % (color, style), end='')
	else :
		print('Error Foreground color')
		
def setBGColor(color = Back.BLACK, style = Style.NORMAL) :
	if color in BACKS and style in STYLES:
		print("%s%s" % (color, style), end='')
	else :
		print('Error Background color')
		
def gotoxy(x, y) :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	print('\x1b[%d;%dH' % (y, x), end='')
	
def clsscr() :
	os.system("cls")

def drawText(x, y, string) :
	gotoxy(x, y)
	putstr(string)
	
def box(x = 1, y = 1, width = 39, height = 24) :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	gotoxy(x, y)
	putstr(' '*width*2)
	for i in range(height) :
		gotoxy(x, y + i)
		putstr('  ')
		gotoxy(x + width*2 - 1, y + i)
		putstr('  ')
	gotoxy(x, y + height)
	putstr(' '*(width*2 + 1))
	
def chess(x = 1, y = 1) :
	global __chess__x__
	global __chess__y__
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	__chess__x__ = x
	__chess__y__ = y
	wall = (0, 2, 4, 6, 8)
	for j in range(9) :
		if j in wall :
			inactive(__chess__x__, j + __chess__y__, '-'*25)
			continue
		for i in range(25) :
			if (i - 1) % 3 == 0 :
				setFGColor(ACTIVE[0], ACTIVE[1])
				setBGColor(ACTIVE[2], ACTIVE[3])
				gotoxy(i + __chess__x__, j + __chess__y__)
				print(u'  ', end='')
				setFGColor()
				setBGColor()
			elif i % 3 == 0 :
				inactive(i + __chess__x__, j + __chess__y__, '|')
				
def chessSet(x = 1, y = 1, string = u'', ON = False) :
	posY = [2, 4, 6, 8]
	posX = [2, 5, 8, 11, 14, 17, 20, 23]
	if x > 0 and x <= 8 and y > 0 and y <= 4 :
		if ON :
			setFGColor(ACTIVE[0], ACTIVE[1])
			setBGColor(ACTIVE[2], ACTIVE[3])
		else :
			setFGColor(INACTIVE[0], INACTIVE[1])
			setBGColor(INACTIVE[2], INACTIVE[3])
		gotoxy(__chess__x__ - 1 + posX[x - 1], __chess__y__ - 1  + posY[y - 1])
		print(string, end='')
		setFGColor()
		setBGColor()

class Chess :
	def __init__(self) :
		self.C = dict()
		self.pos = (1, 1)
		self.chessman = dict()
		for j in range(1, 5) :
			for i in range(1, 9) :
				self.C[(i, j)] = []
	def rand(self) :
		for cmk in list(CHESSMAN.keys()) :
			self.chessman[cmk] = [0, 0, False, False] # 位置 明/暗 死亡/生存
		shuffle = [i for i in range(1, 33)]
	def move(self, Op) :
		if Op == KEY_UP :
			pass
		if Op == KEY_DOWN :
			pass
		if Op == KEY_LEFT :
			pass
		if Op == KEY_RIGHT :
			pass
		if Op == Enter :
			pass
	
def active(x, y, string) : # set some label as active color# 
	setFGColor(ACTIVE[0], ACTIVE[1])
	setBGColor(ACTIVE[2], ACTIVE[3])
	gotoxy(x, y)
	putstr(string)
	setFGColor()
	setBGColor()
	
def inactive(x, y, string) : # set some label as inactive color
	setFGColor(INACTIVE[0], INACTIVE[1])
	setBGColor(INACTIVE[2], INACTIVE[3])
	gotoxy(x, y)
	putstr(string)
	setFGColor()
	setBGColor()
	
# ui item : name U TAG D TAG L TAG R TAG ETR FUNC 

class uiItem :
	def __init__(self, name, x = 1, y = 1) :
		self.name = name
		self.U = ""
		self.D = ""
		self.L = ""
		self.R = ""
		self.F = ""
		self.x = x
		self.y = y
	def setName(self, name) :
		self.name = name
		return self.name
	def setR(self, tag) :
		self.R = tag
	def setL(self, tag) :
		self.L = tag
	def setU(self, tag) :
		self.U = tag
	def setD(self, tag) :
		self.D = tag
	def setF(self, F) :
		self.F = F
	def setxy(self, x, y) :
		self.x = x
		self.y = y
	def getName(self) :
		return self.name
	def getU(self) :
		return self.U
	def getD(self) :
		return self.D
	def getL(self) :
		return self.L
	def getR(self) :
		return self.R
	def getxy(self) :
		return (self.x, self.y)

# ui page
		
class uiPage :
	def __init__(self, pageName) :
		self.pageName = pageName
		self.O = dict()
		self.curItem = ""
	def addItem(self, Item) :
		if not Item.getName() in list(self.O.keys()) : 
			self.curItem = Item.getName()
			self.O[Item.getName()] = Item
	def delItem(self, itemName) :
		if itemName in list(self.O.keys()) :
			del self.O[itemName]
	def drawUI(self) :
		xy = (0, 0)
		itemName = ""
		for itemName in list(self.O.keys()) :
			xy = self.O[itemName].getxy()
			inactive(xy[0], xy[1], itemName)
		xy = self.O[self.curItem].getxy()
		itemName = self.O[self.curItem].getName()
		active(xy[0], xy[1], itemName)
	def current(self) :
		return (self.pageName, self.curItem)
	def move(self, Op) :
		nextItem = ""
		xy = (0, 0)
		itemName = ""
		if Op == KEY_UP :
			nextItem = self.O[self.curItem].getU()
		elif Op == KEY_DOWN :
			nextItem = self.O[self.curItem].getD()
		elif Op == KEY_RIGHT :
			nextItem = self.O[self.curItem].getR()
		elif Op == KEY_LEFT :
			nextItem = self.O[self.curItem].getL()
		elif Op == Enter :
			print(self.O[self.curItem])
			return self.O[self.curItem]
		if nextItem in list(self.O.keys()) :
			xy = self.O[self.curItem].getxy()
			itemName = self.O[self.curItem].getName()
			inactive(xy[0], xy[1], itemName)
			self.curItem = nextItem
			xy = self.O[nextItem].getxy()
			itemName = self.O[nextItem].getName()
			active(xy[0], xy[1], itemName)

if __name__ == "__main__" :
	initscr()
	"""
	clsscr()
	setBGColor(Back.YELLOW, Style.NORMAL)
	box()
	drawText(5, 3, 'A')
	drawText(7, 3, 'A')
	setBGColor()
	drawText(9, 3, 'A')
	"""
	
	# active(1, 2, "apple")
	# inactive(1, 3, "apple2")
	
	chess(10, 5)
	chessSet(5, 1, u'士')
	"""
	item0 = uiItem('apple0', 1, 1)
	item0.setD('apple1')
	item0.setR('apple2')
	item1 = uiItem('apple1', 1, 3)
	item1.setU('apple0')
	item2 = uiItem('apple2', 6, 1)
	item2.setL('apple0')
	page0 = uiPage('example')
	page0.addItem(item0)
	page0.addItem(item1)
	page0.addItem(item2)
	page0.drawUI()
	"""
	while True :
	#	value = getKey()
	#	page0.move(value)
		pass
	"""
	gotoxy(16, 5)
	input()
	while (True) :
		if kbhit() :
			clsscr()
			setFGColor(Fore.YELLOW, Style.NORMAL)
			gotoxy(16, 5)
			# print(getKey(), end='')
			value = getKey()
			if value == '\r' or value == '\n' :
				print('Enter', end = '')
			elif value == '\x08' :
				print('BackSpace', end = '')
			elif value == KEY_DOWN :
				print('KEY DOWN', end = '')
	"""