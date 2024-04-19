class Street:
    def __init__(self,x,y,isCross,route,direction):
        self.x = x
        self.y = y
        self.isCross = isCross
        self.route = route
        self.direction = direction
        self.nodes = []
        self.node = None
        self.image = None
        self.text = None