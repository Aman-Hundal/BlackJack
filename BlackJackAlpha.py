#BLACKJACK by Aman (v1.0)
import random
suit = ("Hearts","Diamonds","Clubs","Spades")
rank = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

class Chips():
	# small thing but be careful and consistent with your spacing
	def __init__(self, chip_value = 100):
		self.chip_value = chip_value
	def add_chips(self, chips):
		self.chip_value += chips
	def remove_chips(self, chips):
		self.chip_value -= chips
	def __str__(self):
		return f"Your chips are curently worth ${self.chip_value}."
# Not sure how Python does it but I'd put a space between each class
# I know Python is big on the meaningful whitespace though :|

class Hand():
	def __init__(self):
		self.current_hand = []
	def sum_of_hand(self): 
		sum_total = 0
		# You can change the i to whatever you want to make it more readable, you're picking a variable name
		# if you're iterating for numbers then `i` can make sense but here I'd probably go with `card`
		# for card in self.current_hand
		#         sum_total += card.value
		for i in self.current_hand:
			sum_total += i.value
		return sum_total	
	def add_to_hand(self, card):
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
	# In general I think it's good to avoid creating new instances of a class if possible
	# We talked about this a bit during our chat but are there changes you could make so that you only new one instance of the Deck class?
	# maybe instead of discarding cards after they're drawn, they could be moved to a `used` or `discard` or `in_play` pile
	# shuffle could grab those cards back to the in_play pile and then shuffle
	def __init__(self):
		self.all_cards = []
		# for rank in ranks
		for r in rank:
			# for suit in suits
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
	for card in player_hand.current_hand:
		sum_total += i.value
	if sum_total > 21:
		# Is there ever a situation where we would only want to subtract 10 even if a user has multiple aces?
		# I think this would count 2 aces to have a total value of 2 instead of 12
		# You could do a check after subtracting the 10 to see if the sum_total is still over 21. If not then break the loop
		for i in player_hand.current_hand:
			if i.rank == "Ace":
				sum_total -= 10
			return sum_total
	# not sure the else is strictly necessary. Don't think it effets the code much either way, but you could get rid of the else and the above return
	# because you need to return the same value either way
	else:
		return sum_total

# for player_value/dealer_value, this could be an opportunity to DRY up your code. There's a lot of overlap between the two 
# would a dealer never use an ace as a value of 1? If no you could still try to combine these two functions
# something I've done is pass in a second arg -- in this case it would be something like `is_player_hand`
# def hand_value(hand, is_player_hand = true):
# ...
# if is_player_hand and sum_total > 21
#
# When you call it for the dealer, just remember to pass in false as the second arg
def dealer_value(dealer_hand):
	sum_total = 0
	for i in dealer_hand.current_hand:
		sum_total += i.value
	return sum_total

def reshuffle_deck(game_deck):
		game_deck.shuffle_deck()
		
def draw(user):
	# where does `game_deck` come from? This makes it look like there's a global `game_deck`, but the above function it's being passed in as an arg
	user.hand.add_to_hand(game_deck.draw_one())

def show_table(players):
	for player in players:
		print(f'\n{player.name} hand')
		player.hand.display_hand()

def clear_table(players):
	for player in players:
		player.hand.clear_hand()
	
def deal_em(players):
	# definitely understand the range thing here but if I could think of another option I'd change it lol
	for i in range(0,2):
		for player in players:
			# same deal here, is there a global `game_deck` or should that be passed in?
		player.hand.add_to_hand(game_deck.draw_one())

if __name__ == "__main__":
	player = Player(Chips(), Hand())
	dealer = Dealer(Hand())
	game_deck = Deck()
	game_deck.shuffle_deck()
	# is game_on ever used? Looks like it's set to true and then forgotten about.
	# You're essentially just saying `while true` .. which is always true
	# I'd try to tie this to actual game logic
	game_on = True
	
	# Start the game
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
				clear_tale(player, dealer)
			elif player_choice == "bet":
				# general thought here is to make this game part more readable, is there more that could be abstracted to a method?
				# This while .. try .. expect .. else block here feels like it could be
				#
				# One practice I've tried following from my current job is having as little logic as possible in the "main" part of the
				# program, try to make it so it's just a bunch of function calls that return values. Each of those functions could call more functions
				# It's functions all the way down
				#
				# The `while True` loop is something I'd avoid and try to tie to game logic like above (while is_bet_invalid ?)
				# This feels like it could be a recursive function
				#
				# A try except else block is when there's a possibility of an error, but you don't want it to crash the entire program
				# Is that necessary here? Could you introspect the string from the user? In general it is good practice to never trust anything
				# from a user, but parsing a string and seeing if it's a numeric value doesn't feel like it could produce too many unexpected values
				#
				# Not saying you need to remove the try .. except .. else! 
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
	# Start a round; Player and Dealer turns
		while len(player.hand.current_hand) != 0:
			player_turn = True

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
			while not player_turn:
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
#LOGIC BRAINSTORM (v1.0)
#Give the player two cards from the deck to their hand, 2.give the dealer 2 cards to their hand list but only one is visible 3. Player makes a bet from their chip pool. HAND and DECK ARE A LIST of CARDS. Chip pool is a balnace of chips -> just holds values 

#Player turn:
#player 1 choose to either hit or stay -> need an input call here. 
#Hit->, append their hand list with a card -> deal one deck class, add one player hand class
# Hit - >check to see if hand list sum is >21, if it is = bust and dealer gets chiips. else, ask again if hit or stay. After every hit print a hand value Repeat until bust or player chooses stay - while loop?
#stay -> calculate the sum of player hand go to dealers turn

#dealer turn: 
# continusoulsy append to their hand list (deal one deck class, add one hand class) until 
# they beat the sum of players hand (comaprison operators needed) -> player loss and chips go to dealer
# or until they bust and their hand is >21 (player win and gets x2 chips)

#round end:
# anytime their is a player loss or player win (when a round ends) -> Ask (using an input !) if thye would like to play again. If yes, go back to the first two checks and start a new round again. If not, game_on = False and game is over print out the players chip count and say good bye

#special rules - JQK = value of 10 and Ace can be a 1 or a 11 - whatever is preferrable to the player meaning if they dont bust Ace = 11 if they do bust Ace =1 (do a check in the player turn?) Add the ace rule at the end - this is hardest part. Can you a if statement or can inbed it in class. JQK rule can be done in deck class
