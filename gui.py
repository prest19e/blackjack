import pygame

from button import Button
from logic import Game
from resource_manager import ResourceManager
from consts import *
from typing import Tuple


class App:
    window_h: int = WINDOWS_HEIGHT
    window_w: int = WINDOWS_WIDTH
    window_size: Tuple[int, int] = (window_w, window_h)
    display_surface: pygame.Surface = pygame.display.set_mode(window_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    is_running: bool = True
    is_started: bool = False
    resources: ResourceManager = None
    clock = pygame.time.Clock()
    game: Game = Game()

    def __init__(self):
        self.button_rise = Button((700, 377, 140, 40), "Удвоить")
        self.button_restart = Button((550, 377, 140, 40), "Заново")
        self.button_stand = Button((700, 327, 140, 40), "Уйти")
        self.button_hit = Button((700, 277, 140, 40), "Играть")
        self.button_dec_bet = Button((550, 327, 140, 40), "Опустить ставку")
        self.button_inc_bet = Button((550, 277, 140, 40), "Поднять ставку", )

    def start(self):
        self.resources = ResourceManager()

        pygame.display.set_caption("Проект ПП: Блэкджек")
        pygame.display.set_icon(self.resources.get_icon_surface())

        while self.is_running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.clock.tick(FPS)
            self.render()
            pygame.display.flip()
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if not self.is_started:
                self.is_started = True

        if 'click' in self.button_inc_bet.handle_click(event) and self.game.is_playing == True:
            self.game.inc_bet()

        if 'click' in self.button_dec_bet.handle_click(event) and self.game.is_playing == True:
            self.game.dec_bet()

        if 'click' in self.button_hit.handle_click(event) and self.game.is_playing == True:
            self.game.hit()

        if 'click' in self.button_stand.handle_click(event) and self.game.is_playing == True:
            self.game.stand()

        if 'click' in self.button_rise.handle_click(event) and self.game.is_playing == True:
            self.game.rise()

        if 'click' in self.button_restart.handle_click(event):
            self.game.restart()

    def render(self):
        self.display_surface.blit(self.resources.get_background_surface(self.window_size), (0, 0))

        if not self.is_started:
            self.show_welcome_msg("Проект по ПП: Блэкджек", "Студент группы ИДБ-18-09 Жиленко Андрей",
                                  "Нажмите ЛКМ, чтобы продолжить")
        else:
            self.show_player_cards()
            self.show_player_hand_cost()
            self.show_player_bank()
            self.show_player_bet()
            self.show_dealer_cards()
            self.show_dealer_hand_cost()
            self.show_status()

            self.button_inc_bet.draw(self.display_surface)
            self.button_dec_bet.draw(self.display_surface)
            self.button_hit.draw(self.display_surface)
            self.button_stand.draw(self.display_surface)
            self.button_rise.draw(self.display_surface)
            self.button_restart.draw(self.display_surface)

    def show_welcome_msg(self, title: str, who: str, action: str):
        font = pygame.font.SysFont(TEXT_FONT_FAMILY, TEXT_SIZE, TEXT_MOD)

        self.display_surface.blit(font.render(title, 1, TEXT_COLOR), (50, 50))
        self.display_surface.blit(font.render(who, 1, TEXT_COLOR), (50, 100))
        self.display_surface.blit(font.render(action, 1, TEXT_COLOR), (50, 150))

    def show_player_cards(self):
        offset = 0
        for card in self.game.player.hand.cards:
            card_image = self.resources.get_card_surface(card, (140, 190))
            self.display_surface.blit(card_image, (20 + offset, 60))
            offset += 33

    def show_player_hand_cost(self):
        self.print_text("Игрок: " + str(self.game.player.hand.cost), 20, 7)

    def show_player_bank(self):
        self.print_text("Ваш банк: " + str(self.game.player.bank.total_money), 20, 277)

    def show_player_bet(self):
        self.print_text("Ваша ставка: " + str(self.game.player.bank.bet), 20, 311)

    def show_dealer_cards(self):
        offset = 0
        for card in self.game.dealer.hand.cards:
            card_image = self.resources.get_card_surface(card, (140, 190))
            self.display_surface.blit(card_image, (550 + offset, 60))
            offset += 33

    def show_dealer_hand_cost(self):
        self.print_text("Дилер: " + str(self.game.dealer.hand.cost), 550, 7)

    def print_text(self, text: str, x: int, y: int):
        font = pygame.font.SysFont(TEXT_FONT_FAMILY, TEXT_SIZE, TEXT_MOD)
        rendered_text = font.render(text, 1, TEXT_COLOR)

        self.display_surface.blit(rendered_text, (x, y))

    def show_status(self):
        self.print_text("Статус игры: " + str(self.game.status), 20, 341)