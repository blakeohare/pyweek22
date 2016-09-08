
class JoystickWrapper:
	def __init__(self, index, actualJs):
		self.index = index
		self.js = actualJs
		self.name = actualJs.get_name()
		self.initialized = False
		self.axes = 0
		self.buttons = 0
		self.hats = 0
		self.configMapping = [{}]
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
				output = self.js.get_button(binding[1]) == 1
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
					output = value < -.5
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
