
class TileStore_:
	def __init__(self):
		self.tiles = None
		
	def initializeTiles(self):
		self.tiles = {}
		lines = readTextResourceLines('images/tiles/manifest.txt')
		for line in lines:
			if line[0] != '#':
				cols = line.split('\t')
				tileId = cols[0]
				flags = list(cols[1])
				if cols[2] != '-':
					images = []
					for imgFile in cols[2].split(','):
						images.append(ImageLibrary.getAtScale('tiles/' + imgFile.strip() + '.png', 4))
				self.tiles[tileId] = TileTemplate(tileId, images, flags)

	def get(self, tileId):
		if self.tiles == None: self.initializeTiles()
		return self.tiles[tileId]

TileStore = TileStore_()
