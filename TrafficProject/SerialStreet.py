class SerialStreet:
    def __init__(self, is_cross, is_corner, grades, direction, text, x, y):
        self.is_cross = is_cross
        self.is_corner = is_corner
        self.grades = grades
        self.direction = direction
        self.text = text
        self.x = x
        self.y = y
        self.node = None
        self.nodes = None
