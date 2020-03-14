import pygame
from pygame.locals import *

pygame.font.init()
PYGAME_STANDART_FONT = pygame.font.Font('freesansbold.ttf', 14)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (64, 64, 64)
GRAY = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)


class Button(object):
	def __init__(self, rect=None, caption='', background_color=LIGHTGRAY, foreground_color=BLACK, font=None, normal=None, down=None, highlight=None):
		if rect is None:
			self._rect = pygame.Rect(0, 0, 30, 60)
		else:
			self._rect = pygame.Rect(rect)

		self._caption = caption
		self._background_color = background_color
		self._foreground_color = foreground_color

		if font is None:
			self._font = PYGAME_STANDART_FONT
		else:
			self._font = font

		self.buttonDown = False
		self.mouseOverButton = False
		self.lastMouseDownOverButton = False
		self._visible = True
		self.customSurfaces = False

		if normal is None:
			self.surfaceNormal = pygame.Surface(self._rect.size)
			self.surfaceDown = pygame.Surface(self._rect.size)
			self.surfaceHighlight = pygame.Surface(self._rect.size)
			self._update()
		else:
			self.set_surfaces(normal, down, highlight)

	def handle_click(self, event):
		if event.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
			return []

		ret_val = []

		has_exited = False
		if not self.mouseOverButton and self._rect.collidepoint(event.pos):
			self.mouseOverButton = True
			ret_val.append('enter')
		elif self.mouseOverButton and not self._rect.collidepoint(event.pos):

			has_exited = True

		if self._rect.collidepoint(event.pos):
			if event.type == MOUSEMOTION:
				ret_val.append('move')
			elif event.type == MOUSEBUTTONDOWN:
				self.buttonDown = True
				self.lastMouseDownOverButton = True
				ret_val.append('down')
		else:
			if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
				self.lastMouseDownOverButton = False

		do_mouse_click = False
		if event.type == MOUSEBUTTONUP:
			if self.lastMouseDownOverButton:
				do_mouse_click = True
			self.lastMouseDownOverButton = False

			if self.buttonDown:
				self.buttonDown = False
				ret_val.append('up')

			if do_mouse_click:
				self.buttonDown = False
				ret_val.append('click')

		if has_exited:
			ret_val.append('exit')

		return ret_val

	def draw(self, surface_obj):
		if self._visible:
			if self.buttonDown:
				surface_obj.blit(self.surfaceDown, self._rect)
			elif self.mouseOverButton:
				surface_obj.blit(self.surfaceHighlight, self._rect)
			else:
				surface_obj.blit(self.surfaceNormal, self._rect)

	def _update(self):
		if self.customSurfaces:
			self.surfaceNormal = pygame.transform.smoothscale(self.original_surface_normal, self._rect.size)
			self.surfaceDown = pygame.transform.smoothscale(self.original_surface_down, self._rect.size)
			self.surfaceHighlight = pygame.transform.smoothscale(self.original_surface_highlight, self._rect.size)
			return

		w = self._rect.width
		h = self._rect.height

		self.surfaceNormal.fill(self.bgcolor)
		self.surfaceDown.fill(self.bgcolor)
		self.surfaceHighlight.fill(self.bgcolor)

		caption_surface = self._font.render(self._caption, True, self.fgcolor, self.bgcolor)
		caption_rect = caption_surface.get_rect()
		caption_rect.center = int(w / 2), int(h / 2)
		self.surfaceNormal.blit(caption_surface, caption_rect)
		self.surfaceDown.blit(caption_surface, caption_rect)

		pygame.draw.rect(self.surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)
		pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (w - 2, 1))
		pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (1, h - 2))
		pygame.draw.line(self.surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
		pygame.draw.line(self.surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
		pygame.draw.line(self.surfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
		pygame.draw.line(self.surfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))

		pygame.draw.rect(self.surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1)
		pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (w - 2, 1))
		pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (1, h - 2))
		pygame.draw.line(self.surfaceDown, DARKGRAY, (1, h - 2), (1, 1))
		pygame.draw.line(self.surfaceDown, DARKGRAY, (1, 1), (w - 2, 1))
		pygame.draw.line(self.surfaceDown, GRAY, (2, h - 3), (2, 2))
		pygame.draw.line(self.surfaceDown, GRAY, (2, 2), (w - 3, 2))

		self.surfaceHighlight = self.surfaceNormal

	def set_surfaces(self, normal_surface, down_surface=None, highlight_surface=None):
		if down_surface is None:
			down_surface = normal_surface
		if highlight_surface is None:
			highlight_surface = normal_surface

		if type(normal_surface) == str:
			self.original_surface_normal = pygame.image.load(normal_surface)
		if type(down_surface) == str:
			self.original_surface_down = pygame.image.load(down_surface)
		if type(highlight_surface) == str:
			self.original_surface_highlight = pygame.image.load(highlight_surface)

		if self.original_surface_normal.get_size() != self.original_surface_down.get_size() != self.original_surface_highlight.get_size():
			raise Exception('foo')

		self.surfaceNormal = self.original_surface_normal
		self.surfaceDown = self.original_surface_down
		self.surfaceHighlight = self.original_surface_highlight
		self.customSurfaces = True
		self._rect = pygame.Rect(
			(self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))

	def _propGetCaption(self):
		return self._caption

	def _propSetCaption(self, captionText):
		self.customSurfaces = False
		self._caption = captionText
		self._update()

	def _propGetRect(self):
		return self._rect

	def _propSetRect(self, newRect):
		self._update()
		self._rect = newRect

	def _propGetVisible(self):
		return self._visible

	def _propSetVisible(self, setting):
		self._visible = setting

	def _propGetFgColor(self):
		return self._foreground_color

	def _propSetFgColor(self, setting):
		self.customSurfaces = False
		self._foreground_color = setting
		self._update()

	def _propGetBgColor(self):
		return self._background_color

	def _propSetBgColor(self, setting):
		self.customSurfaces = False
		self._background_color = setting
		self._update()

	def _propGetFont(self):
		return self._font

	def _propSetFont(self, setting):
		self.customSurfaces = False
		self._font = setting
		self._update()

	caption = property(_propGetCaption, _propSetCaption)
	rect = property(_propGetRect, _propSetRect)
	visible = property(_propGetVisible, _propSetVisible)
	fgcolor = property(_propGetFgColor, _propSetFgColor)
	bgcolor = property(_propGetBgColor, _propSetBgColor)
	font = property(_propGetFont, _propSetFont)
