import msvcrt,_thread,os,sys,time
key = []
run = True


class blocks:
	top_left = u'\u2554'   # ╔
	top_right = '\u2557'  # ╗
	bottom_left = '\u255A'  # ╚
	bottom_right = '\u255D'  # ╝
	horizontal = '\u2550'  # ═
	vertical = '\u2551'    # ║
def move(x,y):
	print(f"\u001b[{y};{x}H",end="")
def keythread():
	global key
	while run:
		x = msvcrt.getch()
		if x == b'\xe0':
			#Escape
			key.append(x + msvcrt.getch())
			#print(key)
		else:
			key.append(x)
class Widget:
	def __init__(self,screen):
		self.screen = screen
	def foreground(self):
		pass
	def background(self):
		pass
	def tick(self,state):
		pass
class Screen:
	def __init__(self):
		self.w,self.h = os.get_terminal_size()
		self.widgets = []
		self.widget = Widget
	def setCurrentWidget(self,w):
		self.widget = w
		self.widget.foreground()
	def addWidget(self,w):
		self.widgets.append(w)
		w.background()
	def removeWidget(self,w):
		w.background()
		self.widgets.remove(w)
		if self.widget == w:
			self.widget = None
	def close(self):
		global run
		run = False
		key.clear()
	def open(self):
		global run
		run = True
		_thread.start_new_thread(keythread,())
	def clear(self):
		os.system("CLS")
	def main(self):
		while True:
			for i in self.widgets:
				self.widget.tick(0)
			self.widget.tick(1)
	def backall(self):
		for i in self.widgets:
			i.tick(0)
		self.widget.tick(0)
		
	def tick(self):
		self.w,self.h = os.get_terminal_size()

		for i in self.widgets:
			self.widget.tick(0)
		self.widget.tick(1)
class Window():
	def __init__(self,screen:Screen,x=0,y=0,w=None,h=None,title="Untitled Window"):
		self.screen = screen
		self.title = title
		self.status = ""
		self.fgcolor = "\u001b[44m\u001b[37m"
		self.bgcolor = "\u001b[240m"

		self.x = x
		self.y = y
		self.w = w if w else self.screen.w
		self.h = h if h else self.screen.h

		self.width = self.screen
	def foreground(self):
		pass
	def background(self):
		pass
	def clear(self):
		gc = self.fgcolor
		move(self.x,self.y)
		for i in range(self.h+2):
			move(self.x,self.y+i)

			print("\u001b[0m\u001b[2K")

	def tick(self,state):
		if state == 1:
			#Foreground
			move(self.x,self.y)
			print(self.fgcolor,end="")
			print(self.fgcolor+blocks.top_left,end='')
			try:
				print(
					self.title if len(self.title)<self.screen.w-2 else self.title[:self.w-2-len(self.title)],
					end=""
				)
				print(blocks.horizontal*(self.w-len(self.title)-2),end="")
			except:
				print((self.w-2)*blocks.horizontal,end="")
			print(blocks.top_right)
			for i in range(self.h-2):
				print(blocks.vertical,end=(" "*(self.w-2))+blocks.vertical)
			print(self.fgcolor+blocks.bottom_left,end='')
			try:
				print(
					self.status if len(self.status)<self.w-2 else self.title[:self.w-2-len(self.status)],
					end=""
				)
				print(blocks.horizontal*(self.w-len(self.status)-2),end="")
			except:
				print((self.screen.w-2)*blocks.horizontal,end="")
			print(blocks.bottom_right,end='\u001b[0m')
		else:
			print(self.bgcolor,end="")
			print(blocks.top_left,end='')
			try:
				print(
					self.title if len(self.title)<self.screen.w-2 else self.title[:self.w-2-len(self.title)],
					end=""
				)
				print(blocks.horizontal*(self.w-len(self.title)-2),end="")
			except:
				print((self.w-2)*blocks.horizontal,end="")
			print(blocks.top_right)
			for i in range(self.h-2):
				print(blocks.vertical,end=(" "*(self.w-2))+blocks.vertical)
			print(self.bgcolor+blocks.bottom_left,end='')
			try:
				print(
					self.status if len(self.status)<self.w-2 else self.title[:self.w-2-len(self.status)],
					end=""
				)
				print(blocks.horizontal*(self.w-len(self.status)-2),end="")
			except:
				print((self.screen.w-2)*blocks.horizontal,end="")
			print(blocks.bottom_right,end='\u001b[0m')
