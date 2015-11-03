# Jujitsu Project
# By Hestiaflame
# Edits by cproctor

from jujitsu_library import is_valid_play, winning_card, cards
from random import choice

def chris_version_of_myplayer(state, player_name):
    hand = cards(player_name, state['history'])
    treasure = state['treasure']
    # If the treasure is below 8 but not 1, play the same card as the treasure 
    # (If I have that card).
    if treasure != 1 and treasure < 8:
        if treasure in hand:
            return treasure
        # If I don't have that card, play the next highest card. 
        if treasure + 1 in hand:
            return treasure + 1
    # If the treasure is above 8 but not 13, 
    if treasure >= 8 and treasure != 13:
        # play the next higher card above the treasure. 
        if treasure + 1 in hand:
            return treasure + 1
    # If the treasure is 13, play 1 if we have it.
    if treasure == 13 and 1 in hand:
        return 1
    # If the the treasure is 1, play the next higher card above the treasure.
    for card in range(2,14):
        if card in hand:
            return card
    # If we haven't played a card yet, play a random card. 
    return choice(hand)
            
        
        

# Original version
def check_card(card_number, state, player_name):
    for each_dict in state['history']:
        if each_dict[player_name] == card_number:
            return False
        else:
            return True

def myplayer(state, player_name):
    myCards = cards(player_name, state['history'])
    new_card = state['treasure']
    card = False
    counter = 0
    while card == False:
        if new_card < 7 and new_card != 1:
            new_card = new_card - 1
        if new_card > 7 and new_card != 13:
            if counter > 0:
                new_card += 1
        elif new_card == 1:
            new_card += 1
        elif new_card == 13:
            if new_card == 13:
                new_card = 2
            elif new_card == 1:
                new_card = 13
            else:
                new_card = new_card - 1
        counter += 1
        card = check_card(new_card, state, player_name)
    return new_card    
