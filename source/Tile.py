
class Tile:
	def __init__(self, template, col, row):
		self.images = template.images
		self.col = col
		self.row = row
		self.blocking = template.blocking
		self.staticImage = self.images[0]
		if len(self.images) > 1: self.staticImage = None
