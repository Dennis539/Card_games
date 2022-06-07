# Blackjack 

# There will only be a computer dealer and a human player
# Player will start with placing a bet for the bankroll. 
# the Player will place a bet according to his/her bankroll

# Start of the game
# at the start, the player will get 2 cards face up and the computer one card
# face up and one card face down. The player will have 2 actions, hit or stay. 

# After that, the dealer will play. It will play along if the player is under 21.
# The dealer will hit until they either beat the player or they bust. 

#%%
import random
import pygame
import os

os.chdir('C:\\Users\\Dennis\\OneDrive\\Documenten\\Programming in Python\\Pet projects\\Card_games')
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

card_image_dict = {}
for rank in ranks:
    for suit in suits:
        card_name = f'{rank}_of_{suit}'
        card_image_dict[card_name] = pygame.image.load(os.path.join('assets', card_name + '.png'))






#%%

class Card():
    def __init__(self, suit, rank, img):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        self.img = img

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck():
    
    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                card_name = f'{rank}_of_{suit}'
                created_card = Card(suit, rank, card_image_dict[card_name])
                self.all_cards.append(created_card)


    def shuffle_deck(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop(0)


class Computer():
    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.hand_rank = []
        self.aces = []

    def add_card(self, new_card):
        self.hand.append(new_card)

    def add_card_value(self, value):
        self.hand_value += value

    def add_card_rank(self, rank):
        self.hand_rank.append(rank)
    
    def add_ace(self, ace):
        self.aces.append(ace)

    def remove_ace(self):
        self.aces.pop(0)

    def show_hand(self):
        for card in self.hand:
            print(f'{card.rank} of {card.suit}')

    def reset_hand(self):
        self.hand = []
        self.hand_rank = []
        self.hand_value = 0
        self.aces = []

class Player():
    def __init__(self, name):
        self.hand = []
        self.hand_rank = []
        self.hand_value = 0
        self.name = name
        self.budget = 1000
        self.aces = []

    def add_card(self, new_card):
        self.hand.append(new_card)

    def add_card_value(self, value):
        self.hand_value += value

    def add_card_rank(self, rank):
        self.hand_rank.append(rank)

    def add_to_budget(self, inlay_won):
        self.budget += inlay_won

    def inlay(self, inlay):
        self.budget -= inlay

    def add_ace(self, ace):
        self.aces.append(ace)

    def remove_ace(self):
        self.aces.pop(0)

    def show_hand(self):
        for card in self.hand:
            print(f'{card.rank} of {card.suit}')

    def reset_hand(self):
        self.hand = []
        self.hand_rank = []
        self.hand_value = 0
        self.aces = []


def update_hand(user, card):
    user.add_card(card)
    user.add_card_value(card.value)
    user.add_card_rank(card.rank)
    if card.rank == 'Ace':
        user.add_ace(card.rank)



#%%
while True:
    computer = Computer()
    player = Player('Kees')

        
    game_on = True
    # Turn of the player
    while player.budget > 0 and game_on:
        deck = Deck()
        deck.shuffle_deck()

        inlay = 100
        player.inlay(inlay)

        # Creating the hand of the player
        card1 = deck.deal_one()
        card2 = deck.deal_one()
        update_hand(user = player, card = card1)
        update_hand(user = player, card = card2)

        # Creating the hand of the computer
        card1 = deck.deal_one()
        card2 = deck.deal_one()
        update_hand(user = computer, card = card1)

        player_bust = False

        print('Your cards are:')        
        player.show_hand()
        print(f'The value in your hand is {player.hand_value}')
        print('\n')
        print('The computer has the following cards:')
        computer.show_hand()
        print('\n')
        
        while player.hand_value < 21:
            
            x = input('Hit or Stop?:' )
            if x.lower() == 'stop':
                print('Player decided to stop')
                break

            elif x.lower() == 'hit':
                print('Deal one card')
                new_card = deck.deal_one()
                print(f'{new_card.rank} of {new_card.suit}')

               
                update_hand(user = player, card = new_card)

                if player.hand_value > 21:
                    print(f'The value in your hand is {player.hand_value}')
                    if len(player.aces) > 0:
                        player.hand_value -= 10
                        print('Ace in hand! Total value in hand will be lowered')
                        player.remove_ace()
                        print(f'The value in your hand is {player.hand_value}')
                        continue
                    
                    else:
                        print('Total value of hand exceeds 21. Bust!')
                        outcome = 'computer_won'
                        player_bust = True
                        break


                elif player.hand_value < 21: 
                    print(f'The value in your hand is {player.hand_value}')
                    continue

                else: # The player will have a combined value of 21 in his/her hand
                    print('The value in your hand is 21!')
                    break

            else:
                print('Improper text, please fill in Hit or Stop')

            break

        if player_bust:
            player.hand_value = 0


        # Computers turn
        print('\n\n')
        print('Now it is the turn of the computer')

        print('Computer reveals his hidden card')
        update_hand(user = computer, card = card2)
        computer.show_hand()
        print(f'The value of the computers hand is {computer.hand_value}')

        #if computer.hand_value > player.hand_value:
        #    print('Computer won')
        #    outcome = 'computer_won'
        #   break

        if computer.hand_value == player.hand_value and computer.hand_value >= 16 and len(computer.aces) == 0:
            
            print(f'The value of the computers hand is {computer.hand_value}')
            print('Computer will not hit again, Tie!')
            outcome = 'tie'
            

        if computer.hand_value > player.hand_value:
            print('Computer won')
            outcome = 'computer_won'

        while computer.hand_value < 21 and computer.hand_value < player.hand_value:
            new_card = deck.deal_one()
            print('Deal one card')
            update_hand(user = computer, card = new_card)

            if computer.hand_value > 21:
                print(f'The value of the computers hand is {computer.hand_value}')

                if len(computer.aces) > 0:
                    print('Ace in hand! Total value in hand will be lowered')
                    computer.hand_value -= 10
                    computer.remove_ace()
                    print(f'The value of the computers hand is {computer.hand_value}')

                else:
                    print('computer busted!')
                    outcome = 'player_won'
                    break

            if computer.hand_value > player.hand_value:
                print(f'The value of the computers hand is {computer.hand_value}')
                print('Value of cards higher for the computer. Computer won.')
                outcome = 'computer_won'
                break

            if computer.hand_value < player.hand_value:
                print(f'The value of the computers hand is {computer.hand_value}')

            if computer.hand_value == player.hand_value and computer.hand_value >= 16 and len(computer.aces) == 0:
                print(f'The value of the computers hand is {computer.hand_value}')
                print('Computer will not hit again, Tie!')
                outcome = 'tie'
                break

            if computer.hand_value == 21 and player.hand_value == 21:
                print('Tie')
                outcome = 'tie'
                break

            # The idea would be that the computer would continue if the value of its cards
            # is lower than that of the player or there is a tie where the value of its
            # cards is 15 or lower. 

        if outcome == 'player_won':
            print(f'Added {inlay * 2} credits to your budget')
            player.add_to_budget(inlay * 2)

        elif outcome == 'tie':
            print(f'Added {inlay} credits to your budget')
            player.add_to_budget(inlay)
        
        else:
            print('You lost your inlay!')

        print(f'You have a budget of {player.budget} credits')
        continue_playing = input('Do you wish to continue playing? (yes or no): ')

        if continue_playing.lower() == 'no':
            game_on = False

        if continue_playing.lower() == 'yes':
            player.reset_hand()
            computer.reset_hand()


    print('Quit the game')
    break




    







#%%
def po(ruig):
    return ruig.pop(0)

kees = [1,2,3,4]

po(kees)

# %%
