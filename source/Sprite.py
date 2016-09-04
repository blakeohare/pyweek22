GRAVITY = .01
	
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
	
	def update(self, scene, dt):
		timeRatio = dt * FPS
		if self.dx != None:
			newX = self.x + self.dx * timeRatio
			self.tryMoveSprite(scene, newX, self.y, 0)
		
		if self.ground == None:
			self.vy += GRAVITY * timeRatio
			if self.vy < -.9 or self.vy > .9:
				self.vy = .9 if self.vy > 0 else -.9
			newY = self.y + self.vy
			self.tryMoveSprite(scene, self.x, newY, self.vy > 0)
	
	def tryMoveSprite(self, scene, newX, newY, isFalling):
		
		col = int(newX)
		rowBottom = int(newY)
		rowTop = int(newY - self.height * .75)
		
		if col < 0 or col >= scene.width:
			return
		if rowTop < 0 or rowBottom >= scene.height:
			return
		
		row = rowBottom
		while row >= rowTop:
			tile = scene.tiles[col][row]
			if tile.blocking:
				return
			row -= 1
			
		self.x = newX
		self.y = newY
		
	
	def render(self, screen, cameraX, cameraY):
		centerX = self.x * 64 - cameraX
		bottomY = self.y * 64 - cameraY
		
		pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(int(centerX - 32), int(bottomY - 64), 64, 64))
