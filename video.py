import threading
import pygame
import Queue
import os
from textwrap import *
from pygame import time

SLIDE = '__SLIDE__'

import settings
if settings.CAMERA:
	from pygame import camera

class Video(threading.Thread):
	def __init__(self, logger, queue, parent_queue):
		threading.Thread.__init__(self)
		self.logger = logger
		self.logger.debug("Creating video...")
		self.queue = queue
		self.parent_queue = parent_queue
		self.is_slide = False
		self.slide = None

		self.text = "Welcome!"

		# Setup screen
		pygame.init()
		self.clock = time.Clock();
		pygame.mouse.set_visible(False)
		self.width = settings.SCREEN_WIDTH
		self.height = settings.SCREEN_HEIGHT
		flags = 0 #pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
		self.screen = pygame.display.set_mode((self.width, self.height), flags)
		font_size = settings.FONT_SIZE
		self.font = pygame.font.SysFont(settings.FONT, font_size, bold=1)


		if settings.CAMERA:
			camera.init()
			camera_size = (640,480)
			self.c = camera.Camera('/dev/video0', camera_size)
			self.c.start()
			self.surface = pygame.Surface(camera_size)
		self.bigSurface = None
		self.alert = False

		self.foregroundColor = pygame.Color(settings.FONT_COLOR)
		self.backgroundColor = pygame.Color(settings.BACKGROUND_COLOR)
		self.black = pygame.Color(0, 0, 0, 100)
		self.shadowShade = 0

		self.background_image = None
		if settings.BACKGROUND_IMAGE:
			self.background_image = pygame.image.load(settings.BACKGROUND_IMAGE)
		self.logger.debug("Video created")

	def blit_background(self):
		if not self.alert:
			if settings.CAMERA:
				if self.c.query_image():
					self.c.get_image(self.surface)
					self.surface = pygame.transform.flip(self.surface, True, False)
					self.bigSurface = pygame.transform.scale(self.surface, (self.width, self.height))
			else:
				self.bigSurface = pygame.Surface((self.width, self.height))
				self.bigSurface.fill(self.backgroundColor)

		if self.bigSurface != None:
			self.screen.blit(self.bigSurface, (0,0))

		if self.background_image:
			self.screen.blit(self.background_image, (0,0))

		if self.is_slide:
			self.screen.blit(self.slide, (0,0))
		
	def truncline(self, text, font, maxwidth):
		"""Truncates a single line of text to given pixel size."""
		real=len(text)
		stext=text
		l=font.size(text)[0]
		a=0
		done=1
		while l > maxwidth: 
			a=a+1
			stext=text.rsplit(None, a)[0]
			l=font.size(stext)[0]
			real=len(stext)
			done=0
		return real, done, stext
			
	def wrapline(self, text, font, maxwidth):
		"""Wraps text line by word by word into multiple lines to fit given pixel size."""
		done=0
		wrapped=[]
		
		while not done: 
			nl, done, stext=self.truncline(text, font, maxwidth)
			wrapped.append(stext.strip())
			text=text[nl:]
		return wrapped

	def run(self):
		while True:
			# Set frame rate
			self.clock.tick(30)
			try:
				try:
					msg = self.queue.get_nowait()
					priority = msg[0]
					line1 = msg[1]
					line2 = msg[2]
					self.is_slide = line2 == SLIDE
					if self.is_slide:
						filename = line1
						self.slide = pygame.image.load(filename)

					self.alert = msg[3]
					self.text = line1 + ' ' + line2
					self.queue.task_done()
					t0 = time.get_ticks()
				except Queue.Empty:
					False
					#self.logger.debug("Video queue empty")

				self.blit_background()

				if not self.is_slide and self.text != None:
					wrapped_text = self.wrapline(self.text, self.font, self.width)
					# center text vertically
					start_y = (self.height - (len(wrapped_text) * self.font.get_linesize())) / 2 
					if self.alert:
						if settings.TEXT_EFFECT == 'blink':
							for index, line in enumerate(wrapped_text):
								textSurface = self.font.render(line, True, self.foregroundColor)
								self.shadowShade = (self.shadowShade + 3) % 255
								shadowColor = pygame.Color(self.shadowShade, self.shadowShade, self.shadowShade)
								shadow = self.font.render(line, True, shadowColor)
								pos = (1, start_y + index * self.font.get_linesize())
								shadowOffset = 3
								self.screen.blit(shadow, (pos[0]+shadowOffset, pos[1]+shadowOffset))
								self.screen.blit(textSurface, pos)
						elif settings.TEXT_EFFECT == 'type':
							t0 = time.get_ticks()
							self.blit_background()
							for index, line in enumerate(wrapped_text):
								for caret in range(len(line)):
									current_part = line[0:caret+1]
									textSurface = self.font.render(current_part, True, self.foregroundColor)
									shadowColor = self.black
									shadow = self.font.render(current_part, True, shadowColor)
									pos = (1, start_y + index * self.font.get_linesize())
									shadowOffset = 3
									self.screen.blit(shadow, (pos[0]+shadowOffset, pos[1]+shadowOffset))
									self.screen.blit(textSurface, pos)
									pygame.display.update()
									time.wait(80)						
							while(t0 + settings.ALERT_DISPLAY_TIME*1000 - time.get_ticks() > 0):
								# keep the display updated while we wait
								pygame.display.update()
								self.clock.tick(30)
					else:
						for index, line in enumerate(wrapped_text):
							textSurface = self.font.render(line, True, self.foregroundColor)
							width = textSurface.get_width()
							shadowColor = self.black
							shadow = self.font.render(line, True, shadowColor)
							pos = ((self.width - width)/2, start_y + index * self.font.get_linesize())
							shadowOffset = 3
							self.screen.blit(shadow, (pos[0]+shadowOffset, pos[1]+shadowOffset))
							self.screen.blit(textSurface, pos)


				pygame.display.update()
				
				for event in pygame.event.get():
					if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key ==pygame.K_q:
						self.logger.info("EXIT")
						pygame.quit()
						os._exit(0)
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_t:
							msg = [1, settings.FAKE_TWEET, "", True]
							self.parent_queue.put(msg)
			except Exception as e:
				self.logger.exception("Exception in video: " + str(e))

