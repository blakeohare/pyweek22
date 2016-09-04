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
	
	def render(self, screen, cameraOffsetX, cameraOffsetY):
		centerX = self.x * 64 + cameraOffsetX
		bottomY = self.y * 64 + cameraOffsetY
		
		pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(int(centerX - 32), int(bottomY - 64), 64, 64))

class Projectile:
	def __init__(self, x, y, vx, vy, color, size):
		self.color = color
		self.size = size
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
	
	def update(self, scene):
		self.x += self.vx
		self.y += self.vy
	
	def renderFirstPass(self, screen):
		pass
	
	def renderSecondPass(self, screen, cameraOffsetX, cameraOffsetY):
		x = int(self.x * 64 + cameraOffsetX)
		y = int(self.y * 64 + cameraOffsetY)
		s = self.size
		left = x - s
		top = y - s
		pygame.draw.ellipse(screen, self.color, (left, top, 2 * s, 2 * s))
		