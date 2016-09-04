GRAVITY = .01

ROW_COLLISION_CACHE = [False] * 1000

class Sprite:
	def __init__(self, template, x, y):
		self.type = type
		self.x = x + 0.0
		self.y = y + 0.0
		self.template = template
		self.dx = None
		self.dy = None
		self.vy = 0.0
		self.ground = None
		self.visualHeight = 1.0
		self.effectiveHeight = .75
		self.rowCollisionCache = None
	
	def updateHorizontal(self, scene, dx):
		newX = self.x + dx
		newCol = int(newX)
		oldCol = int(self.x)
		if (self.ground == None):
			# flying horizontally through the air
			rowBottom = int(self.y)
			rowTop = int(self.y - self.effectiveHeight)
			
			#####
			# first ensure that no inclines were collided with in the current tile
			#####
			oldColumnTiles = scene.tiles[oldCol]
			if newCol == oldCol:
				collisionX = newX % 1 # check the new position if you're only moving in this tile
			elif dx < 0:
				collisionX = 0.0 # check the leftmost point in this tile if you're moving left out of this tile
			else:
				collisionX = 1.0 # check the rightmost point in this tile if you're moving right out of this tile
			collisionY = (self.y) % 1.0
			
			bottomTile = oldColumnTiles[rowBottom]
			if bottomTile != None:
				inclineType = bottomTile.inclineType
				if inclineType == 'up':
					if collisionX + collisionY >= 1.0:
						# it's a collision, update feet to stand on ground at collision point
						if collisionX > 0.99: collisionX = .99
						if collisionX < 0.01: collisionX = .01
						self.ground = bottomTile
						self.x = oldCol + collisionX + 0.0
						self.y = rowBottom + 1.0 - self.collisionX
						return
				elif inclineType == 'down':
					if 1 - collisionX + collisionY >= 1.0:
						# it's a collision, update feet to stand on ground at collision point
						if collisionX > 0.99: collisionX = .99
						if collisionX < 0.01: collisionX = .01
						self.ground = bottomTile
						self.x = oldCol + collisionX + 0.0
						self.y = rowBottom + self.collisionX + 0.0
						return
				else:
					raise Exception("Somehow managed to move to a tile that isn't an incline")
			
			#####
			# Continue through to the next tile if applicable
			#####
			if newCol != oldCol:
				collisionX = newX % 1.0
				oldColumnTiles = scene.tiles[oldCol]
				
				row = rowTop
				while row < rowBottom:
					# any collisions here should be treated as blockers
					# note that this doesn't check the bottom row
					
					tile = oldColumnTiles[row]
					if tile != None and tile.blocking:
						return # Collision
					
					row += 1
				
				tile = oldColumnTiles[rowBottom]
				if tile == None:
					self.x = newX
					return
				
				if not tile.isIncline:
					return # Collision
				
				if tile.inclineType:
					
				
		else:
			# walking on the ground
			pass
		
	
	# Note: the collision box of the player for the purposes of movement is actually just a vertical line
	def update(self, scene, timeRatio):
		# update horizontal changes
		if self.dx != 0 or self.dy != 0:
			dx = self.dx * timeRatio
			dy = self.dy * timeRatio
			
			# guarantee that no vector component is greater than 1 in magnitude by breaking it in half recursively as needed
			if dx < -1 or dx > 1 or dy < -1 or dy > 1:
				incrementalDx = self.dx * .5
				incrementalDy = self.dy * .5
				i = 0
				while i < 2:
					self.dx = incrementalDx
					self.dy = incrementalDx
					self.update(scene, timeRatio)
					i += 1
				return
			
			if self.dx != None:
				self.updateHorizontal(scene, dx)
		
	
	def render(self, screen, cameraOffsetX, cameraOffsetY):
		centerX = self.x * 32 + cameraOffsetX
		bottomY = self.y * 32 + cameraOffsetY
		left = int(centerX - 16)
		top = int(bottomY - 32)
		pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(left, top, 32, 32))