class Popup:
	def message(title,text,color="\u001b[41m\u001b[37m"):
		screen = Screen()
		c = 1
		lines = [""]
		ml = 0
		for i in text:
			if c > ml:
				ml = c
			if c == screen.w-3:
				lines[-1] += " "
				lines.append("")
				c = 1
			elif i != "\n":
				lines[-1] += i
				c += 1
				
			else:

				lines.append(blocks.vertical)
				c = 1

		text = "\n".join(lines)
		w = ml+2
		h = 3+len(lines)
		x = round(screen.w/2)-round((w+2)/2)
		y = round(screen.h/2)-round((h+2)/2)

		window = Window(screen,0,y,h=h)
		window.status = "Press Enter or Esc to close."
		window.fgcolor = color
		window.tick(1)
		print(color,end="")
		move(x+2,y+1)
		
		print(text)
		move(x+round(w/2),y+h-2)
		print("\u001b[7mOK\u001b[27m")
		while True:
			if key:
				if key[0] in [b'\r',b'\x1b']:
					key.pop(0)
					return
	def option(title,text,options,index=0,color="\u001b[41m\u001b[37m",screen=Screen()):
		c = 1
		lines = [""]
		ml = 0
		for i in text:
			if c > ml:
				ml = c
			if c == screen.w-3:
				lines[-1] += " "
				lines.append("")
				c = 1
			elif i != "\n":
				lines[-1] += i
				c += 1
				
			else:

				lines.append(blocks.vertical)
				c = 1

		text = "\n".join(lines)
		w = ml+2
		h = 3+len(lines)
		x = round(screen.w/2)-round((w+2)/2)
		y = round(screen.h/2)-round((h+2)/2)

		window = Window(screen,0,y,h=h+1)
		window.title = title
		window.status = "Up/Down: Navigate, Enter: Select, Escape: Exit"
		window.fgcolor = color
		window.tick(1)
		print(color,end="")
		move(x+2,y+1)
		
		print(text)
		move(x+round(w/2)-round((len(options[index])+2)/2),y+h-2)

		print(f"\u001b[7m<>{options[index]}\u001b[27m")
		move(x+round(w/2)-round((len(options[index])+2)/2),y+h-1)
		print(color,end="OK\n")
		edit = False
		submit = False
		ot = os.get_terminal_size()
		while True:
			if os.get_terminal_size() != ot:
				screen.clear()
				screen.w,screen.h = os.get_terminal_size()
				screen.backall()
				ot = os.get_terminal_size()
				x = round(screen.w/2)-round((w+2)/2)
				y = round(screen.h/2)-round((h+2)/2)
				window.y = y
				window.tick(1)
				print(color,end="")
				move(x+2,y+1)
				
				print(text)
				if edit:
					print(f"\u001b[48;5;250m\u001b[38;5;255m",end="")
					for i in range(len(options)):
						move(x+round(w/2)-round((len(options[i])+2)/2),y+h-2+i)
						if index == i:
							print(f"\u001b[7m{options[i]}\u001b[27m")
						else:
							print(options[i])
					move(x+round(w/2)-1,y+h-2+i)
					
					print(color,end="OK")
				else:
					window.tick(1)
					print(color,end="")
					move(x+2,y+1)
					
					print(text)
					move(x+round(w/2)-round((len(options[index])+2)/2),y+h-2)
					print(f"\u001b[7m<>{options[index]}\u001b[27m")
					move(x+round(w/2)-round((len(options[index])+2)/2),y+h-1)
					if submit:
						print(f"\u001b[7m"+color,end="OK\u001b[27m\n")
					else:
						print(color,end="OK\n")
			if key:
				#print(key)
				if key[0] == b'\x1b':
					return None
				elif key[0] == b'\xe0H':
					if edit:
						if index > 0:
							index -= 1
						else:
							print("\a",end="",flush=True)
					else:
						submit = False
					#DOWN
					window.tick(1)
					print(color,end="")
					move(x+2,y+1)
					
					print(text)
					if edit:
						print(f"\u001b[48;5;250m\u001b[38;5;255m",end="")
						for i in range(len(options)):
							move(x+round(w/2)-round((len(options[i])+2)/2),y+h-2+i)
							if index == i:
								print(f"\u001b[7m{options[i]}\u001b[27m")
							else:
								print(options[i])
						move(x+round(w/2)-1,y+h-2+i)
						
						print(color,end="OK")
					else:
						window.tick(1)
						print(color,end="")
						move(x+2,y+1)
						
						print(text)
						move(x+round(w/2)-round((len(options[index])+2)/2),y+h-2)
						print(f"\u001b[7m<>{options[index]}\u001b[27m")
						move(x+round(w/2)-round((len(options[index])+2)/2),y+h-1)
						if submit:
							print(f"\u001b[7m"+color,end="OK\u001b[27m\n")
						else:
							print(color,end="OK\n")
					

				elif key[0] == b'\xe0P':
					if edit == False:
						submit = True
					else:
						if index < len(options)-1:
							index += 1
						else:
							print("\a",end="",flush=True)

					#DOWN
					window.tick(1)
					print(color,end="")
					move(x+2,y+1)
					print(text)
					if edit:
						print(f"\u001b[48;5;250m\u001b[38;5;255m",end="")
						for i in range(len(options)):
							move(x+round(w/2)-round((len(options[i])+2)/2),y+h-2+i)
							if index == i:
								print(f"\u001b[7m{options[i]}\u001b[27m")
							else:
								print(options[i])
					else:

						window.tick(1)
						print(color,end="")
						move(x+2,y+1)
						
						print(text)
						move(x+round(w/2)-round((len(options[index])+2)/2),y+h-2)
						print(f"\u001b[7m<>{options[index]}\u001b[27m")
						move(x+round(w/2)-round((len(options[index])+2)/2),y+h-1)
						if submit:
							print(f"\u001b[7m"+color,end="OK\u001b[27m\n")
						else:
							print(color,end="OK\n")
				elif key[0] == b'\r':
					if submit:
						key.pop(0)
						return index
					edit = not edit
					window.clear()
					if edit:
						window.h = h+len(options)
					else:
						window.h = h+1
					
					window.tick(1)
					print(color,end="")
					move(x+2,y+1)
					
					print(text)
					if edit:
						print(f"\u001b[48;5;250m\u001b[38;5;255m",end="")
						for i in range(len(options)):
							move(x+round(w/2)-round((len(options[i])+2)/2),y+h-2+i)
							if index == i:
								print(f"\u001b[7m{options[i]}\u001b[27m")
							else:
								print(options[i])
						move(x+round(w/2)-1,y+h-2+i)
					else:
						window.tick(1)
						print(color,end="")
						move(x+2,y+1)
						
						print(text)
						move(x+round(w/2)-round((len(options[index])+2)/2),y+h-2)
						print(f"\u001b[7m<>{options[index]}\u001b[27m")
						move(x+round(w/2)-round((len(options[index])+2)/2),y+h-1)

						print(color,end="OK\n")
				key.pop(0)
				time.sleep(0.01)
	def input_popup(prompt="Enter text:", input_text="", color="\u001b[41m\u001b[37m", screen=Screen(),selected=None):
		import time
		# Prompt wrapping logic
		c = 1
		lines = [""]
		ml = 0
		for i in prompt:
			if c > ml:
				ml = c
			if c == screen.w - 3:
				lines[-1] += " "
				lines.append(blocks.vertical)
				c = 1
			elif i != "\n":
				lines[-1] += i
				c += 1
			else:
				lines.append(blocks.vertical)
				c = 1

		text = "\n".join(lines)
		w = ml + 2
		h = 3 + len(lines)
		x = round(screen.w / 2) - round((w + 2) / 2)
		y = round(screen.h / 2) - round((h + 2) / 2)
		cursor_pos = len(input_text)
		viewshift = 0

		# Calculated visible width (usable screen width)
		visible_width = screen.w - 4  # accounts for borders

		window = Window(screen, 0, y, h=h)
		window.status = "Press Enter or Esc to close."
		window.fgcolor = color
		window.title = ""
		screen.addWidget(window)
		screen.setCurrentWidget(window)

		def redraw():
			window.tick(1)
			move(2, y + 1)
			print(color, end="")
			print(text)

			move(2, y + 1 + len(lines))

			# Adjust viewshift if needed
			nonlocal viewshift
			if cursor_pos < viewshift:
				viewshift = cursor_pos
			elif cursor_pos >= viewshift + visible_width:
				viewshift = cursor_pos - visible_width + 1

			# Prepare visible portion
			visible_text = input_text[viewshift:viewshift + visible_width]
			padded = visible_text + "_" * (visible_width - len(visible_text))
			print(padded, end="")

			# Move cursor (within bounds)
			cursor_screen_x = 2 + (cursor_pos - viewshift)
			cursor_screen_x = max(2, min(screen.w - 2, cursor_screen_x))
			move(cursor_screen_x, y + 1 +len(lines))
			print(color, end="", flush=True)

		redraw()

		while True:
			global key
			if key:
				k = key.pop(0)
				if k == b'\r':  # Enter
					return input_text
				elif k == b'\x1b':  # Escape
					return None
				elif k == b'\x08':  # Backspace
					if cursor_pos > 0:
						input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
						cursor_pos -= 1
				elif k == b'\xe0K':  # Left arrow
					if cursor_pos > 0:
						cursor_pos -= 1
				elif k == b'\xe0M':  # Right arrow
					if cursor_pos < len(input_text):
						cursor_pos += 1
				elif isinstance(k, bytes) and 32 <= k[0] <= 126:  # Printable
					input_text = input_text[:cursor_pos] + k.decode() + input_text[cursor_pos:]
					cursor_pos += 1
				redraw()
