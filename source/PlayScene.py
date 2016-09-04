
class PlayScene:
	def __init__(self):
		self._next = None
		self.player = Sprite('player', 2, 3)
		self.sprites = [self.player]
		self.projectiles = []
		
		ids = """
xxxxxxxxxx
x        x
x        x
x  xxx   x
x    xx  x
x        x
x        x
x        x
x        x
x        x
xxxxxxxxxx""".strip().replace('\r\n', '\n').replace('\r', '\n').split('\n')
		width = len(ids[0])
		height = len(ids)
		self.tiles = makeGrid(width, height)
		for x in range(width):
			for y in range(height):
				self.tiles[x][y] = Tile(x, y, TileStore.get(ids[y][x]))
		self.width = width
		self.height = height
		
	def update(self):
		dt = 1.0 / FPS # bullet time would go here
		for sprite in self.sprites:
			sprite.update(self, dt)
		
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
	
	def renderTiles(self, screen, cameraX, cameraY):
		for y in range(self.height):
			for x in range(self.width):
				tile = self.tiles[x][y]
				img = tile.staticImage
				if img != None:
					screen.blit(img, (x * 64 - cameraX, y * 64 - cameraY))
	
	def renderProjectiles(self, screen, projectiles, cameraX, cameraY):
		pass
		
	def renderSprites(self, screen, sprites, cameraX, cameraY):
		for sprite in sprites:
			sprite.render(screen, cameraX, cameraY)
	
	def renderLighting(self, screen, projectiles, cameraX, cameraY):
		pass
