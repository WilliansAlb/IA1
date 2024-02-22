import random
class Vacuum:
	def __init__(self, locationSquare, isStupid):
		self.locationSquare = locationSquare
		self.isStupid = isStupid

	def verifiedStupid(self, squareA, squareB, graphic):
		action = random.randint(1, 3)
		if action == 1:
			self.clean(self.locationSquare)
		elif action == 2:
			self.move(squareA=squareA,squareB=squareB,graphic=graphic)
		else:
			print("doing nothing")
	
	def verifiedIntelligence(self, squareA, squareB, graphic):
		if not self.locationSquare.isCleaned:
			self.clean(self.locationSquare)
			graphic.changeImage(self.locationSquare.name,2)
		self.move(squareA,squareB,graphic)
	
	def move(self, squareA, squareB, graphic):
		other_square = squareA if self.locationSquare == squareB else squareB
		if (self.locationSquare.isCleaned):
			graphic.changeImage(self.locationSquare.name,0)
		else:
			graphic.changeImage(self.locationSquare.name,1)
		self.locationSquare = other_square
		graphic.changeImage(self.locationSquare.name,2)
		print("moving to "+self.locationSquare.name)


	def clean(self, squareToClean):
		print('cleaning '+squareToClean.name)
		squareToClean.isCleaned = True