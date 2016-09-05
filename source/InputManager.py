
class InputManager_:
	def __init__(self):
		self.menuEventQueue = []
		self.quitAttempted = False
		
		self.joystickMoveVector = [0.0, 0.0]
		self.keyboardMoveVector = [0.0, 0.0]
		self.useKeyboard = True
		self.jumpPressed = False
		self.magicJumpPressed = False
		self.systemKeysPressed = {}
	
	def applySystemEvents(self, events):
		# Reset all values
		while len(self.menuEventQueue) > 0:
			self.menuEventQueue.pop()
	
		self.quitAttempted = False
		
		for event in events:
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				self.useKeyboard = True
				down = event.type == pygame.KEYDOWN
				k = event.key
				self.systemKeysPressed[k] = down
				if k == pygame.K_w or k == pygame.K_UP:
					if down: self.menuEventQueue.append('up')
				elif k == pygame.K_s or k == pygame.K_DOWN:
					if down: self.menuEventQueue.append('down')
				elif k == pygame.K_a or k == pygame.K_LEFT:
					if down: self.menuEventQueue.append('left')
				elif k == pygame.K_d or k == pygame.K_RIGHT:
					if down: self.menuEventQueue.append('right')
				elif k == pygame.K_ESCAPE:
					self.quitAttempted = True
				elif k == pygame.K_F4:
					if self.systemKeysPressed.get(pygame.K_LALT, False) or self.systemKeysPressed.get(pygame.K_RALT, False):
						self.quitAttempted = True
				elif k == pygame.K_RETURN:
					if down: self.menuEventQueue.append('enter')
				elif k == pygame.K_SPACE:
					if down: self.menuEventQueue.append('enter')
					self.jumpPressed = down
				elif k == pygame.K_f:
					self.magicJumpPressed = down
			elif event.type == pygame.QUIT:
				self.quitAttempted = True
		
		pressed = self.systemKeysPressed
		leftPressed = pressed.get(pygame.K_a, False)
		rightPressed = pressed.get(pygame.K_d, False)
		upPressed = pressed.get(pygame.K_w, False)
		downPressed = pressed.get(pygame.K_s, False)
		self.keyboardMoveVector[0] = -1 if leftPressed else 1 if rightPressed else 0
		self.keyboardMoveVector[1] = -1 if upPressed else 1 if downPressed else 0
		
	def getMenuEvents(self):
		return self.menuEventQueue
	
	def getDirectionVector(self):
		
		if self.useKeyboard:
			x, y = self.keyboardMoveVector
		else:
			x, y = self.joystickMoveVector
		
		dist = (x ** 2 + y ** 2) ** .5
		if dist > 1:
			x = x / dist
			y = y / dist
		
		return (x, y)


InputManager = InputManager_()
