from pygame import *
from random import randint

init()

N,M=30,20
Scale=25
w,h=Scale*N,Scale*M
screen = display.set_mode((w,h))

Snake=[(5,5),(5,4),(5,3),(5,2),(5,1)]
Apple=[(23,6),(5,26),(3,16),(2,4)]
(R,L,U,D)=range(4)
d=R
def tick():
	if d==R: x=1;y=0;
	if d==L: x=-1;y=0;
	if d==U: x=0;y=-1;
	if d==D: x=0;y=1;
	t=Snake[0]
	t=(t[0]+x,t[1]+y)
	Snake.insert(0,t)
	del Snake[-1]
	NewApple()

def btn_press(btn):
	global d
	if btn==K_UP: d=U
	if btn==K_DOWN: d=D
	if btn==K_LEFT: d=L
	if btn==K_RIGHT: d=R

def SnakeDraw():
	for i in Snake:
		rect=(i[0]*Scale,i[1]*Scale,Scale-1,Scale-1)
		draw.rect(screen,(255,0,0),rect)

def NewApple():
	if Snake[0] in Apple:
		i=Apple.index(Snake[0])
		Apple[i]=(randint(0,N),randint(0,M))
		Snake.append(Snake[-1])

		
def AppleDraw():
	for i in Apple:
		rect=(i[0]*Scale,i[1]*Scale,Scale-1,Scale-1)
		draw.rect(screen,(0,255,0),rect)

screen.fill((255,255,250))


k=1
while k:
	screen.blit(FIELD,(0,0))
	k+=1
	if k%5==0:tick()
	SnakeDraw()
	AppleDraw()
	display.update()
	for e in event.get():
		if e.type == KEYDOWN:
			btn_press(e.key)
			if e.key==K_ESCAPE:k=0
			
