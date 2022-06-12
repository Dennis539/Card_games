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
from ast import Continue
import random
import pygame
import os
import sys
import time


pygame.font.init()
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blackjack')


os.chdir('C:\\Users\\Dennis\\OneDrive\\Documenten\\Programming in Python\\Pet projects')
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

card_image_dict = {}
for rank in ranks:
    for suit in suits:
        card_name = f'{rank}_of_{suit}'
        scale = pygame.image.load(os.path.join('assets', card_name + '.png'))
        card_image_dict[card_name] = pygame.transform.scale(scale, (100,139))

BG = pygame.image.load(os.path.join('assets', 'poker_table.png'))
BG = pygame.transform.scale(BG, (1200, 700))

forfeit_img = pygame.image.load(os.path.join('assets', 'forfeit.jpg'))
forfeit_img = pygame.transform.scale(forfeit_img, (200, 100))

hit_image = pygame.image.load(os.path.join('assets', 'Hit_button.png'))
hit_image = pygame.transform.scale(hit_image, (200, 100))

pass_image = pygame.image.load(os.path.join('assets', 'Pass_button.png'))
pass_image = pygame.transform.scale(pass_image, (200, 100))

quit_image = pygame.image.load(os.path.join('assets', 'Quit_button.png'))
quit_image = pygame.transform.scale(quit_image, (200, 100))

continue_image = pygame.image.load(os.path.join('assets', 'Continue_button.png'))
continue_image = pygame.transform.scale(continue_image, (200, 100))

card_backside_image = pygame.image.load(os.path.join('assets', 'Playing_card_backside.jpg'))
card_backside_image = pygame.transform.scale(card_backside_image, (200, 100))

play_button_image = pygame.image.load(os.path.join('assets', 'play_button.png'))
play_button_image = pygame.transform.scale(play_button_image, (200, 100))

start_button_image = pygame.image.load(os.path.join('assets', 'start_button.png'))
start_button_image = pygame.transform.scale(start_button_image, (500, 250))

close_button_image = pygame.image.load(os.path.join('assets', 'close_button.png'))
close_button_image = pygame.transform.scale(close_button_image, (500, 250))

split_button_image = pygame.image.load(os.path.join('assets', 'split_button.png'))
split_button_image = pygame.transform.scale(split_button_image, (200, 100))




class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, window):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            # Checks whether the left mouse button is being clicked.
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        window.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Card():
    def __init__(self, suit, rank, img, x, y):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        self.img = img
        self.x = x
        self.y = y


    def __str__(self):
        return self.rank + ' of ' + self.suit


    def draw(self, window, x, y):
        self.x = x
        self.y = y
        window.blit(self.img, (self.x, self.y))

class Deck():
    
    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                card_name = f'{rank}_of_{suit}'
                created_card = Card(suit, rank, card_image_dict[card_name],0, 0)
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
        self.active_hand = []
        self.name = name
        self.budget = 1000
        self.split = False

    def add_hand(self, new_hand):
        self.active_hand.append(new_hand)

    def add_to_budget(self, inlay_won):
        self.budget += inlay_won

    def inlay(self, inlay):
        self.budget -= inlay


    def show_hand(self):
        for card in self.hand:
            print(f'{card.rank} of {card.suit}')

    def reset_hand(self):
        self.hand = []
        self.hand_rank = []
        self.hand_value = 0
        self.aces = []

    def split_hand(self):
        self.split = True

class GameState():
    def __init__(self):
        self.run = True
        self.outcome = None
        self.turn = 'Player'
        self.quit = False
        self.next_round = False
        self.player_bust = False
        self.resume = True
        self.show_split_button = True

    def reset(self):
        self.run = True
        self.outcome = None
        self.turn = 'Player'
        self.quit = False
        self.next_round = True
        self.player_bust = False

class Hand():
    def __init__(self):
        self.hand = []
        self.hand_rank = []
        self.hand_value = 0
        self.aces = []

    def update_hand(self, new_card, value, rank):
        self.hand.append(new_card)
        self.hand_value += value
        self.hand_rank.append(rank)
        if new_card.rank == 'Ace':
            self.aces.append(new_card.rank)

    def remove_card(self):
        pop_card = self.hand.pop()

        self.hand_value -= pop_card.value

    def remove_ace(self):
        self.aces.pop(0)


