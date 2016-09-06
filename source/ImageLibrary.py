class ImageLibrary_:
	def __init__(self):
		self.images = {}
		self.imagesByScale = {}
	
	# TODO: colorkey magic
	def get(self, path):
		img = self.images.get(path)
		if img == None:
			rpath = ('images/' + path).replace('/', os.sep)
			reverse = False
			if '-east' in rpath or '-west' in rpath:
				if not os.path.exists(rpath):
					if '-east' in path:
						rpath = rpath.replace('-east', '-west')
					else:
						rpath = rpath.replace('-west', '-east')
					reverse = True
				
			img = pygame.image.load(rpath)
			if reverse:
				if self.images.get(rpath) == None:
					self.images[rpath.replace('\\', '/')] = img
				img = pygame.transform.flip(img, True, False)
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
