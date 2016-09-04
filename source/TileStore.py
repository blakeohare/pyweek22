
class TileStore_:
	def __init__(self):
		self.tiles = {}
	
	def get(self, tileId):
		tile = self.tiles.get(tileId)
		if tile == None:
			tile = TileTemplate(tileId)
			self.tiles[tileId] = tile
		return tile
TileStore = TileStore_()