def update_hand(user, card):
    user.add_card(card)
    user.add_card_value(card.value)
    user.add_card_rank(card.rank)
    if card.rank == 'Ace':
        user.add_ace(card.rank)


forfeit_button = Button(800,0, forfeit_img)
hit_button = Button(400, 300, hit_image)
pass_button = Button(600, 300, pass_image)
quit_button = Button(600, 300, quit_image)
continue_button = Button(400, 300, continue_image)
play_button = Button(200, 300, play_button_image)
start_button = Button(350, 150, start_button_image)
close_button = Button(350, 350, close_button_image)
split_button = Button(350, 350, split_button_image)


def main():
    gamestate = GameState()
    computer = Computer()
    player = Player('Kees')

    main_font = pygame.font.SysFont('comicsans', 20)

    def start_screen():
        WIN.blit(BG, (0,0))
        start_button.draw(WIN)
        close_button.draw(WIN)
        pygame.display.update()
        while not gamestate.next_round:
            event = pygame.event.wait()
            if start_button.draw(WIN):
                gamestate.next_round = True

            elif close_button.draw(WIN):
                WIN.blit(BG, (0,0))
                label = main_font.render(f'Hope to see you next time!', 8, (255,255,255))
                WIN.blit(label, (400, 350))
                pygame.display.update()
                time.sleep(3)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    def draw_window():
        WIN.blit(BG, (0,0))
            
        chips_label = main_font.render(f'You have {player.budget} credits', 1, (255,255,255))
        WIN.blit(chips_label, (10,10))

        if card1.value != card2.value and gamestate.show_split_button:
            split_button.draw(WIN)
            pass_button.draw(WIN)
            

        if gamestate.turn == 'Player' and gamestate.resume == True:
            hit_button.draw(WIN)
            pass_button.draw(WIN)

        player_hand_value_text = main_font.render(f'Total value: {player.active_hand[0].hand_value}', 1, (255, 255, 255))
        WIN.blit(player_hand_value_text, (10, 500))

        comp_hand_value_text = main_font.render(f'Total value: {computer.hand_value}', 1, (255, 255, 255))
        WIN.blit(comp_hand_value_text, (10, 150))

        dist = 0
        dist_stack = 0
        for i in range(len(player.active_hand)):
            dist = dist + dist_stack
            
            for card in player.active_hand[i].hand:
                x_pos = (900/(len(player.active_hand[i].hand) + 1)) + dist
                card.draw(WIN, x_pos, 560)
                dist += 75

            dist_stack += 300

        if len(computer.hand) == 1:
            card1_comp.draw(WIN, 450, 0)
            WIN.blit(card_backside_image, (600, 0))

        else:
            dist = 0
            for card in computer.hand:
                x_pos = (900/len(computer.hand)) + dist
                card.draw(WIN, x_pos, 0)
                dist += 150

        if gamestate.outcome == 'Player_won':
            outcome_label = main_font.render(f'You won, you receive 200 credits', 1, (255,255,255))
            WIN.blit(outcome_label, (400, 350))

        elif gamestate.outcome  == 'Tie':
            outcome_label = main_font.render(f'Tie! You get your credits back, ', 1, (255,255,255))
            WIN.blit(outcome_label, (400, 350))

        elif gamestate.outcome  == 'Computer_won':
            outcome_label = main_font.render(f'You lost!', 1, (255,255,255))
            WIN.blit(outcome_label, (400, 350))

        else:
            outcome_label = None

        pygame.display.update()


    pass_label = main_font.render('You have chosen to pass, now the computer goes', 1, (255, 255, 255))
    busted_label = main_font.render('Busted!', 1, (255, 255, 255))

    while gamestate.run:
        #clock.tick(60)
        start_screen()


        while gamestate.next_round:

            deck = Deck()
            deck.shuffle_deck()

            inlay = 100
            player.inlay(inlay)
            hand1 = Hand()

            card1 = deck.deal_one()
            card2 = deck.deal_one()

            hand1.update_hand(card1, card1.value, card1.rank)
            hand1.update_hand(card2, card2.value, card2.rank)
            player.add_hand(hand1)
            #card1.draw(WIN, 500, 500)

            draw_window()
            pygame.display.update()
            if card1.value != card2.value: #debug only
                gamestate.resume = False
                while gamestate.resume == False:
                    split_button.draw(WIN)
                    draw_window()
                    event = pygame.event.wait()
                    if split_button.draw(WIN):
                        new_hand = Hand()
                        new_hand.update_hand(card2, card2.value, card2.rank)
                        player.active_hand[0].remove_card()
                        gamestate.show_split_button = False
                        gamestate.resume = True
                        player.add_hand(new_hand)
                        draw_window()


                    elif pass_button.draw(WIN):
                        gamestate.resume = True
                        Passing = True
                        gamestate.show_split_button = False
                        WIN.blit(pass_label, (10,10))
                        break
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            card1_comp = deck.deal_one()
            update_hand(user = computer, card = card1_comp)

            card1_comp.draw(WIN, 500, 0)
            WIN.blit(card_backside_image, (650, 0))
            draw_window()

            Passing = False
            for i in range(len(player.active_hand)):

                while player.active_hand[i].hand_value < 21 and Passing == False:
                    Hit = False
                    
                    while not Hit:
                        event = pygame.event.wait()
                        if hit_button.draw(WIN):
                            Hit = True
                            new_card = deck.deal_one()
                            player.active_hand[i].update_hand(new_card, new_card.value, new_card.rank)
                            draw_window()


                        elif pass_button.draw(WIN):
                            Hit = True
                            Passing = True
                            WIN.blit(pass_label, (10,10))
                            break
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()


                    if player.active_hand[i].hand_value > 21:
                        if len(player.active_hand[i].aces) > 0:
                            player.active_hand[i].hand_value -= 10
                            player.active_hand[i].remove_ace()
                            draw_window()
                        else:
                            gamestate.player_bust = True
                            break

                    if Passing == False:
                        Hit = False






            gamestate.turn = 'Computer'
            draw_window()
            time.sleep(3)

            if gamestate.player_bust:
                gamestate.outcome = 'Computer_won'
                draw_window()

            else:
                card2_comp = deck.deal_one()

                update_hand(user = computer, card = card2_comp)   
                draw_window()
                
                if computer.hand_value == player.hand_value and computer.hand_value >= 16 and len(computer.aces) == 0:
                    gamestate.outcome = 'Tie'
                    outcome_label = main_font.render(f'Computer passed', 1, (255,255,255))
                    WIN.blit(outcome_label, (500, 500))

                if computer.hand_value > player.hand_value:
                    gamestate.outcome = 'Computer_won'

            while computer.hand_value < 21 and computer.hand_value < player.hand_value and gamestate.player_bust == False:
                new_card = deck.deal_one()
                update_hand(user = computer, card = new_card)

                comp_draw_label = main_font.render(f'Computer gets a card', 1, (255,255,255))
                WIN.blit(comp_draw_label, (500, 350))
                pygame.display.update()

                time.sleep(3)

                if computer.hand_value > 21:

                    if len(computer.aces) > 0:
                        computer.hand_value -= 10
                        computer.remove_ace()
                        draw_window()

                    else:
                        gamestate.outcome = 'Player_won'
                        break

                if computer.hand_value > player.hand_value:

                    gamestate.outcome = 'Computer_won'
                    break

                if computer.hand_value == player.hand_value and computer.hand_value >= 16 and len(computer.aces) == 0:

                    gamestate.outcome = 'Tie'
                    break

                if computer.hand_value == 21 and player.hand_value == 21:
                    gamestate.outcome = 'Tie'
                    break

                draw_window()
            draw_window()
            if gamestate.outcome == 'Player_won':
                player.add_to_budget(inlay_won = inlay * 2)

            elif gamestate.outcome == 'Tie':
                player.add_to_budget(inlay_won = inlay)

            
            time.sleep(3)

            gamestate.outcome = None
            draw_window()
            player.reset_hand()
            computer.reset_hand()
            while not gamestate.quit:
                continue_button.draw(WIN)
                quit_button.draw(WIN)
                pygame.display.update()
                event = pygame.event.wait()
                if continue_button.draw(WIN):
                    gamestate.reset()
                    break

                
                elif quit_button.draw(WIN):
                    gamestate.next_round = False
                    break
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            if not gamestate.next_round:
                break

            draw_window()
            

            if player.budget == 0:
                gamestate.run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

