def makeGrid(width, height):
	output = []
	while width > 0:
		width -= 1
		output.append([None] * height)
	return output
