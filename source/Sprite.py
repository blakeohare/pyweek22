
ROW_COLLISION_CACHE = [False] * 1000
PLAYER_JUMP_VELOCITY = -0.4

class Sprite:
	def __init__(self, template, x, y):
		self.type = type
		self.x = x + 0.0
		self.y = y + 0.0
		self.template = template
		self.dx = 0
		self.dy = 0
		self.vx = 0.0
		self.vy = 0.0
		self.ground = None
		self.visualHeight = 2.0
		self.effectiveHeight = self.visualHeight - .25
		self.rowCollisionCache = None
		self.draggingAgainstWall = False
		self.lastDir = 'east'
		self.dead = False
		self.dustCounter = -1
		self.forceAppliedX = 0.0
	
	def updateHorizontal(self, scene, dx):
		
		newX = self.x + dx
		newCol = int(newX)
		oldCol = int(self.x)
		rowBottom = int(self.y)
		rowTop = int(self.y - self.effectiveHeight)
		
		if self.ground == None:
			# flying horizontally through the air
			
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
			passable = bottomTile == None or not bottomTile.blocking or bottomTile.bar
			if not passable:
				inclineType = bottomTile.inclineType
				if inclineType == 'up':
					if collisionX + collisionY >= 1.0:
						# it's a collision, update feet to stand on ground at collision point
						if collisionX > 0.99: collisionX = .99
						if collisionX < 0.01: collisionX = .01
						self.ground = bottomTile
						self.x = oldCol + collisionX + 0.0
						self.y = rowBottom + 1.0 - collisionX
						return
				elif inclineType == 'down':
					if 1 - collisionX + collisionY >= 1.0:
						# it's a collision, update feet to stand on ground at collision point
						if collisionX > 0.99: collisionX = .99
						if collisionX < 0.01: collisionX = .01
						self.ground = bottomTile
						self.x = oldCol + collisionX + 0.0
						self.y = rowBottom + collisionX + 0.0
						return
				else:
					raise Exception("Somehow managed to move to a tile that isn't an incline")
			else:
				#####
				# You are flying through the air.
				# Go ahead and move as far as you can within this same column.
				#####
				
				if newCol == oldCol:
					# move all the way to the destination.
					self.x += dx
				else:
					# move as far as you can within this single column.
					originalX = self.x
					if newCol > oldCol:
						# moving to the right.
						newPartialX = oldCol + .99
					else:
						# moving to the left
						newPartialX = oldCol + 0.01
					# take away the amount that you moved from dx and continue on
					diff = newPartialX - self.x
					dx -= diff
					self.x = newPartialX
				
			#####
			# Continue through to the next tile if applicable
			#####
			if newCol != oldCol:
				collisionX = newX % 1.0
				newColumnTiles = scene.tiles[newCol]
				
				row = rowTop
				while row < rowBottom:
					# any collisions here should be treated as blockers
					# note that this doesn't check the bottom row
					
					tile = newColumnTiles[row]
					if tile != None and tile.blocking:
						self.draggingAgainstWall = True
						self.vx = 0
						return # Collision
					
					row += 1
				
				tile = newColumnTiles[rowBottom]
				if tile == None or not tile.blocking:
					self.x = newX
					return
				
				if not tile.isIncline:
					self.draggingAgainstWall = True
					self.vx = 0
					return # Collision
				
				collisionY = self.y % 1.0
				if collisionY < 0.01: collisionY = 0.01
				elif collisionY > 0.99: collisionY = 0.99
				
				if tile.inclineType == 'up':
					if oldCol > newCol:
						self.vx = 0
						return
					if collisionY + collisionX < 1:
						self.x = newX
						self.vx = 0
						return
					self.x = newCol + 1.0 - collisionY
					self.y = collisionY + rowBottom
					self.ground = tile
					return
				
				if tile.inclineType == 'down':
					if oldCol < newCol:
						self.vx = 0
						return
					if collisionY + 1 - collisionX < 1:
						self.x = newX
						self.vx = 0
						return
					self.x = newCol + collisionY + 1.0
					self.y = collisionY + rowBottom
					self.ground = tile
					return
					
				raise Exception("Unknown inclineType: '" + str(tile.inclineType) + "'")

		else:
			# TODO: need to run the newCol == oldCol code block even if you're walking out of the current column
			# In which case, you walk all the way up to the edge - epsilon and then modify dx by the amount traversed.
			
			#####
			# walking on the ground
			#####
			if newCol == oldCol:
			
				# Nothing stopping you if you're in the same X coordinate
				self.x = newX
				
				#####
				# Moving around on a flat tile and doesn't cross boundaries
				#####
				if not self.ground.isIncline:
					return
				
				#####
				# Moving around on an incline and not crossing boundaries
				#####
				ux = self.x % 1.0
				type = self.ground.inclineType
				if ux < 0.01: ux = 0.01
				elif ux > 0.99: ux = 0.99
				
				if type == 'up':
					self.y = rowBottom + 1 - ux
					return
				elif type == 'down':
					self.y = rowBottom + ux
					return
				
				raise Exception("Unknown inclineType: '" + str(tile.inclineType) + "'")
			
			#####
			# Walking out of bounds?
			#####
			if newCol < 0 or newCol >= scene.width:
				self.vx = 0
				return # Nope
			
			currentGround = self.ground
			newTileColumn = scene.tiles[newCol]
			
			cleanConnectTile = None
			cleanConnectY = currentGround.row # this references the y coordinate, not the nth row, so 4 here means the top of tileColumn[4], just after the bottom of tileColumn[3].
			# TODO: cleanConnect will have to support half-increments.
			
			#####
			# Check what y coordinate the next column should line up with to make a clean continuous platform connection
			#####
			if currentGround.isIncline:
				type = currentGround.inclineType
				if type == 'up':
					cleanConnectY = currentGround.row if newCol > oldCol else (currentGround.row + 1)
				elif type == 'down':
					cleanConnectY = (currentGround.row + 1) if newCol > oldCol else currentGround.row
				else:
					raise Exception("Unknown incline type: '" + type + "'")
			else:
				cleanConnectY = currentGround.row
			
			#####
			# Now look for a tile that connects cleanly
			#####
			
			newGroundCandidate = None
			if oldCol < newCol: # coming from the left
				tile = newTileColumn[cleanConnectY - 1]
				if tile != None and tile.inclineType == 'up':
					newGroundCandidate = tile
				else:
					tile = newTileColumn[cleanConnectY]
					if tile != None and (not tile.isIncline or tile.inclineType == 'down'):
						newGroundCandidate = tile
			else:
				tile = newTileColumn[cleanConnectY - 1]
				if tile != None and tile.inclineType == 'down':
					newGroundCandidate = tile
				else:
					tile = newTileColumn[cleanConnectY]
					if tile != None and (not tile.isIncline or tile.inclineType == 'up'):
						newGroundCandidate = tile
			
			if newGroundCandidate != None:
				#####
				# Adjust newY
				#####
				ux = newX % 1.0
				if ux < 0.01: ux = 0.01
				elif ux > 0.99: ux = 0.99
				
				if newGroundCandidate.isIncline:
					type = newGroundCandidate.inclineType
					if type == 'up':
						newY = newGroundCandidate.row + 1.0 - ux
					elif type == 'down':
						newY = newGroundCandidate.row + ux + 0.0
					else:
						raise Exception("Unknown incline type: '" + type + "'")
				else:
					newY = newGroundCandidate.row + 0.0
			else:
				#####
				# If the player is walking off of a platform, then they will enter freefall mode but keep their current Y value initially.
				#####
				newY = self.y
			
			newRowBottom = int(newY)
			newRowTop = int(newY - self.effectiveHeight)
			row = newRowTop
			collision = False
			while row < newRowBottom: # don't check row bottom
				tile = newTileColumn[row]
				if tile != None and (tile.blocking or tile.isIncline):
					collision = True
					self.vx = 0
					break
				row += 1
			
			if not collision:
				self.ground = newGroundCandidate
				self.x = newX
				self.y = newY
	
	def updateVerticalGoingUp(self, scene, dy):
		col = int(self.x)
		newRow = int(self.y + dy - self.effectiveHeight)
		if newRow < 0: return # hit the top
		tile = scene.tiles[col][newRow]
		if tile != None and (tile.blocking or tile.isIncline):
			# head bonks the ceiling
			self.vy = 0.0 # velocity is now 0
			self.y = tile.row + 1.0 + self.effectiveHeight + 0.001
			return
		
		self.y += dy
	
	def updateVerticalGoingDown(self, scene, dy):
		col = int(self.x)
		oldRow = int(self.y)
		newRow = int(self.y + dy)
		if newRow >= scene.height:
			# fell off the bottom
			# TODO: this will be valid and I'll need to allow this
			# will likely do something that extends the tiles around the edge to infinity.
			return
		
		columnTiles = scene.tiles[col]
		
		tile = columnTiles[oldRow]
		if tile == None or (not tile.blocking and not tile.bar):
			tile = columnTiles[newRow]
		
		if tile == None or (not tile.blocking and not tile.bar):
			self.y += dy
			return
		
		if not tile.isIncline:
			self.y = tile.row + 0.0
			self.ground = tile
			self.vy = 0
			return
		
		type = tile.inclineType
		ux = self.x % 1.0
		uy = self.y % 1.0
		if ux < 0.01: ux = 0.01
		elif ux > 0.99: ux = 0.99
		
		newY = self.y + dy
		if type == 'up':
			inclineY = tile.row + 1 - ux
		elif type == 'down':
			inclineY = tile.row + ux
		else:
			raise Exception("Unknown incline type: '" + type + "'")
		
		if newY > inclineY:
			self.y = inclineY
			self.ground = tile
			self.vy = 0
		else:
			self.y = newY
	
	def update(self, scene, timeRatio):
		if self.ground == None:
			self.vy += GRAVITY
			self.dy += self.vy
		else:
			self.vy = 0
			self.dy = 0
		
		self.dx += self.vx
			
		
		self.dx *= timeRatio
		self.dy *= timeRatio
		
		self.draggingAgainstWall = False
		self.updateImpl(scene)
	
	# Note: the collision box of the player for the purposes of movement is actually just a vertical line
	def updateImpl(self, scene):
		dx = self.dx
		dy = self.dy
		
		# nothing to do
		if dx == 0 and dy == 0:
			return
		
		if self.dustCounter < 0:
			if self.ground != None and ((self.forceAppliedX < 0) != (self.vx < 0)) and abs(self.forceAppliedX) > .2:
				self.dustCounter = 5
				for i in range(3):
					dust = Debris(self.x, self.y, (128, 128, 128), 'grow-and-fade')
					scene.sprites.append(dust)
					dust.vx = self.vx / 10.0 + random.random() * 0.03 - 0.015
					dust.vy = -0.02 + random.random() * 0.02
		else:
			self.dustCounter -= 1
			
		
		#####
		# Break the vector into half and call update twice if the vector has a magnitude > 1
		# This simplifies the physics logic. 
		# This also works recursively.
		#####
		if dx < -1 or dx > 1 or dy < -1 or dy > 1:
			incrementalDx = self.dx * .5
			incrementalDy = self.dy * .5
			i = 0
			while i < 2:
				self.dx = incrementalDx
				self.dy = incrementalDx
				self.updateImpl(scene)
				i += 1
			return
		if dx != 0:
			self.updateHorizontal(scene, dx)
			if self.draggingAgainstWall:
				if dy <= 0: 
					# moving up or stationary so not really dragging against it
					self.draggingAgainstWall = False
				else:
					# slow down descent
					if dy > .03:
						dy = .03
						self.vy = 0.03
			self.dx = 0
			if self.ground != None:
				self.vy = 0.0
				dy = 0
				
		if dy != 0:
			if dy < 0:
				self.updateVerticalGoingUp(scene, dy)
			else:
				self.updateVerticalGoingDown(scene, dy)
			self.dy = 0
		
		if self.ground != None:
			self.vy = 0
		
		if self.draggingAgainstWall and self.dustCounter < 0:
			self.dustCounter = 9
			x = self.x
			if self.x % 1.0 < .5:
				x -= .35
			else:
				x += .35
			dust = Debris(x, self.y - 1.7, (128, 128, 128), 'grow-and-fade')
			scene.sprites.append(dust)
			dust.vy = -0.03 + 0.015 * random.random()
			dust.vx = -0.01 + 0.02 * random.random()
	
	def render(self, screen, cameraOffsetX, cameraOffsetY, rtInt):
		
		# TODO: maybe this should go in update?
		if self.vx == 0:
			dir = self.lastDir
		else:
			dir = 'east' if self.vx > 0 else 'west'
			self.lastDir = dir
			
		centerX = self.x * 32 + cameraOffsetX
		bottomY = self.y * 32 + cameraOffsetY
		xOffset = 0
		yOffset = 0
		if self.draggingAgainstWall:
			if self.x % 1.0 < .5:
				dir = 'east'
				xOffset = 8
			else:
				dir = 'west'
				xOffset = -8
			
			path = 'sprites/player/walldrag-' + dir + '-1.png'
		else:
			num = int((rtInt % 3) + 1)
			path = 'sprites/player/stand-' + dir + '-' + str(num) + '.png'
		
		img = ImageLibrary.getAtScale(path, 4)	
		left = int(centerX - img.get_width() // 2 + xOffset)
		top = int(bottomY - img.get_height() + yOffset)
		screen.blit(img, (left, top))
		