import random
import unittest

# SI 507 Winter 2018
# Homework 2 - Code

##COMMENT YOUR CODE WITH:
# Section Day/Time:
# People you worked with:

######### DO NOT CHANGE PROVIDED CODE #########
### Below is the same cards.py code you saw in lecture.
### Scroll down for assignment instructions.
#########

class Card(object):
	suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
	rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

	def __init__(self, suit=0,rank=2):
		self.suit = self.suit_names[suit]
		if rank in self.faces: # self.rank handles printed representation
			self.rank = self.faces[rank]
		else:
			self.rank = rank
		self.rank_num = rank # To handle winning comparison

	def __str__(self):
		return "{} of {}".format(self.rank,self.suit)


class Deck(object):
	def __init__(self): # Don't need any input to create a deck of cards
		# This working depends on Card class existing above
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card) # appends in a sorted order

	def __str__(self):
		total = []
		for card in self.cards:
			total.append(card.__str__())
		# shows up in whatever order the cards are in
		return "\n".join(total) # returns a multi-line string listing each card

	def pop_card(self, i=-1):
		# removes and returns a card from the Deck
		# default is the last card in the Deck
		return self.cards.pop(i) # this card is no longer in the deck -- taken off


	def shuffle(self):
		random.shuffle(self.cards)

	def replace_card(self, param_Card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
		if param_Card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(param_Card) # append it to the list

	def sort_cards(self):
		# Basically, remake the deck in a sorted way
		# This is assuming you cannot have more than the normal 52 cars in a deck
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card)

class Hand(object):
	# create the Hand with an initial set of cards
	# param: a list of cards
	def __init__(self, init_cards):
		self.my_cards = init_cards

	# add a card to the hand
	# silently fails if the card is already in the hand
	# param: the card to add
	# returns: nothing

	def __str__(self):
		total = []
		for card in self.my_cards:
			total.append(card.__str__())
		return total

	def add_card(self, card):
		card_strs = []
		for c in self.my_cards:
			card_strs.append(c.__str__())
		if card.__str__() not in card_strs:
			self.my_cards.append(card)

	# remove a card from the hand
	# param: the card to remove
	# returns: the card, or None if the card was not in the Hand
	def remove_card(self, card):
		i = 0
		for c in self.my_cards:
			if c.__str__() == card.__str__():
				return self.my_cards.pop(i) # this card is no longer in the deck -- taken off
			else:
				i =+ 1

	# draw a card from a deck and add it to the hand
	# side effect: the deck will be depleted by one card
	# param: the deck from which to draw
	# returns: nothing
	def draw(self, deck):
		self.add_card(deck.pop_card())


def play_war_game(testing=False):
	# Call this with testing = True and it won't print out all the game stuff -- makes it hard to see test results
	player1 = Deck()
	player2 = Deck()

	p1_score = 0
	p2_score = 0

	player1.shuffle()
	player2.shuffle()
	if not testing:
		print("\n*** BEGIN THE GAME ***\n")
	for i in range(52):
		p1_card = player1.pop_card()
		p2_card = player2.pop_card()
		print('p1 rank_num=', p1_card.rank_num, 'p1 rank_num=', p2_card.rank_num)
		if not testing:
			print("Player 1 plays", p1_card,"& Player 2 plays", p2_card)

		if p1_card.rank_num > p2_card.rank_num:

			if not testing:
				print("Player 1 wins a point!")
			p1_score += 1
		elif p1_card.rank_num < p2_card.rank_num:
			if not testing:
				print("Player 2 wins a point!")
			p2_score += 1
		else:
			if not testing:
				print("Tie. Next turn.")

	if p1_score > p2_score:
		return "Player1", p1_score, p2_score
	elif p2_score > p1_score:
		return "Player2", p1_score, p2_score
	else:
		return "Tie", p1_score, p2_score

if __name__ == "__main__":
	result = play_war_game()
	print("""\n\n******\nTOTAL SCORES:\nPlayer 1: {}\nPlayer 2: {}\n\n""".format(result[1],result[2]))
	if result[0] != "Tie":
		print(result[0], "wins")
	else:
		print("TIE!")


######### DO NOT CHANGE CODE ABOVE THIS LINE #########

## You can write any additional debugging/trying stuff out code here...
## OK to add debugging print statements, but do NOT change functionality of existing code.
## Also OK to add comments!

#########