main()


#%%


player = Player('Kees')
deck = Deck()
deck.shuffle_deck()

inlay = 100
player.inlay(inlay)
hand1 = Hand()

card1 = deck.deal_one()
card2 = deck.deal_one()

hand1.update_hand(card1, card1.value, card1.rank)
hand1.update_hand(card2, card2.value, card2.rank)
player.add_hand(hand1)

player.active_hand[0]

player.active_hand[0].remove_card

#%%



















#%%
def main():
    gamestate = GameState()
    computer = Computer()
    player = Player('Kees')

    main_font = pygame.font.SysFont('comicsans', 20)

    def start_screen():
        WIN.blit(BG, (0,0))
        start_button.draw(WIN)
        close_button.draw(WIN)
        pygame.display.update()
        while not gamestate.next_round:
            event = pygame.event.wait()
            if start_button.draw(WIN):
                gamestate.next_round = True

            elif close_button.draw(WIN):
                WIN.blit(BG, (0,0))
                label = main_font.render(f'Hope to see you next time!', 8, (255,255,255))
                WIN.blit(label, (400, 350))
                pygame.display.update()
                time.sleep(3)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    def draw_window():
        WIN.blit(BG, (0,0))
            
        chips_label = main_font.render(f'You have {player.budget} credits', 1, (255,255,255))
        WIN.blit(chips_label, (10,10))

        if gamestate.turn == 'Player':
            hit_button.draw(WIN)
            pass_button.draw(WIN)
            if player.split_hand:
                split_button.draw(WIN)
        dist = 0

        player_hand_value_text = main_font.render(f'Total value: {player.hand_value}', 1, (255, 255, 255))
        WIN.blit(player_hand_value_text, (10, 500))

        comp_hand_value_text = main_font.render(f'Total value: {computer.hand_value}', 1, (255, 255, 255))
        WIN.blit(comp_hand_value_text, (10, 150))


        for card in player.hand:
            x_pos = (900/len(player.hand)) + dist
            card.draw(WIN, x_pos, 560)
            dist += 150

        if len(computer.hand) == 1:
            card1_comp.draw(WIN, 450, 0)
            WIN.blit(card_backside_image, (600, 0))

        else:
            dist = 0
            for card in computer.hand:
                x_pos = (900/len(computer.hand)) + dist
                card.draw(WIN, x_pos, 0)
                dist += 150

        if gamestate.outcome == 'Player_won':
            outcome_label = main_font.render(f'You won, you receive 200 credits', 1, (255,255,255))
            WIN.blit(outcome_label, (400, 350))

        elif gamestate.outcome  == 'Tie':
            outcome_label = main_font.render(f'Tie! You get your credits back, ', 1, (255,255,255))
            WIN.blit(outcome_label, (400, 350))

        elif gamestate.outcome  == 'Computer_won':
            outcome_label = main_font.render(f'You lost!', 1, (255,255,255))
            WIN.blit(outcome_label, (400, 350))

        else:
            outcome_label = None

        pygame.display.update()


    pass_label = main_font.render('You have chosen to pass, now the computer goes', 1, (255, 255, 255))
    busted_label = main_font.render('Busted!', 1, (255, 255, 255))

    
    while gamestate.run:
        #clock.tick(60)
        start_screen()

        while gamestate.next_round:
            draw_window()


            deck = Deck()
            deck.shuffle_deck()

            inlay = 100
            player.inlay(inlay)



            card1 = deck.deal_one()
            card1.draw(WIN, 500, 500)

            card2 = deck.deal_one()
            card2.draw(WIN, 650, 500)

            update_hand(user = player, card = card1)
            update_hand(user = player, card = card2)
            
            card1_comp = deck.deal_one()
            update_hand(user = computer, card = card1_comp)

            card1_comp.draw(WIN, 500, 0)
            WIN.blit(card_backside_image, (650, 0))
            

            pygame.display.update()
            if card1.rank == card1.rank:
                resume = False
                while not resume:
                    event = pygame.event.wait()
                    if split_button.draw(WIN):
                        new_hand = Hand()
                        update_hand(user = new_hand, card = card2)
                        draw_window()


                    elif pass_button.draw(WIN):
                        resume = True
                        Passing = True
                        WIN.blit(pass_label, (10,10))
                        break
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            Passing = False
            draw_window()



