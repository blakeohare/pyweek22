
class JoystickWrapper:
	def __init__(self, index, actualJs):
		self.index = index
		self.js = actualJs
		self.name = actualJs.get_name()
		self.initialized = False
		self.axes = 0
		self.buttons = 0
		self.hats = 0
		self.configMapping = [{
			'move-left': None,
			'move-right': None,
			'move-up': None,
			'move-down': None,
			'A': None,
			'B': None,
			'X': None,
			'Y': None,
			'start': None,
			'trigger': None,
		}]
		self.knownState = {}
		self.taken = [{}]
		self.fingerprint = computeMD5(self.name)[:10]
		self.alreadyConfigured = False
		self.configFilename = 'joystick-config-' + self.fingerprint + '.txt'
		existingConfig = readFileMaybe(self.configFilename)
		if existingConfig != None:
			for line in existingConfig.split('\n'):
				line = line.strip().lower()
				if len(line) > 0:
					parts = line.split(':')
					action = parts[0]
					config = parts[1:]
					if config[0] == 'b':
						config = ('b', int(config[1]))
					elif config[0] == 'a':
						config = ('a', int(config[1]), config[2] == 'true')
					elif config[0] == 'h':
						config = ('h', int(config[1]), int(config[2]), config[3] == 'true')
					else:
						continue # ignore invalid file data
					self.configMapping[-1][action] = config
					self.alreadyConfigured = True # called redundantly, but want to make sure it's only invoked for non-empty files.
		
		print(self.configMapping[-1])
		
	def pushCleanConfig(self):
		self.configMapping.append({})
		self.taken.append({})
	
	def initialize(self):
		if not self.initialized:
			self.js.init()
			self.initialized = True
			self.axes = self.js.get_numaxes()
			self.hats = self.js.get_numhats()
			self.buttons = self.js.get_numbuttons()
	
	def popConfig(self):
		self.configMapping.pop()
		self.taken.pop()
	
	def flattenConfig(self):
		self.configMapping = self.configMapping[-1:]
		self.taken = self.taken[-1:]
	
	def saveConfig(self):
		config = self.configMapping[-1]
		output = []
		keys = list(config.keys())
		keys.sort()
		for key in keys:
			action = key
			binding = config[key]
			row = ':'.join(map(str, [action] + list(binding)))
			output.append(row)
		text = '\n'.join(output)
		writeTextFile('joystick-config-' + self.fingerprint + '.txt', text)
	
	def getBooleanState(self, action):
		if not self.initialized: self.initialize()
		binding = self.configMapping[-1].get(action)
		if binding != None:
			if binding[0] == 'b':
				output = self.js.get_button(binding[1])
			elif binding[0] == 'a':
				value = self.js.get_axis(binding[1])
				if binding[2]:
					output = value > .5
				else:
					output = value < -.5
			elif binding[0] == 'h':
				value = self.js.get_hat(binding[1])[binding[2]]
				if binding[3]:
					output = value > .5
				else:
					output =value < -.5
			else:
				output = False
		else:
			output = False
		
		self.knownState[action] = output
		return output
	
	def getButtonPreviousState(self, action):
		return self.knownState.get(action, False)
	
	def getAxis(self, actionNegative, actionPositive, noDead):
		getFloat = self.getFloatNoDeadZone if noDead else self.getFloatState
		negative = getFloat(actionNegative)
		positive = getFloat(actionPositive)
		
		if negative > positive:
			return -negative
		return positive
	
	def getFloatNoDeadZone(self, action):
		output = self.getFloatState(action)
		if output < 0.2: return 0.0
		return (output - 0.2) / 0.8
	
	def getFloatState(self, action):
		if not self.initialized: self.initialize()
		binding = self.configMapping[-1].get(action)
		if binding != None:
			if binding[0] == 'b':
				return 1.0 if self.js.get_button(binding[1]) else 0.0
			elif binding[0] == 'a':
				value = self.js.get_axis(binding[1])
				if binding[2]:
					return 1.0 * value if value > 0 else 0.0
				else:
					return -1.0 * value if value < 0 else 0.0
			elif binding[0] == 'h':
				value = self.js.get_hat(binding[1])[binding[2]]
				if binding[3]:
					return 1.0 * value if value > 0 else 0.0
				else:
					return -1.0 * value if value < 0 else 0.0
		return 0.0
	
	def configure(self, action):
		taken = self.taken[-1]
		config = self.configMapping[-1]
		
		for buttonIndex in range(self.buttons):
			if self.js.get_button(buttonIndex):
				key = 'b:' + str(buttonIndex)
				if not taken.get(key, False):
					taken[key] = True
					config[action] = ('b', buttonIndex)
					return True
		
		for hatIndex in range(self.hats):
			state = self.js.get_hat(hatIndex)
			for i in (0, 1):
				if abs(state[i]) > .25:
					isPositive = state[i] > 0
					key = 'h:' + str(hatIndex) + ':' + str(i) + ':' + ('+' if isPositive else '-')
					if not taken.get(key, False):
						taken[key] = True
						config[action] = ('h', hatIndex, i, isPositive)
						return True
		
		for axisIndex in range(self.axes):
			state = self.js.get_axis(axisIndex)
			if abs(state) > .25:
				isPositive = state > 0
				key = 'a:' + str(axisIndex) + ':' + ('+' if isPositive else '-')
				if not taken.get(key, False):
					taken[key] = True
					config[action] = ('a', axisIndex, isPositive)
					return True
		

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
		self.magicJumpPressed = False
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
	
	def applySystemEvents(self, events):
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


InputManager = InputManager_()
