
class PlayScene:
	def __init__(self):
		self._next = None
		self.player = Sprite('player', 2, 3)
		self.sprites = [self.player]
		self.projectiles = []
		
		# a tile is accessible by its index in a 1D array that's been flattened from a 2D array
		# i.e. index = x + (y * width)
		# use a dictionary instead of a list since the 2D grid is 1 million by 1 million
		self.tilesByIndexCache = None # lazily initialized from self.chunks
		self.chunks = [getMapChunk('starting')] # list of dictionaries of tile indices
		self.chunkOffsets = [(1000000, 1000000)]
		self.player.x = 1000002.0
		self.player.y = 1000004.0
		
		
	def update(self):
		dt = 1.0 / FPS # bullet time would go here
		#for sprite in self.sprites:
		#	sprite.update(self, dt)
		
	def render(self, screen):
		# There are 7 layers
		
		cameraX = self.player.x * 64 - screen.get_width() // 2
		cameraY = self.player.y * 64 - screen.get_height() // 2
		
		self.renderTiles(screen, cameraX, cameraY)
		self.renderProjectiles(screen, self.projectiles, cameraX, cameraY)
		self.renderSprites(screen, self.sprites, cameraX, cameraY)
		self.renderLighting(screen, self.projectiles, cameraX, cameraY)
		#self.renderText(screen)
		#self.renderHud(screen)
	
	def ensureTilesFilled(self):
		if self.tilesByIndexCache == None:
			self.tilesByIndexCache = {}
			for i in range(len(self.chunks)):
				chunk = self.chunks[i]
				chunkOffsets = self.chunkOffsets[i]
				tiles = chunk.tiles
				width = chunk.width
				for index in tiles.keys():
					x = index % width
					y = index // width
					x = chunkOffsets[0] + x
					y = chunkOffsets[1] + y
					newIndex = x + y * 1000000
					self.tilesByIndexCache[newIndex] = tiles[index]
	
	def renderTiles(self, screen, cameraX, cameraY):
		left = int((cameraX - SCREEN_WIDTH / 2) / 64 - 2)
		top = int((cameraY - SCREEN_HEIGHT / 2) / 64 - 2)
		right = left + SCREEN_WIDTH // 64 + 4
		bottom = top + SCREEN_HEIGHT // 64 + 4
		
		screen.fill((0, 0, 100))
		black = (0, 0, 0)
		self.ensureTilesFilled()
		lookup = self.tilesByIndexCache
		row = top
		while row <= bottom:
			index = left + row * 1000000
			endIndex = index - left + right
			py = row * 64 - cameraY + SCREEN_HEIGHT // 2
			px = left * 64 - cameraX + SCREEN_WIDTH // 2
			while index <= endIndex:
				tile = lookup.get(index, 'block')
				if tile == 'block':
					pygame.draw.rect(screen, black, (px, py, 64, 64))
				elif tile == 'empty':
					pass
				index += 1
				px += 64
			row += 1
		
	
	def renderProjectiles(self, screen, projectiles, cameraX, cameraY):
		pass
		
	def renderSprites(self, screen, sprites, cameraX, cameraY):
		for sprite in sprites:
			sprite.render(screen, cameraX, cameraY)
	
	def renderLighting(self, screen, projectiles, cameraX, cameraY):
		pass
