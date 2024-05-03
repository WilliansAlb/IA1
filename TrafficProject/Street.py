class Street:
    def __init__(self, x, y, isCross, route, direction):
        self.x = x
        self.y = y
        self.isCross = isCross
        self.route = route
        self.direction = direction
        self.direction_label = None
        self.nodes = []
        self.node = None
        self.image = None
        self.text = None
        self.grades = None
        self.is_corner = False
        self.label = None

