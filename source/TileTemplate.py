class TileTemplate:
	def __init__(self, id, images, flags):
		self.blocking = True
		self.bar = False
		self.inclineType = None
		self.animationSpeedRatio = 1.0 # TODO: flags to modify this
		
		for flag in flags:
			if flag == 'B':
				self.bar = True
				self.blocking = False # for most purposes (3 out of 4 directions) this is not blocking. 
			elif flag == 'P':
				self.blocking = False
			elif flag == '-':
				pass
			elif flag == '/':
				self.inclineType = 'up'
			elif flag == '\\':
				self.inclineType = 'down'
			else:
				raise Exception("Unknown tile flag: " + flag)
		
		self.isIncline = self.inclineType != None
		self.images = images
		self.staticImage = None
		if len(self.images) == 1:
			self.staticImage = self.images[0]
