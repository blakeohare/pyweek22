class JoystickMenu:
	def __init__(self, background):
		self._next = None
		self.background = background
		self.options = [
			('Back', 'back'),
			('Configure Active Gamepad', 'config'),
			('No Gamepad Selected', 'none')
		]
		
		for i, joystick in enumerate(InputManager.getJoysticks()):
			self.options.append((joystick.name, 'select:' + str(i)))
		
		self.activeIndex = 0
	
	def update(self):
		for event in InputManager.getMenuEvents():
			if event == 'up':
				if self.activeIndex > 0:
					self.activeIndex -= 1
			elif event == 'down':
				if self.activeIndex < len(self.options) - 1:
					self.activeIndex += 1
			elif event == 'enter':
				option = self.options[self.activeIndex][1]
				if option == 'back':
					self._next = self.background
					self.background._next = None
				elif option == 'config':
					js = InputManager.getActiveJoystick()
					if js != None:
						self._next = JoystickConfigMenu(self, js)
				elif option == 'none':
					InputManager.clearActiveJoystick()
				else:
					parts = option.split(':')
					if parts[0] == 'select':
						index = int(parts[1])
						InputManager.setActiveJoystick(index)
					
		
		if InputManager.escapePressed:
			self._next = self.background
			self.background._next = None
		
	def render(self, screen):
		self.background.render(screen)
		
		renderRectangle(screen, (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200), (0, 0, 0, 128))
		
		TextRenderer.render(screen, "Gamepad Options", 110, 110)
		
		x = 200
		y = 200
		for i, option in enumerate(self.options):
			command = option[1].split(':')
			label = option[0]
			if self.activeIndex == i:
				pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x - 20, y, 10, 10))
			TextRenderer.render(screen, label, x, y)
			y += 50
			
			