#! /usr/bin/env python
# coding: utf-8
import pygame, sys, os, math, random, time
from PIL import Image, ImageDraw
from pygame.locals import *
pygame.init()

#~ if there is an argument, generate so many images
if len(sys.argv) > 1:
	try:
		times = int(sys.argv[1])
	except:
		times = 1
else:
	times = 1

#~ set resolution for the result image
resx = 210 * 5	#~ for A4 paper sheet
resy = 295 * 5
#~ resx = 600		#~ for quick tests
#~ resy = 400

lines = int(resx * resy / 120.0)	#~ lines quantity per frame
frames_q = 3						#~ frames quantity
max_line_len = 64					#~ length limit for lines
delay = 350
#~ pygame stuff
window = pygame.display.set_mode((resx, resy))
screen = pygame.display.get_surface()

def print_text(text, xx, yy, color, font_name = 'Sans'):
	font = pygame.font.SysFont(font_name, 22)
	ren = font.render(text, 1, color)
	screen.blit(ren, (xx, yy))
def print_message(text):
	print(text)
	print_text(text, 20, 20, (205, 255, 205))
	pygame.display.flip()
def draw_lines(max_lngth):
	q_max_lngth = 0		#~ quantity of lines with max length
	needed_lines_q = 0
	while needed_lines_q < lines:
		x1 = int( random.random() * resx )
		y1 = int( random.random() * resy )
		x2 = int( random.random() * resx )
		y2 = int( random.random() * resy )
		#~ calculate the length of a line (x1,y1),(x2,y2)
		lngth = math.sqrt( math.fabs( (x1-x2)**2 + (y1-y2)**2 ) )
		#~ if the length is too big, skip that line
		if lngth > max_lngth:
			q_max_lngth += 1
			continue
		start = (x1,y1)
		end = (x2,y2)
		pygame.draw.aaline(screen, (200,200,200), start, end, 2)
		needed_lines_q += 1
		#~ pygame.display.flip()	#~ comment it for faster work and lesser effects
	return q_max_lngth

im_filenames = tuple('screen{}.png'.format(cn) for cn in range(frames_q))

#~ main cycle
for main_cn in range(times):
		#~ creating frames with random lines, saving it as 'screenX.png'
	message = 'Image {}, stage 1/5...'.format(main_cn+1)
	print(message)
	for cn in range(frames_q):
		q_lines_drawing = draw_lines(max_line_len)
		pygame.image.save(screen, im_filenames[cn])
		#~ print the progress
		#~ message = 'Image {}, stage {}/5 done. Processing stage {}...'.format(main_cn+1, cn+1, cn+2)
		message = 'Image {}, stage {}/5...'.format(main_cn+1, cn+2)
		print_message(message)
		screen.fill((0,0,0), special_flags=0)

		#~ frame 2, invert and half-opacity
	image = Image.open(im_filenames[2])
	image = image.convert('RGBA')
	draw = ImageDraw.Draw(image)
	pix = image.load()
	for i in range(resx):
		for j in range(resy):
			a = pix[i, j][0]
			b = pix[i, j][1]
			c = pix[i, j][2]
			d = pix[i, j][3]
			draw.point((i, j), (255-a, 255-b, 255-c, d/2))
	image.save(im_filenames[2], 'PNG')
		#~ print the progress
	#~ message = 'Image {}, stage 4/5 done. Processing stage 5...'.format(main_cn+1)
	message = 'Image {}, stage 5/5...'.format(main_cn+1)
	print_message(message)
	del draw

		#~ frame 1, invert and transform whiting into transparansy
	image = Image.open(im_filenames[1])
	image = image.convert('RGBA')
	draw = ImageDraw.Draw(image)
	pix = image.load()
	screen.fill((0,0,0), special_flags=0)
	for i in range(resx):
		for j in range(resy):
			a = pix[i, j][0]
			b = pix[i, j][1]
			c = pix[i, j][2]
			d = pix[i, j][3]
			draw.point((i, j), (255-a, 255-b, 255-c, d-(a+b+c)/3))
	image.save(im_filenames[1], 'PNG')
	del draw

		#~ merge our frames
	im = []
	for cn in range(frames_q):
		im.append( pygame.image.load(im_filenames[cn]) )
		screen.blit(im[cn], (0, 0))
		pygame.display.flip()
		pygame.time.wait(delay)
	res_filename = 'res{}.png'.format(time.time())
	pygame.image.save(screen, res_filename)

		#~ delete temp files
	for x in im_filenames:
		os.remove(x)
	print('{} is generated.'.format(res_filename))
	screen.fill((0,0,0), special_flags=0)
	pygame.display.flip()
exit(0)
