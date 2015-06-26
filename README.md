# Jujutsu

Jujutsu is a game is played by two opponents, each
starting with cards numbering from 1 to 13. There are also 13 treasure cards, 
also numbered from 1 to 13. (Clearly, this game can be played with three suits
of a standard deck of cards.) The treasures are shuffled, and revealed one at a
time. After each treasure is revealed, each player selects one card; they are
revealed at the same time. The higher card wins the treasure, unless a 1 and a
13 are played, in which case the 1 wins. If two cards with the same number are 
played, nobody gets the treasure. At the end of the game, the player with the 
most treasure points wins.

This is a coding assignment for students with around one year's experience in 
Python.

## Card Chooser

The card chooser function is the heart of the assignment: this is a Python 
function which is passed two arguments: a state object and this player's name, 
and which returns an integer representing the player's choice. The rest of the 
framework is provided; students' task is to write their own card chooser 
function. Once this is done, they can start a server which plays this function. 

## The State Object

treasure: the integer value of this turn's treasure  
history: an array of turn objects (earliest turn first), each containing the following keys  
    playerOneName: the integer value of the card this player played  
    playerTwoName: the integer value of the card the opponent played  
    treasure: the integer value of the turn's treasure

Here is an example state object:

    {
        "treasure": 4,
        "history": [
            {
                "treasure": 6,
                "Polly": 12,
                "Molly": 5
            },
            {
                "treasure": 11,
                "Polly": 11,
                "Molly": 10
            }
        ]
    }

## Helper functions

It will be good to build a shared library of helper functions for commonly-performed
tasks. For example, players will almost always want to figure out what cards they
still have in their hands; to do this they will need to iterate through the state
history to figure out what has already been played.

## Prerequisites

* Need to understand lists, dicts, and functions well
* Functions as arguments to other functions
* deconstructing large project into smaller projects
* Error handling?
* Types, particularly ints vs strings
* Allowing computers to interact with each other will be new and exciting.
