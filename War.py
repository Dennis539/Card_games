# War

# You start with a normal deck from 52 card, which will be split up in 2 equal stacks. 
# Every player will take one card and and lay it on the table. The card with the higher ranking will win
# The player which had the higher rank would then receive both cards. 

# Caveat. there will be a moment where both players will have the same card. This is war. 
# In this case, an additional set of cards will be pulled out (lets say 5). These will be held apart 
# after which both players draw a new card. The person who wins now will then get all of the cards. 

#%%
from numpy import number
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck():
    
    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)


    def shuffle_deck(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class Player():
    def __init__(self, name):
        self.name = name
        self.hand = []

        for cards in range(26):
            card = new_deck.deal_one()
            self.hand.append(card)

    def lay_card(self):
        return self.hand.pop(0)

    def add_card(self, new_cards):
        if type(new_cards) == type([]):
            self.hand.extend(new_cards)
        
        else:
            self.hand.append(new_cards)

    def __str__(self):
        return f'Player {self.name} had {len(self.hand)} cards.'


#%%
while Game_on:
    new_deck = Deck()
    new_deck.shuffle_deck()
    war_cards = 5

    player1 = Player('Silver')
    player2 = Player('Bjob')

    while len(player1.hand) != 0 and len(player2.hand) != 0:
        print(f'{player1.name} has {len(player1.hand)} cards')
        print(f'{player2.name} has {len(player2.hand)} cards')

        player1_card = player1.lay_card()
        player2_card = player2.lay_card()

        if player1_card.value > player2_card.value:
            player1.add_card([player1_card, player2_card])
            print(f'Round won by {player1.name}')
            

        elif player1_card.value < player2_card.value:
            player2.add_card([player1_card, player2_card])
            print(f'Round won by {player2.name}')
            

        else:
            print('War!!')

            if len(player1.hand) == 0:
                print(f'{player1.name} is out of cards and cannot go on war')
                break

            elif len(player2.hand) == 0:
                print(f'{player2.name} is out of cards and cannot go on war')
                break
                
            cards_at_stake = [player1_card, player2_card]
            equal_value = True

            while equal_value:

                if len(player1.hand) > war_cards and len(player2.hand) > war_cards:
                    for num in range(war_cards):
                        cards_at_stake.append(player1.lay_card())
                        cards_at_stake.append(player2.lay_card())

                else:
                    for num in range(min([len(player1.hand), len(player2.hand)]) - 1):
                        cards_at_stake.append(player1.lay_card())
                        cards_at_stake.append(player2.lay_card())

                player1_card = player1.lay_card()
                player2_card = player2.lay_card()
                cards_at_stake.extend([player1_card, player2_card])

                if player1_card.value > player2_card.value:
                    player1.add_card(cards_at_stake)
                    print(f'Round won by {player1.name}')
                    equal_value = False
                    continue

                elif player1_card.value < player2_card.value:
                    player2.add_card(cards_at_stake)
                    print(f'Round won by {player2.name}')
                    equal_value = False
                    continue

                if len(player1.hand) == 0 or len(player2.hand) == 0:
                    break
            
    if len(player1.hand) == 0:
        print(f'{player1.name} is out of cards')

    elif len(player2.hand) == 0:
        print(f'{player2.name} is out of cards')







#%%
kees = [1,2,3,4,5]

hond = kees.pop(0)





#%%




# %%
