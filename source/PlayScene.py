
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
		self.chunkOffsets = [(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2)]
		self.player.x = self.chunkOffsets[0][0] + 2.0
		self.player.y = self.chunkOffsets[0][1] + 3.0
		self.shooterCooldown = -1
		self.cameraX = self.player.x * 64
		self.cameraY = self.player.y * 64
		self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
		self.overlay.fill((0, 0, 0))
		self.lightblender = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
		
		
		
	def update(self):
		player = self.player
		bulletOriginX = player.x
		bulletOriginY = player.y - player.height * .75
		
		pxScreen = bulletOriginX * 64 - self.cameraX + SCREEN_WIDTH // 2
		pyScreen = bulletOriginY * 64 - self.cameraY + SCREEN_HEIGHT // 2
		dt = 1.0 / FPS # bullet time would go here
		#for sprite in self.sprites:
		#	sprite.update(self, dt)
		self.shooterCooldown -= 1
		
		bulletVelocity = 10.0
		
		if InputManager.isShooting and self.shooterCooldown < 0:
			self.shooterCooldown = 13
			shoot = False
			if InputManager.mousePosition != None:
				mx, my = InputManager.mousePosition
				dx = mx - pxScreen
				dy = my - pyScreen
				dist = (dx ** 2 + dy ** 2) ** .5
				if dist > 10:
					ux = dx / dist
					uy = dy / dist
					shoot = True
			elif InputManager.shootStickDirection != None:
				ux = 0.0
				uy = 1.0
				shoot = True
			if shoot:
				vx = ux / 30 * bulletVelocity
				vy = uy / 30 * bulletVelocity
				self.projectiles.append(Projectile(bulletOriginX, bulletOriginY, vx, vy, (128, 255, 255), 3))
		
		for projectile in self.projectiles:
			projectile.update(self)
		
		
	def render(self, screen):
		# There are 7 layers
		
		cameraX = self.player.x * 64
		cameraY = self.player.y * 64
		cameraOffsetX = -cameraX + SCREEN_WIDTH // 2
		cameraOffsetY = -cameraY + SCREEN_HEIGHT // 2
		
		self.renderTiles(screen, cameraOffsetX, cameraOffsetY)
		self.renderProjectiles(screen, self.projectiles, cameraOffsetX, cameraOffsetY)
		self.renderSprites(screen, self.sprites, cameraOffsetX, cameraOffsetY)
		self.renderLighting(screen, self.projectiles, cameraOffsetX, cameraOffsetY)
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
					newIndex = x + y * VIRTUAL_WIDTH
					self.tilesByIndexCache[newIndex] = tiles[index]
	
	def renderTiles(self, screen, cameraOffsetX, cameraOffsetY):
		left = int(-cameraOffsetX / 64 - 2)
		top = int(-cameraOffsetY / 64 - 2)
		right = left + SCREEN_WIDTH // 64 + 4
		bottom = top + SCREEN_HEIGHT // 64 + 4
		
		screen.fill((200, 200, 200))
		black = (0, 0, 0)
		self.ensureTilesFilled()
		lookup = self.tilesByIndexCache
		row = top
		while row <= bottom:
			index = left + row * VIRTUAL_WIDTH
			endIndex = right + row * VIRTUAL_WIDTH
			py = row * 64 + cameraOffsetY
			px = left * 64 + cameraOffsetX
			while index <= endIndex:
				tile = lookup.get(index, 'block')
				if tile == 'block':
					pygame.draw.rect(screen, black, (px, py, 64, 64))
				elif tile == 'empty':
					pass
				
				index += 1
				px += 64
			row += 1
		
	
	def renderProjectiles(self, screen, projectiles, cameraOffsetX, cameraOffsetY):
		for projectile in projectiles:
			projectile.renderBullet(screen, cameraOffsetX, cameraOffsetY)
		
	def renderSprites(self, screen, sprites, cameraOffsetX, cameraOffsetY):
		for sprite in sprites:
			sprite.render(screen, cameraOffsetX, cameraOffsetY)
	
	def renderLighting(self, screen, projectiles, cameraOffsetX, cameraOffsetY):
		pygame.draw.rect(self.overlay, (0, 0, 0), pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
		self.lightblender.blit(self.overlay, (0, 0), None, pygame.BLEND_RGBA_SUB)
		
		for projectile in projectiles:
			for path, scale in [('gradients/blue_30.png', 1), ('gradients/blue.png', .3)]:
				blueGradient = ImageLibrary.getAtScale(path, scale)
				x = int(projectile.x * 64 + cameraOffsetX)
				y = int(projectile.y * 64 + cameraOffsetY)
				w, h = blueGradient.get_size()
				self.lightblender.blit(blueGradient, (x - w // 2, y - h // 2))
		
		self.overlay.blit(self.lightblender, (0, 0), None, pygame.BLEND_RGBA_SUB)
		screen.blit(self.overlay, (0, 0))
