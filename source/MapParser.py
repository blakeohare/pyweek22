class MapParser:
	
	@staticmethod
	def parseMap(id):
		lines = readTextResourceLines('maps/' + id + '.txt')
		tileLines = []
		width = -1
		height = 0
		spriteLines = []
		music = None
		doors = {}
		
		mode = None
		for line in lines:
			if line[0] == '#':
				parts = line[1:].split(':')
				key = parts[0].strip().lower()
				value = ':'.join(parts[1:]).strip()
				if key == 'music':
					music = value
				elif key == 'tiles':
					mode = 'tiles'
				elif key == 'sprites':
					mode = 'sprites'
			elif mode == 'tiles':
				items = list(line)
				if width == -1:
					width = len(items)
				elif len(items) != width:
					raise Exception("Error while parsing map '" + id + "': row " + str(len(tileLines) + 1) + " does not have expected number of tiles (" + str(width) + ")")
				tileLines.append(items)
			elif mode == 'sprites':
				spriteLines.append(line.split(','))
		
		if width == -1: raise Exception("No tile data.")
		height = len(tileLines)
		
		tiles = makeGrid(width, height)
		for y in range(height):
			for x in range(width):
				id = tileLines[y][x]
				if id == '.':
					tile = None
				else:
					tile = Tile(TileStore.get(id), x, y)
				tiles[x][y] = tile
		
		tempStartDoor = Door('start', 2, height - 2)
		doors[tempStartDoor.id] = tempStartDoor
		doorStartId = tempStartDoor.id
		return {
			'width': width,
			'height': height,
			'music': music,
			'sprites': spriteLines,
			'tiles': tiles,
			'doors': doors,
			'startDoorId': doorStartId,
		}
