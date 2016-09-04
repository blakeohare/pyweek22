TILE_ID_KEY_LOOKUP = {
	'.': 'empty',
	'X': 'block',
	'/': 'incline-right',
	'\\': 'incline-left',
	'V': 'stallactite',
	'^': 'stallagmite',
}

class MapChunk:
	def __init__(self, type):
		c = open(('maps/' + type + '.txt').replace('/', os.sep), 'rt')
		text = c.read().upper()
		c.close()
		lines = text.strip().split('\n')
		lines[0] = lines[0].strip()
		width = len(lines[0])
		height = len(lines)
		tiles = {}
		y = 0
		while y < height:
			line = lines[y].strip()
			x = 0
			while x < width:
				tileId = TILE_ID_KEY_LOOKUP.get(line[x])
				if tileId != None:
					index = x + y * width
					tiles[index] = tileId
				x += 1
			y += 1
		self.tiles = tiles
		self.width = width
		self.height = height
		
_mapChunks = {}
def getMapChunk(type):
	chunk = _mapChunks.get(type)
	if chunk == None:
		chunk = MapChunk(type)
		_mapChunks[type] = chunk
	return chunk

CHUNKS_BY_DIR = {
	'east-east': ['short_tunnel', 'some_platforms'],
	'west-west': ['short_tunnel'],
}

def getRandomChunkByDirection(startDir, endDir):
	choices = CHUNKS_BY_DIR.get(startDir + '-' + endDir)
	id = random.choice(choices)
	return getMapChunk(id)
		