class test_card(unittest.TestCase):

	# Test Basic unit testing No.1 No2
	def test_set_No1_No2(self):#
		card1 = Card(1,12)
		card2 = Card(1,1)
		test_faces=card1.rank
		self.assertEqual(card1.rank,"Queen")
		self.assertEqual(card2.rank,"Ace")

	# Tet Basic unit testing No.3, No.4
	def test_set_No3(self):
		card3 = Card(0,3)
		self.assertEqual(card3.rank, 3)
	#	self.assertEqual(card1.rank,"Queen")
	#	self.assertEqual(card2.rank,"Ace")

	def test_set_No4_No5(self):
		card4 = Card(1,0)
		card5 = Card(2,0)
		self.assertEqual(card4.suit,"Clubs")
		self.assertEqual(card5.suit,"Hearts")


	def test_set_No6(self):
		card6=Card(1,3)
		self.assertTrue(card6.suit in Card.suit_names)

	def test_set_No7(self):
		card7 = Card(2,7)
		self.assertEqual(str(card7), "7 of Hearts")

	def test_set_No8(self):
		card8 = Card(3,13)
		self.assertEqual(str(card8), "King of Spades")

	def test_set_No9(self):#test_deck
		test_deck = Deck()
		self.assertTrue(len(test_deck.cards) == 52)

	def test_set_No10(self):
		self.deck = Deck()
		self.deck.pop_card()
		self.assertIsInstance(self.deck.cards,list)

	def test_set_No11(self):
		self.deck = Deck()
		self.deck.pop_card()
		self.assertEqual(len(self.deck.cards), 51)

	def test_set_No12(self):
		self.assertIsInstance(play_war_game(testing=True),tuple)
		self.assertTrue(len(play_war_game(testing=True)), 3)
		self.assertIsInstance(play_war_game(testing=True)[0], str)

	def test_set_No13(self):
		self.deck = Deck()
		for i in range(52):
			self.deck.pop_card()
		self.assertEqual(self.deck.cards,[])



	def test_init_hand_class(self):
		test_card_set = []
		card1 = Card(0,12)
		card2 = Card(0,1)

		test_card_set.append(card1)
		test_card_set.append(card2)

		test_hand = Hand(test_card_set)

		test_card_str = []
		test_card_str.append(card1.__str__())
		self.assertNotEqual(test_hand.__str__(), test_card_str)

		test_card_str.append(card2.__str__())
		self.assertEqual(test_hand.__str__(), test_card_str)

	def test_add_remove_hand(self):
		test_card_set = []
		card1 = Card(0,12)
		card2 = Card(0,1)

		test_card_set.append(card1)
		test_card_set.append(card2)

		test_hand = Hand(test_card_set)

		test_card_str = []
		test_card_str.append(card1.__str__())
		test_card_str.append(card2.__str__())
		self.assertEqual(test_hand.__str__(), test_card_str)
		#add card
		card3 = Card(0,10)
		test_hand.add_card(card3)
		test_card_str.append(card3.__str__())

		self.assertEqual(test_hand.__str__(), test_card_str)

		#remove
		test_hand.remove_card(card2)
		test_card_str = []
		test_card_str.append(card1.__str__())
		test_card_str.append(card3.__str__())

		self.assertEqual(test_hand.__str__(), test_card_str)

	def test_draw(self):
		test_deck = Deck()
		self.assertTrue(len(test_deck.cards) == 52)

		test_card_set = []
		card1 = Card(0,12)
		card2 = Card(0,1)

		test_card_set.append(card1)
		test_card_set.append(card2)

		test_hand = Hand(test_card_set)

		test_hand.draw(test_deck)
		self.assertTrue(len(test_deck.cards) == 51)
		test_hand.draw(test_deck)
		self.assertTrue(len(test_deck.cards) == 50)



	#def test(self,rank):
	#for rank_num in sample_rank :



	#	self.assertEqual(card1.rank,"Queen")
	#	self.assertEqual(card2.rank,"Ace")









##**##**##**##@##**##**##**## # DO NOT CHANGE OR DELETE THIS COMMENT LINE -- we use it for grading your file
###############################################

### Write unit tests below this line for the cards code above.

#class TestCard(unittest.TestCase):


	# this is a "test"
#	def test_create(self):
#		card = Card()
#		self.assertEqual(self.card1.suit, "Diamonds")
#		self.assertEqual(self.card1.rank, 3)




#############
## The following is a line to run all of the tests you include:
if __name__ == "__main__":
	unittest.main(verbosity=2)
## verbosity 2 to see detail about the tests the code fails/passes/etc.
