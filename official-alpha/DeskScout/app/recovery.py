import urllib,os
os.chdir(os.path.dirname(__file__))
class Pages:
	def main():
		
		
		while True:
			os.system("CLS")
			print("Main menu")
			print("1-System Check")
			print("2-Download latest version from internet")
			print("3-Reinitialize Settings")
			print("4-Update from file")
			print("5-Fix Settings")
			print("Or type x to exit")
			ans = input(">")
			if ans == "x":
				exit()
			elif ans == "1":
				#Check application integrity
				try:
					compile(open("DeskScout.pyw").read(),'launcher','exec')
					print("Launcher OK")
				except Exception as e:
					print("Issue with DeskScout Launcher",e)
				try:
					compile(open("DeskScoutApp.py").read(),'app','exec')
					print("App OK")
				except Exception as e:
					print("Issue with DeskScout App",e)
				try:
					compile(open("DeskScoutService.py").read(),'service','exec')
					print("Service OK")
				except Exception as e:
					print("Issue with DeskScout Service",e)
				try:
					compile(open("updater.py").read(),'updater','exec')
					print("Updater OK")
				except Exception as e:
					print("Issue with DeskScout Updater",e)
					print("A complete re-install is reccomended")
				input("Press enter to continue")
			elif ans == "4":
				from tkinter import filedialog
				print("Select a path to update system")
				path = filedialog.askopenfilename(defaultextension=".zip")
				if path:
					print("Attempting to update")
					






Pages.main()