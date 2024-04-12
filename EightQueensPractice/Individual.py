import random
from colorama import Fore, Back, Style
class Individual:
	def __init__(self, id):
		self.gens = []
		self.aptitude = 0
		self.id = id
		self.randomPopulation()
	
	def randomPopulation(self):	
		for i in range(8):
			self.gens.append(random.randint(0,7))

	def calculateAptitude(self):
		crashes = 0
		for i in range(8):
			actual = self.gens[i]
			for j in range(i+1,8):
				next = self.gens[j]
				difference = j - i
				min_next = next - difference
				max_next = next + difference
				crashes += 1 if actual == next else 1 if actual == min_next else 1 if actual == max_next else 0
		self.aptitude = 28 - crashes
		"""print(f"Pares sin choques {self.aptitude}!")"""
	def printBoard(self):
		#print('\x1B[2;0H')
		print(f"{Fore.GREEN}Aptitude {self.aptitude}{Style.RESET_ALL}", end="\n")
		isWhite = True
		for i in range(8):
			for j in range(8):
				if isWhite:
					print(Back.WHITE+ '       '+ Style.RESET_ALL,end ="")
				else :
					print(Back.BLACK+ '       '+ Style.RESET_ALL,end ="")
				isWhite = not isWhite
			print('', end='\n')
			for j in range(8):
				if isWhite:
					print(Back.WHITE+ '  '+ ('♛' if self.gens[j]== i else ' ') + '    '+ Style.RESET_ALL,end ="")
				else:
					print(Back.BLACK+ '  '+ ('♛' if self.gens[j]== i else ' ') + '    '+ Style.RESET_ALL,end ="")
				isWhite = not isWhite
			print('', end='\n')
			for j in range(8):
				if isWhite:
					print(Back.WHITE+ '       '+ Style.RESET_ALL,end ="")
				else :
					print(Back.BLACK+ '       '+ Style.RESET_ALL,end ="")
				isWhite = not isWhite
			print('', end='\n')
			isWhite = not isWhite
		print(self.gens)
		print('--------------------------------------------------------------')