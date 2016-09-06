def makeGrid(width, height):
	output = []
	while width > 0:
		width -= 1
		output.append([None] * height)
	return output

def readTextResource(path):
	c = open(path.replace('/', os.sep), 'rt')
	text = c.read()
	c.close()
	
	text = text.replace('\r\n', '\n').replace('\r', '\n')
	return text

def readTextResourceLines(path):
	path = path.replace('/', os.sep)
	output = []
	for line in readTextResource(path).split('\n'):
		line = line.strip()
		if len(line) > 0:
			output.append(line)
	return output

def writeTextFile(filename, content):
	filename = filename.replace('/', os.sep)
	c = open(filename, 'wt')
	c.write(content)
	c.close()

def readFileMaybe(filename):
	filename = filename.replace('/', os.sep)
	if not os.path.exists(filename): return None
	if os.path.isdir(filename): return None
	c = open(filename, 'rt')
	text = c.read()
	c.close()
	return text
		
	
_tempRect = [None]
def renderRectangle(screen, position, color):
	if len(color) == 3 or color[3] == 255: return pygame.draw.rect(screen, color, position)
	
	x, y, width, height = position
	r, g, b, alpha = color
	if alpha == 0: return
	
	surface = _tempRect[0]
	if surface == None:
		surface = pygame.Surface((width, height)).convert()
		_tempRect[0] = surface
	elif surface.get_width() < width or surface.get_height() < height:
		newWidth = max(width, surface.get_width())
		newHeight = max(height, surface.get_height())
		surface = pygame.Surface((newWidth, newHeight)).convert()
		_tempRect[0] = surface
	pygame.draw.rect(surface, (r, g, b), pygame.Rect(0, 0, width, height))
	surface.set_alpha(alpha)
	screen.blit(surface, pygame.Rect(x, y, width, height), pygame.Rect(0, 0, width, height))

def computeMD5(string):
	try:
		import md5
		m = md5.new()
		m.update(string)
	except:
		import hashlib
		m = hashlib.md5()
		m.update(string.encode('latin-1'))
	return m.hexdigest()