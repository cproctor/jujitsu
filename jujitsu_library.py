import random
from flask import Flask, request
import requests
import json

def jujitsu(playerOne, playerTwo, nameOne, nameTwo):
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
		
        playerTwoChoice = playerTwo(state, nameTwo)
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
        
def is_valid_play(playerName, playerChoice, state):
	hand = cards(playerName, state['history'])
	if playerChoice in hand:
		return True
	else:
		message = "GAME OVER: {} made an illegal play: {}."
		print(message.format(playerName, playerChoice))
	
def choose_random(state, player):
    myCards = cards(player, state['history'])
    return random.choice(myCards)

def usually_choose_treasure(state, player):
    myCards = cards(player, state['history'])
    if state['treasure'] in myCards and random.random() < 0.6:
        return state['treasure']
    else: 
        return random.choice(myCards)

def human_player(state, player):
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

def cards(player, history):
    possibleCards = range(1, 14)
    for eachTurn in history:
        possibleCards.remove(eachTurn[player])
    return possibleCards

def winning_card(cardOne, cardTwo):
    cards = sorted([cardOne, cardTwo])
    if cards[0] == 1 and cards[1] == 13:
        return 1
    if cardOne == cardTwo:
        return None
    return cards[1]

def jujitsu_server(chooser):
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
    #app.run(host="0.0.0.0", port=port, debug=True)

def create_remote_player(url, port):
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
        
