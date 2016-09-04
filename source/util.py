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
	output = []
	for line in readTextResource(path).split('\n'):
		line = line.strip()
		if len(line) > 0:
			output.append(line)
	return output
