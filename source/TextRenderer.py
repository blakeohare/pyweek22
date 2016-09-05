class TextRenderer_:
	def __init__(self):
		self.images = None
		
	
	def initialize(self):
		self.images = {
			'@': 'at',
			'&': 'ampersand',
			"'": 'apostrophe',
			'*': 'asterisk',
			'\\': 'backslash',
			'`': 'backtick',
			'!': 'bang',
			'}': 'close_brace',
			']': 'close_bracket',
			')': 'close_paren',
			':': 'colon',
			',': 'comma',
			'=': 'equals',
			'^': 'exp',
			'#': 'hash',
			'-': 'hyphen',
			'<': 'lessthan',
			'$': 'moneys',
			'{': 'open_brace',
			'[': 'open_bracket',
			'(': 'open_paren',
			'%': 'percentage',
			'.': 'period',
			'|': 'pipe',
			'+': 'plus',
			'?': 'question',
			'"': 'quote',
			';': 'semicolon',
			'/': 'slash',
			'~': 'tilde',
			'_': 'underscore',
		}
		
		for letter in 'abcdefghijklmnopqrstuvwxyz':
			self.images[letter.upper()] = letter + '_upper'
			self.images[letter.lower()] = letter + '_lower'
		for i in range(10):
			self.images[str(i)] = 'num_' + str(i)
		
		
		for key in self.images.keys():
			self.images[key] = ImageLibrary.getAtScale('text/' + self.images[key] + '.png', 2)
		
		self.spaceWidth = self.images.get('v').get_width()
	
	def render(self, screen, text, x, y, xyOut = None):
		if self.images == None: self.initialize()
		
		imagesGet = self.images.get
		
		for c in text:
			if c == ' ':
				x += self.spaceWidth
			else:
				img = imagesGet(c)
				screen.blit(img, (x, y))
				x += img.get_width()
		
		if xyOut != None:
			while len(xyOut) < 2: xyOut.append(0)
			xyOut[0] = x
			xyOut[1] = imagesGet('X').get_height()
		return xyOut
		
		
TextRenderer = TextRenderer_()
