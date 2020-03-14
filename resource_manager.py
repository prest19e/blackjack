import os, pygame

from typing import Tuple
from logic import Card


class ResourceManager():
	bg_image: pygame.Surface = pygame.image.load(os.path.join('resources', 'background.jpg'))
	icon_image: pygame.Surface = pygame.image.load(os.path.join('resources', 'icon.png'))

	def get_background_surface(self, resolution: Tuple[int, int]) -> pygame.Surface:
		return pygame.transform.scale(self.bg_image.convert(), resolution)

	def get_icon_surface(self) -> pygame.Surface:
		return self.icon_image.convert_alpha()

	@staticmethod
	def get_card_surface(card: Card, resolution: Tuple[int, int]) -> pygame.Surface:
		card_file = "card" + card.suit + card.rank + ".png"
		img = pygame.image.load(os.path.join('resources', 'cards', card_file)).convert()
		return pygame.transform.scale(img, resolution)