def menu(title,options,color='\u001b[44m\u001b[37m',index=0,hint=None):
	screen = Screen()

	window = Window(screen,0,0,title=title)
	window.fgcolor = color
	if hint:
		window.status = hint
	window.clear()
	window.tick(1)
	vp = 0
	vi = 0
	for i in options[vp:]:
		if vi == screen.h-2:
			break
		else:
			move(2,2+vi)
			if vp+vi == index:
				print('\u001b[7m'+color+i)
			else:
				print('\u001b[0m'+color+i)
		
		vi += 1
	
	for i in range(index-1):
		key.append(b'\xe0P')
	push = 0
	while True:
		vi = 0
		if key != []:
			if key[0] == b'\x1b':
				key.pop(0)
				return None
			elif key[0] == b'\xe0H':
				
				if index > 0:
					index -= 1
					if push == 0 and vp:
						vp -= 1
					else:
						push -= 1
					window.tick(1)
				for i in options[vp:]:
					if vi == screen.h-2:
						break
					else:
						move(2,2+vi)
						if vp+vi == index:
							print('\u001b[7m'+color+i)
						else:
							print('\u001b[0m'+color+i)
					
					vi += 1
				key.pop(0)

			elif key[0] == b'\xe0P':
				if index < len(options)-1:
					index += 1
					if push == screen.h-3:
						vp += 1
					else:
						push += 1
					window.tick(1)

				for i in options[vp:]:
					if vi == screen.h-2:
						break
					else:
						move(2,2+vi)
						if vp+vi == index:
							print('\u001b[7m'+color+i)
						else:
							print('\u001b[0m'+color+i)
					
					
					vi += 1
				print('\u001b[0m'+color,end="",flush=True)
				#move(2,2+vp+push)
				#print(color+'\u001b[7m'+options[index]+'\u001b[0m'+color,end="  "+str(push),flush=True)
				key.pop(0)
			elif key[0] == b'\r':
				screen.clear()
				key.pop(0)
				return index



				
			else:
				key.pop(0)
			

			
	input()