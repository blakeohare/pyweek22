class JoystickConfigMenu:
	def __init__(self, background, joystick):
		self._next = None
		self.background = background
		self.joystick = joystick
		self.currentIndex = 0
		self.initialized = False
		self.buttons = [
			'move-left',
			'move-right',
			'move-up',
			'move-down',
			'a',
			'b',
			'x',
			'y',
			'start',
			'trigger']
	
	def update(self):
		if not self.initialized:
			self.joystick.initialize()
			self.joystick.pushCleanConfig()
			self.initialized = True
		
		if InputManager.escapePressed:
			self.joystick.popConfig()
			self._next = self.background
			self.background._next = None
			
		if self.currentIndex >= len(self.buttons):
			self.joystick.flattenConfig()
			self.joystick.saveConfig()
			self._next = self.background
			self.background._next = None
		else:
			current = self.buttons[self.currentIndex]
			if self.joystick.configure(current):
				self.currentIndex += 1
	
	def render(self, screen):
		self.background.render(screen)
		renderRectangle(screen, (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200), (0, 0, 0, 180))
		
		if self.currentIndex < len(self.buttons):
			current = self.buttons[self.currentIndex]
			TextRenderer.render(screen, current, 200, 200)
		