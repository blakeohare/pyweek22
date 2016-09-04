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
	
	def update(self, scene, dt):
		pass
	
	def render(self, screen, cameraOffsetX, cameraOffsetY):
		centerX = self.x * 32 + cameraOffsetX
		bottomY = self.y * 32 + cameraOffsetY
		left = int(centerX - 16)
		top = int(bottomY - 32)
		pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(left, top, 32, 32))
