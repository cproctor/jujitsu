# jujitsu_library.py
# ------------------
# (c) 2014 Chris Proctor
# This code is released under the MIT license. Have fun with it.

import random
from flask import Flask, request
import requests
import json

def jujitsu(playerOne, playerTwo, nameOne, nameTwo):
    "When given two players, plays a jujitsu game"

    treasures = range(1, 14)
    random.shuffle(treasures)
    state = {
        'history': []
    }
    scores = {
        nameOne: 0, 
        nameTwo: 0
    }
    for eachTreasure in treasures:
        print("===========================================")
        state['treasure'] = eachTreasure
        playerOneChoice = playerOne(state, nameOne)
        if not is_valid_play(nameOne, playerOneChoice, state):
            return False
        playerTwoChoice = playerTwo(state, nameTwo)
        if not is_valid_play(nameTwo, playerTwoChoice, state):
            return False
        print("    {} plays {}".format(nameOne, playerOneChoice))
        print("    {} plays {}".format(nameTwo, playerTwoChoice))
        winningCard = winning_card(playerOneChoice, playerTwoChoice)
        if winningCard is None:
            print("Nobody wins the treasure.")
        else:
            if winningCard == playerOneChoice:
                winner = nameOne
            else:
                winner = nameTwo
            scores[winner] += eachTreasure
            print("    {} wins {} points!".format(winner, eachTreasure))
        print("The score is:")
        print("    {}: {}".format(nameOne, scores[nameOne]))
        print("    {}: {}".format(nameTwo, scores[nameTwo]))
        state['history'].append({
            'treasure': eachTreasure,
            nameOne: playerOneChoice,
            nameTwo: playerTwoChoice
        })
        
def jujitsu_server(chooser):
    """Creates a Jujitsu server which will use the provided chooser function 
    to choose cards to play. See start_server.py for an example of how to use 
    this function."""

    app = Flask("Jujitsu Server")
    @app.route('/jujitsu/status')
    def status():
        return "OK"
    @app.route('/jujitsu/<player>')
    def choose(player):
        state = request.get_json(force=True)
        print(state)
        choice = chooser(state, player)
        print "CHOSE {}".format(choice)
        return str(choice)
    return app

# HELPER FUNCTIONS
# ----------------
        
def is_valid_play(playerName, playerChoice, state):
    "When given a player's choice and the state, returns True if the play is legal"
	hand = cards(playerName, state['history'])
	if playerChoice in hand:
		return True
	else:
		message = "GAME OVER: {} made an illegal play: {}."
		print(message.format(playerName, playerChoice))
	
def winning_card(cardOne, cardTwo):
    "When given two cards, returns the winning card. If they are equal, returns None."
    cards = sorted([cardOne, cardTwo])
    if cards[0] == 1 and cards[1] == 13:
        return 1
    if cardOne == cardTwo:
        return None
    return cards[1]

def cards(player, history):
    """ When given a player and a history, returns a list of integers showing 
    which cards the player still has. Most chooser functions will need to use
    this function."""
    possibleCards = range(1, 14)
    for eachTurn in history:
        possibleCards.remove(eachTurn[player])
    return possibleCards

# CARD CHOOSERS
# -------------
# See the readme. A card chooser function receives the game's state and the 
# player's name, and returns the player's choice as an integer 

def choose_random(state, player):
    """ This might be the simplest chooser function--it figures out which cards
    are available and chooses one randomly."""
    myCards = cards(player, state['history'])
    return random.choice(myCards)

def usually_choose_treasure(state, player):
    """ This chooser function usually chooses the same number as the treasure 
    card, but sometimes decides to mix things up and choose a random card 
    instead."""
    myCards = cards(player, state['history'])
    if state['treasure'] in myCards and random.random() < 0.6:
        return state['treasure']
    else: 
        return random.choice(myCards)

def human_player(state, player):
    """ This chooser function asks you what card to play. If you want to play
    against a chooser function, make one of the players a human_player."""
    myCards = cards(player, state['history'])
    print("The treasure card is {}. Your cards are: ".format(state['treasure']))
    print(', '.join([str(card) for card in myCards]))
    while True:
        choice = raw_input("What would you like to play? ")
        if choice.isdigit():
            choice = int(choice)
        if choice in myCards:
            break
        print("Sorry, {} is not an option.".format(choice))
    return choice

def create_remote_player(url, port):
    """ Returns a chooser function which asks another Jujitsu server which cards 
    to play. If you want a game to take place between two different computers, 
    one should be running a server and the other should create a remote player
    which uses the server."""

    def remote_player(state, player):
        fullUrl = url + '/' + player
        headers = {'content-type': 'application/json'}
        data = json.dumps(state)
        print(fullUrl)
        response = requests.get(fullUrl, data=data, headers=headers)
        if response.status_code == 200:
            return int(response.text)
        else: 
            raise Exception("Something went wrong with the remote player: {}".format(response))
    return remote_player
