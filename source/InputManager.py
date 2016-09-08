		

class InputManager_:
	def __init__(self):
		self.menuEventQueue = []
		self.quitAttempted = False
		
		self.joystickMoveVector = [0.0, 0.0]
		self.keyboardMoveVector = [0.0, 0.0]
		self.useKeyboard = True
		self.jumpPressed = False
		self.jumpPressedThisFrame = False
		self.jumpReleasedThisFrame = False
		self.keyboardMagicJumpPressed = False
		self.joystickMagicJumpPressed = False
		self.systemKeysPressed = {}
		self.escapePressed = False
		self.joysticks = None
		self.activeJoystick = -1
	
	def getActiveJoystick(self):
		if self.activeJoystick == -1:
			return None
		return self.joysticks[self.activeJoystick]
	
	def setActiveJoystick(self, index):
		js = self.joysticks[index]
		self.activeJoystick = index
		js.initialize()
	
	def clearActiveJoystick(self):
		self.activeJoystick = -1
	
	def getJoysticks(self):
		if self.joysticks == None:
			self.joysticks = []
			for i in range(pygame.joystick.get_count()):
				js = pygame.joystick.Joystick(i)
				jsWrapper = JoystickWrapper(i, js)
				self.joysticks.append(jsWrapper)
				if jsWrapper.alreadyConfigured and self.activeJoystick == -1:
					self.activeJoystick = i
		return self.joysticks
	
	def applySystemEvents(self, activeScene, events):
		self.getJoysticks()
		
		# Reset all values
		while len(self.menuEventQueue) > 0:
			self.menuEventQueue.pop()
	
		self.quitAttempted = False
		self.jumpPressedThisFrame = False
		self.jumpReleasedThisFrame = False
		self.escapePressed = False

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
					self.escapePressed = down
				elif k == pygame.K_F4:
					if self.systemKeysPressed.get(pygame.K_LALT, False) or self.systemKeysPressed.get(pygame.K_RALT, False):
						self.quitAttempted = True
				elif k == pygame.K_RETURN:
					if down: self.menuEventQueue.append('enter')
					self.keyboardMagicJumpPressed = down
				elif k == pygame.K_SPACE:
					if down: self.menuEventQueue.append('enter')
					self.jumpPressed = down
					self.jumpPressedThisFrame = down
					if not down:
						self.jumpReleasedThisFrame = True
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
		
		joystick = self.getActiveJoystick()
		if joystick != None:
			self.joystickMoveVector[0] = joystick.getAxis('move-left', 'move-right', True)
			self.joystickMoveVector[1] = joystick.getAxis('move-up', 'move-down', True)
			
			jumpPreviousState = joystick.getButtonPreviousState('a')
			jumpCurrentState = joystick.getBooleanState('a')
			self.jumpPressed = jumpCurrentState
			if jumpCurrentState != jumpPreviousState:
				self.jumpPressedThisFrame = jumpCurrentState
				self.jumpReleasedThisFrame = jumpPreviousState
			else:
				self.jumpPressedThisFrame = False
				self.jumpReleasedThisFrame = False
			
			startWasPressed = joystick.knownState.get('start', False)
			startIsPressed = joystick.getBooleanState('start')
			if startIsPressed and not startWasPressed:
				if activeScene.isPlayScene:
					self.escapePressed = True
				else:
					self.menuEventQueue.append('start')
			bWasPressed = joystick.knownState.get('b', False)
			bIsPressed = joystick.getBooleanState('b')
			if not bWasPressed and bIsPressed:
				self.escapePressed = True
			
			self.joystickMagicJumpPressed = joystick.getBooleanState('trigger')
		else:
			self.joystickMagicJumpPressed = False
		
	def getMenuEvents(self):
		return self.menuEventQueue
	
	def getDirectionVector(self):
		
		if self.activeJoystick == -1:
			x, y = self.keyboardMoveVector
		else:
			kx, ky = self.keyboardMoveVector
			jx, jy = self.joystickMoveVector
			x = kx if abs(kx) > abs(jx) else jx
			y = ky if abs(ky) > abs(jy) else jy
		
		dist = (x ** 2 + y ** 2) ** .5
		if dist > 1:
			x = x / dist
			y = y / dist
		
		return (x, y)
	
	def isMagicJumpPressed(self):
		return self.keyboardMagicJumpPressed or self.joystickMagicJumpPressed

InputManager = InputManager_()
