class Vacuum:
	def __init__(self, locationSquare, isStupid):
		self.locationSquare = locationSquare
		self.isStupid = isStupid

	def verifiedStupid(self, squareA, squareB, graphic):
		self.cleanedSquare(self.locationSquare)
		graphic.changeImage(self.locationSquare.name,0)
		self.locationSquare = squareB if squareA == self.locationSquare else squareA
		graphic.changeImage(self.locationSquare.name,2)
		print("moving to "+self.locationSquare.name)
	
	def verifiedIntelligence(self, squareA, squareB, graphic):
		if not self.locationSquare.isCleaned:
			self.cleanedSquare(self.locationSquare)
			graphic.changeImage(self.locationSquare.name,2)
		other_square = squareA if self.locationSquare == squareB else squareB
		if not other_square.isCleaned:
			graphic.changeImage(self.locationSquare.name,0)
			self.locationSquare = other_square
			graphic.changeImage(self.locationSquare.name,2)
			print("moving to "+self.locationSquare.name)

	def cleanedSquare(self, squareToClean):
		print('cleaning '+squareToClean.name)
		squareToClean.isCleaned = True