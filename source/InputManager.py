
class InputManager_:
	def __init__(self):
		self.menuEventQueue = []
		self.gameplayEventQueue = []
		self.mousePosition = [0, 0]
		self.shootStickDirection = [0.0, 0.0]
		self.isShooting = False
		self.moveStickDirection = [-1.0, 0.0]
		self.quitAttempted = False
		self.keyboardX = 0
		self.keyboardY = 0
		self.systemKeysPressed = {}
	
	def applySystemEvents(self, events):
		# Reset all values
		while len(self.menuEventQueue) > 0:
			self.menuEventQueue.pop()
	
		while len(self.gameplayEventQueue) > 0:
			self.gameplayEventQueue.pop()
		
		self.quitAttempted = False
		
		# And get new values
		keyX = self.keyboardX
		keyY = self.keyboardY
		
		for event in events:
			if event.type == pygame.MOUSEMOTION:
				self.mousePosition = event.pos
			elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				down = event.type == pygame.KEYDOWN
				k = event.key
				self.systemKeysPressed[k] = down
				if k == pygame.K_w:
					keyY = -1
				elif k == pygame.K_s:
					keyY = 1
				elif k == pygame.K_a:
					keyX = -1
				elif k == pygame.K_d:
					keyX = 1
				elif k == pygame.K_ESCAPE:
					self.quitAttempted = True
				elif k == pygame.K_F4:
					if self.systemKeysPressed.get(pygame.K_LALT, False) or self.systemKeysPressed.get(pygame.K_RALT, False):
						self.quitAttempted = True
			elif event.type == pygame.QUIT:
				self.quitAttempted = True
		
		directionDirty = False
		if keyX != self.keyboardX:
			if keyX != 0:
				self.menuEventQueue.append('left' if keyX == -1 else 'right')
			self.keyboardX = keyX
			directionDirty = True
		if keyY != self.keyboardY:
			if keyY != 0:
				self.menuEventQueue.append('up' if keyX == -1 else 'down')
			self.keyboardY = keyY
			directionDirty = True
		
		if directionDirty:
			if keyX == 0 or keyY == 0:
				self.moveStickDirection[0] = keyX * 1.0
				self.moveStickDirection[1] = keyY * 1.0
			else:
				self.moveStickDirection[0] = keyX * .707
				self.moveStickDirection[1] = keyY * .707
		
	def getMenuEvents(self):
		return self.menuEventQueue
	

InputManager = InputManager_()