#%%



            while player.hand_value < 21 and Passing == False:
                Hit = False
                
                while not Hit:
                    event = pygame.event.wait()
                    if hit_button.draw(WIN):
                        Hit = True
                        new_card = deck.deal_one()
                        update_hand(user = player, card = new_card)
                        draw_window()


                    elif pass_button.draw(WIN):
                        Hit = True
                        Passing = True
                        WIN.blit(pass_label, (10,10))
                        break
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                WIN.blit(busted_label, (10,10))

                if player.hand_value > 21:
                    if len(player.aces) > 0:
                        player.hand_value -= 10
                        player.remove_ace()
                        draw_window()
                    else:
                        gamestate.player_bust = True
                        break

                if Passing == False:
                    Hit = False

            gamestate.turn = 'Computer'
            draw_window()
            time.sleep(3)

            if gamestate.player_bust:
                gamestate.outcome = 'Computer_won'
                draw_window()

            else:
                card2_comp = deck.deal_one()

                update_hand(user = computer, card = card2_comp)   
                draw_window()
                
                if computer.hand_value == player.hand_value and computer.hand_value >= 16 and len(computer.aces) == 0:
                    gamestate.outcome = 'Tie'
                    outcome_label = main_font.render(f'Computer passed', 1, (255,255,255))
                    WIN.blit(outcome_label, (500, 500))

                if computer.hand_value > player.hand_value:
                    gamestate.outcome = 'Computer_won'

            while computer.hand_value < 21 and computer.hand_value < player.hand_value and gamestate.player_bust == False:
                new_card = deck.deal_one()
                update_hand(user = computer, card = new_card)

                comp_draw_label = main_font.render(f'Computer gets a card', 1, (255,255,255))
                WIN.blit(comp_draw_label, (500, 350))
                pygame.display.update()

                time.sleep(3)

                if computer.hand_value > 21:

                    if len(computer.aces) > 0:
                        computer.hand_value -= 10
                        computer.remove_ace()
                        draw_window()

                    else:
                        gamestate.outcome = 'Player_won'
                        break

                if computer.hand_value > player.hand_value:

                    gamestate.outcome = 'Computer_won'
                    break

                if computer.hand_value == player.hand_value and computer.hand_value >= 16 and len(computer.aces) == 0:

                    gamestate.outcome = 'Tie'
                    break

                if computer.hand_value == 21 and player.hand_value == 21:
                    gamestate.outcome = 'Tie'
                    break

                draw_window()
            draw_window()
            if gamestate.outcome == 'Player_won':
                player.add_to_budget(inlay_won = inlay * 2)

            elif gamestate.outcome == 'Tie':
                player.add_to_budget(inlay_won = inlay)

            
            time.sleep(3)

            gamestate.outcome = None
            draw_window()
            player.reset_hand()
            computer.reset_hand()
            while not gamestate.quit:
                continue_button.draw(WIN)
                quit_button.draw(WIN)
                pygame.display.update()
                event = pygame.event.wait()
                if continue_button.draw(WIN):
                    gamestate.reset()
                    break

                
                elif quit_button.draw(WIN):
                    gamestate.next_round = False
                    break
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            if not gamestate.next_round:
                break

            draw_window()
            

            if player.budget == 0:
                gamestate.run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


main()



# %%
