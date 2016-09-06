def main():
	
	fps = 60
	
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	
	scene = PlayScene()
	
	myEvents = []
	
	pressed = {}
	
	i = 0
	
	while True:
		start = time.time()
		
		i += 1
		
		InputManager.applySystemEvents(pygame.event.get())
		if InputManager.quitAttempted:
			return
		
		screen.fill((0, 0, 0))
		
		scene.update()
		scene.render(screen)
		
		if scene._next != None:
			scene = scene._next

		pygame.display.flip()
		end = time.time()
		
		diff = end - start
		delay = 1.0 / fps - diff
		if delay > 0:
			time.sleep(delay)
		else:
			print("Dropping frames!")

main()
