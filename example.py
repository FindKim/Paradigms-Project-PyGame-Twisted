import pygame, random, sys
from pygame.locals import *

xs = [290, 290, 290, 290, 290];ys = [290, 270, 250, 230, 210];dirs = 0;score = 0;applepos = (random.randint(0, 590), random.randint(0, 590));pygame.init();s=pygame.display.set_mode((600, 600));pygame.display.set_caption('Snake');appleimage = pygame.Surface((10, 10));appleimage.fill((0, 255, 0));img = pygame.Surface((20, 20));img.fill((255, 0, 0));f = pygame.font.SysFont('Arial', 20);clock = pygame.time.Clock()
while True:
	clock.tick(10)
	for e in pygame.event.get():
		if e.type == QUIT:
			sys.exit(0)
		elif e.type == KEYDOWN:
			if e.key == K_UP and dirs != 0:dirs = 2
			elif e.key == K_DOWN and dirs != 2:dirs = 0
			elif e.key == K_LEFT and dirs != 1:dirs = 3
			elif e.key == K_RIGHT and dirs != 3:dirs = 1
	i = len(xs)-1
	while i >= 1:
		xs[i] = xs[i-1];ys[i] = ys[i-1];i -= 1
	if dirs==0:ys[0] += 20
	elif dirs==1:xs[0] += 20
	elif dirs==2:ys[0] -= 20
	elif dirs==3:xs[0] -= 20	
	s.fill((255, 255, 255))	
	for i in range(0, len(xs)):
		s.blit(img, (xs[i], ys[i]))
	s.blit(appleimage, applepos);t=f.render(str(score), True, (0, 0, 0));s.blit(t, (10, 10));pygame.display.update()
					
					
			


