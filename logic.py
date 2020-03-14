import random

from typing import Tuple, Dict, List

suits: Tuple[str, ...] = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks: Tuple[str, ...] = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'J', 'Q', 'K', 'A')
values: Dict[str, int] = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}


class Card(object):
	suit: str
	rank: str

	def __init__(self, suit: str, rank: str):
		self.suit = suit
		self.rank = rank


class Deck:
	deck: List[Card] = []

	def recover(self):
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit, rank))

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self) -> Card:
		return self.deck.pop()

	def size(self) -> int:
		return len(self.deck)


class Hand:
	cards: List[Card] = []
	cost: int = 0
	aces_count: int = 0

	def add_card(self, card: Card):
		self.cards.append(card)
		self.cost += values[card.rank]
		if card.rank == 'A':
			self.aces_count += 1
		self._adjust_for_aces()

	def _adjust_for_aces(self):
		while self.cost > 21 and self.aces_count:
			self.cost -= 10
			self.aces_count -= 1

	def clear(self):
		self.cards = []
		self.cost = 0
		self.aces_count = 0


class Bank:
	total_money: int = 100
	bet: int = 5

	def inc_bet(self):
		if self.bet < self.total_money:
			self.bet += 1

	def dec_bet(self):
		if self.bet > 0:
			self.bet -= 1

	def mul_bet(self):
		if self.bet*2 < self.total_money:
			self.bet *= 2

	def add_bet(self):
		self.total_money += self.bet

	def sub_bet(self):
		self.total_money -= self.bet


class Player:
	hand: Hand = Hand()
	bank: Bank = Bank()


class Dealer:
	hand: Hand = Hand()


class Game:
	player: Player = Player()
	dealer: Dealer = Dealer()
	deck: Deck = Deck()

	is_playing: bool = False
	status: str = "In process"

	def __init__(self):
		self.restart()

	def restart(self):
		self.player.hand.clear()
		self.dealer.hand.clear()
		self.deck.recover()
		self.deal()
		self.is_playing = True
		self.status = "Идёт игра"


	def hit(self):
		self.player.hand.add_card(self.deck.deal())
		self.player.hand._adjust_for_aces()
		if self.player.hand.cost > 21:
			self.player.bank.sub_bet()
			self.status = "Поражение"
			self.is_playing = False

	def stand(self):
		while self.dealer.hand.cost < 17:
			self.dealer.hand.add_card(self.deck.deal())
		if self.dealer.hand.cost > 21:
			self.player.bank.add_bet()
			self.status = "Победа"
		else:
			if self.dealer.hand.cost > self.player.hand.cost:
				self.player.bank.sub_bet()
				self.status = "Поражение"
			else:
				self.player.bank.add_bet()
				self.status = "Победа"
		self.is_playing = False

	def rise(self):
		self.player.bank.mul_bet()

	def inc_bet(self):
		self.player.bank.inc_bet()

	def dec_bet(self):
		self.player.bank.dec_bet()

	def deal(self):
		if self.deck.size() < 4:
			self.deck = Deck()
		self.deck.shuffle()

		self.player.hand.add_card(self.deck.deal())
		self.player.hand.add_card(self.deck.deal())

		self.dealer.hand.add_card(self.deck.deal())