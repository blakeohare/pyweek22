class TileTemplate:
	def __init__(self, id):
		self.blocking = id == 'x'
		self.images = [ImageLibrary.get('tiles/block.png' if id == 'x' else 'tiles/open.png')]
