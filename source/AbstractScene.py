class AbstractScene:
	def __init__(self):
		self._next = None
		self.isPlayScene = False
	
	def update(self):
		raise Exception("Override me.")
	
	def render(self, screen):
		raise Exception("Override me.")
