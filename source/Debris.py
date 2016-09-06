
class Debris:
	# dissipation values:
	# - grow-and-fade --> grows while losing opacity
	def __init__(self, x, y, color, dissipation):
		self.x = x
		self.y = y
		self.color = list(color) + [255]
		self.dead = False
		self.dissipation = dissipation
		self.lifetime = 0
		self.vx = 0.0
		self.vy = 0.0
		self.width = 4.0
		self.alpha = 255
		
	
	def update(self, scene, timeRatio):
		self.x += self.vx * timeRatio
		self.y += self.vy * timeRatio
		if self.dissipation == 'grow-and-fade':
			self.width += timeRatio / 3.0
			alpha = int(255 * (1.0 - self.lifetime / 30.0))
			if alpha < 0 or alpha > 255:
				alpha = max(0, min(255, alpha))
			self.alpha = alpha
			if self.lifetime > 30:
				self.dead = True
		self.lifetime += timeRatio
	
	def render(self, screen, cameraOffsetX, cameraOffsetY, rtInt):
		left = int(self.x * 32 + cameraOffsetX - self.width / 2 + .5)
		top = int(self.y * 32 + cameraOffsetY - self.width / 2 + .5)
		right = left + int(self.width + .5)
		bottom = top + int(self.width + .5)
		if right < 0 or bottom < 0 or left >= SCREEN_WIDTH or top >= SCREEN_HEIGHT: return
		self.color[3] = self.alpha
		renderRectangle(screen, (left, top, right - left, bottom - top), self.color)
