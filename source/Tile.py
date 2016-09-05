
class Tile:
	def __init__(self, template, col, row):
		self.images = template.images
		self.col = col
		self.row = row
		self.blocking = template.blocking
		self.isIncline = template.isIncline
		self.inclineType = template.inclineType
		self.staticImage = self.images[0]
		if len(self.images) > 1: self.staticImage = None
