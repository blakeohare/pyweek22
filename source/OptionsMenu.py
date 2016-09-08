class OptionsMenu(AbstractScene):
	def __init__(self, background):
		AbstractScene.__init__(self)
		self.background = background
		self.options = [
			('Return', 'return'),
			('Sound Options', 'sound'),
			('Keyboard Options', 'keyboard'),
			('Gamepad Options', 'gamepad'),
		]
		
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
				command = self.options[self.activeIndex][1]
				if command == 'return':
					self._next = self.background
					self.background._next = None
				elif command == 'gamepad':
					self._next = JoystickMenu(self)
				elif command == 'sound':
					print("Not implemented.")
				elif command == 'keyboard':
					print("Not implemented.")
		if InputManager.escapePressed:
			self._next = self.background
			self.background._next = None
			
	def render(self, screen):
		self.background.render(screen)
		
		left = SCREEN_WIDTH  // 4
		width = SCREEN_WIDTH // 2
		top = SCREEN_WIDTH // 8
		height = SCREEN_HEIGHT * 3 // 4
		renderRectangle(screen, (left, top, width, height), (0, 0, 0, 160))
		
		# TODO: center these with text render dry-run
		x = left + 80
		y = top + 30
		for i, option in enumerate(self.options):
			label = option[0]
			TextRenderer.render(screen, label, x, y)
			if i == self.activeIndex:
				pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x - 20, y, 10, 10))
			y += 60
		