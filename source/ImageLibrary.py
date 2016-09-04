class ImageLibrary_:
	def __init__(self):
		self.images = {}
		self.imagesByScale = {}
	
	def get(self, path):
		img = self.images.get(path)
		if img == None:
			img = pygame.image.load(('images/' + path).replace('/', os.sep))
			self.images[path] = img
		return img
	
	def getAtScale(self, path, scale):
		scaleKey = int(scale * 1000)
		lookup = self.imagesByScale.get(scaleKey)
		if lookup == None:
			lookup = {}
			self.imagesByScale[scaleKey] = lookup
		img = lookup.get(path)
		if img == None:
			img = self.get(path)
			width, height = img.get_size()
			width = int(width * scale)
			height = int(height * scale)
			img = pygame.transform.scale(img, (width, height))
			lookup[path] = img
		
		return img

ImageLibrary = ImageLibrary_()
