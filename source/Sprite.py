GRAVITY = .01

ROW_COLLISION_CACHE = [False] * 1000

class Sprite:
	def __init__(self, template, x, y):
		self.type = type
		self.x = x + 0.0
		self.y = y + 0.0
		self.template = template
		self.dx = None
		self.dy = None
		self.vy = 0.0
		self.ground = None
		self.height = 1
		self.rowCollisionCache = None
	
	def render(self, screen, cameraX, cameraY):
		centerX = self.x * 64 - cameraX
		bottomY = self.y * 64 - cameraY
		
		pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(int(centerX - 32), int(bottomY - 64), 64, 64))
