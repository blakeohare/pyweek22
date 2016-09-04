	
class Sprite:
	def __init__(self, template, x, y):
		self.type = type
		self.x = x + 0.0
		self.y = y + 0.0
		self.template = template
	
	def render(self, screen, cameraX, cameraY):
		centerX = self.x * 64 - cameraX
		centerY = self.y * 64 - cameraY
		
		pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(int(centerX - 32), int(centerY - 32), 64, 64))
