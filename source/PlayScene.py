
class PlayScene:
	def __init__(self):
		self._next = None
		values = MapParser.parseMap('test')
		self.width = values['width']
		self.height = values['height']
		self.tiles = values['tiles']
		self.music = values['music']
		self.sprites = []
		for spriteAttr in values['sprites']:
			pass # TODO: add sprites
		
		self.doors = values['doors']
		startingDoor = self.doors[values['startDoorId']]
		
		self.player = Sprite('player', startingDoor.col + .5, startingDoor.row + 1)
		self.sprites = [self.player] + self.sprites
		
		self.cameraX = self.player.x
		self.cameraY = self.player.y
		self.xs = list(range(self.width))
		self.ys = list(range(self.height))
		
		self.rt = 0.0 # current time as far as the renderer is concerned
		self.rtLast = time.time() # the last time the rt value was updated
		
	def update(self):
		player = self.player
		playerPos = (player.x, player.y)
		
		movementVector = InputManager.getDirectionVector()
		
		if player.ground:
			player.dx = movementVector[0]
			
			if InputManager.jumpPressed:
				player.ground = None
				player.vy = -.15
		
		dt = 1.0 # TODO: update for bullet time
		for sprite in self.sprites:
			sprite.update(self, dt)
		
		
	def render(self, screen):
		
		newRtLast = time.time()
		diff = time.time() - self.rtLast # how long has passed since the last frame?
		# TODO: adjust diff for bullet-time to slow down animations
		rt = self.rt + diff # add that to the render time
		self.rt = rt
		self.rtLast = newRtLast
		
		targetCameraX = self.player.x
		targetCameraY = self.player.y
		
		cameraInterpolationRatio = .1
		
		self.cameraX = self.cameraX * (1 - cameraInterpolationRatio) + targetCameraX * cameraInterpolationRatio
		self.cameraY = self.cameraY * (1 - cameraInterpolationRatio) + targetCameraY * cameraInterpolationRatio
		
		cameraOffsetX = int((-self.cameraX) * 32 + SCREEN_WIDTH // 2)
		cameraOffsetY = int((-self.cameraY) * 32 + SCREEN_HEIGHT // 2)
		
		self.renderTiles(screen, cameraOffsetX, cameraOffsetY, rt)
		self.renderSprites(screen, self.sprites, cameraOffsetX, cameraOffsetY)
	
	def renderTiles(self, screen, cameraOffsetX, cameraOffsetY, rt):
		
		py = cameraOffsetY
		for row in self.ys:
			px = cameraOffsetX
			for col in self.xs:
				tile = self.tiles[col][row]
				if tile != None:
					img = tile.staticImage
					if img == None:
						images = tile.images
						img = images[int(rt * (8.0 / 60) * self.animationSpeedRatio) % len(images)]
					screen.blit(img, (px, py))
				px += 32
			py += 32		
	
	def renderSprites(self, screen, sprites, cameraOffsetX, cameraOffsetY):
		for sprite in sprites:
			sprite.render(screen, cameraOffsetX, cameraOffsetY)
	