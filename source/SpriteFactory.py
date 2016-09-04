
class SpriteFactory_:
	def __init__(self):
		self.types = {}
	
	def makeSprite(self, type, x, y):
		template = self.types.get(type)
		if template == None:
			template = SpriteTemplate(type)
			self.types[type] = template
		return Sprite(template, x, y)

SpriteFactory = SpriteFactory_()
	