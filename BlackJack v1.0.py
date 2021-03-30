#BLACKJACK by Kewl (v1.0)
import random
suit = ("Hearts","Diamonds","Clubs","Spades")
rank = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

class Chips():
	def __init__(self, chip_value=100):
		self.chip_value = chip_value
	def add_chips(self,chips):
		self.chip_value += chips
	def remove_chips(self,chips):
		self.chip_value -= chips
	def __str__(self):
		return f"Your chips are curently worth ${self.chip_value}."
class Hand(): 
	def __init__(self):
		self.current_hand = []
	def sum_of_hand(self): 
		sum_total = 0
		for i in self.current_hand:
			sum_total += i.value
		return sum_total	
	def add_to_hand(self,card):
		self.current_hand.append(card)
	def display_hand(self):
		for i in self.current_hand:
			print(i)
	def clear_hand(self):
		self.current_hand.clear()
class Card():
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.value = values[rank] 
	def __str__(self):
		return f'{self.rank} of {self.suit}'
class Deck():
	def __init__(self):
		self.all_cards = []
		for r in rank:
			for s in suit:
				created_card = Card(r,s)
				self.all_cards.append(created_card)
	def __str__(self):
		return f'There are {len(self.all_cards)} cards remaining'
	def draw_one(self):
		return self.all_cards.pop(0)
	def shuffle_deck(self):
		random.shuffle(self.all_cards)
class Player():
	def __init__(self, bankroll, hand):
		self.bankroll = bankroll
		self.hand = hand
class Dealer():  
	def __init__(self,hand):
		self.hand = hand

def ready():
	return input("\nAre you ready to play? Enter Yes or No: ").lower().startswith("y")
def player_value(player_hand):
	sum_total = 0
	for i in player_hand.current_hand:
		sum_total += i.value
	if sum_total > 21:
		for i in player_hand.current_hand:
			if i.rank == "Ace":
				sum_total -= 10
			return sum_total
	else:
		return sum_total
def dealer_value(dealer_hand):
	sum_total = 0
	for i in dealer_hand.current_hand:
		sum_total += i.value
	return sum_total
def reshuffle_deck(game_deck):
		game_deck = Deck()
		game_deck.shuffle_deck()
def draw(user):
	user.hand.add_to_hand(game_deck.draw_one())
def show_table(player,dealer):
	print("\nPlayer hand")
	player.hand.display_hand()
	print("\nDealer Hand")
	dealer.hand.display_hand()
def clear_table(player,dealer):
	player.hand.clear_hand()
	dealer.hand.clear_hand()
def deal_em(player,dealer):
	for i in range(0,2):
		player.hand.add_to_hand(game_deck.draw_one())
		dealer.hand.add_to_hand(game_deck.draw_one())

if __name__ == "__main__":
	player = Player(Chips(), Hand())
	dealer = Dealer(Hand())
	game_deck = Deck()
	game_deck.shuffle_deck()
	game_on = True
	#Start the game
	while game_on:
		if not ready():
			print(f"\nYou have cashed out with ${player.bankroll.chip_value} in chips! See you next time.")
			break
		if player.bankroll.chip_value <= 0:
			print("\nYou have no chips left. The game is over, please come back another time.")
			break
		reshuffle_deck(game_deck)
	#Draw the cards and display the table
		deal_em(player,dealer)
		print("\nPlayer hand is:")
		player.hand.display_hand()
		print("\nDealer hand is:")
		print(dealer.hand.current_hand[0])
		print("?")
	#Bet or fold for Player	
		player_choice = "BLANK"
		while player_choice not in ["fold", "bet"]:
			player_choice = input("\nWould you like to bet or fold?: ").lower()
			if player_choice == "fold":
				clear_tale(player,dealer)
			elif player_choice == "bet":
				while True:
					try:
						player_bet = int(input(f"\nPlease enter a bet amount, you currently have ${player.bankroll.chip_value} in chips to bet: "))
					except:
						print("Sorry I did not understand. Please enter a valid bet amount.")
					else:
						if player_bet > player.bankroll.chip_value:
							print("Sorry you do not have enough chips to make that bet. Please bet a lower amount.")
						else:
							player.bankroll.remove_chips(player_bet)
							print(player.bankroll)
							break
	#Start a round; Player and Dealer turns
		while len(player.hand.current_hand) != 0:
			player_turn = True
			dealer_turn = False
			while player_turn:
				player_choice = "BLANK"
				while player_choice != "stand":
					player_choice = input("\nWould you like to hit or stand?: ").lower()
					if player_choice == "hit":
						draw(player)
						player.hand.display_hand()
					if player_value(player.hand) > 21:
						show_table(player,dealer)
						print(f"\nYou have busted. You lost ${player_bet} in chips.")
						clear_table(player,dealer)
						player_turn = False
						break
					if player_choice == "stand":
						player_turn = False
						dealer_turn = True
			while dealer_turn:
				if dealer_value(dealer.hand) < 17:
					draw(dealer)
				if dealer_value(dealer.hand) > 21:
					show_table(player,dealer)
					print(f"\nPlayer wins, you have won ${player_bet} in chips!")
					player.bankroll.add_chips(player_bet*2)
					clear_table(player,dealer)
					dealer_turn = False
				elif dealer_value(dealer.hand) > player_value(player.hand):
					show_table(player,dealer)
					print(f"\nHouse wins, you lose ${player_bet} in chips.")
					clear_table(player,dealer)
					dealer_turn = False