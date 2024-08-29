# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:36:47 2024

@author: lundy
"""

import random
import json
import os


#The Card class establishes the values of the user's cards, it gives an Ace a value of 11.  
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        if rank == "A":
            self.value = 11
        elif rank == "J" or rank == "Q" or rank == "K":
            self.value = 10
        else:
            self.value = int(rank)

#String that the graphics will be printing from.
    def __str__(self):
        return f".-----.\n| {self.rank:<2}  |\n|  {suits_art[self.suit]}  |\n|     |\n|  {self.rank:>2} |\n'-----'"

# CardDeck class is used to generate cards for the user from a standard deck of cards.      
class CardDeck:
    def __init__(self):
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.deck)

    def dealing(self, number):
        cards_dealt = []
        for x in range(number):
            cards_dealt.append(self.deck.pop())
        return cards_dealt

#The Player class gives the user their cards and directs them through the game
class Player:
    def __init__(self):
        self.player_cards = []
        self.player_value = 0
        self.deck = CardDeck()
        self.money = 500
        self.wager = 0

    def calculate_value(self):
        return sum(card.value for card in self.player_cards)

    def start(self):
        self.deck.shuffle()
        self.player_cards = self.deck.dealing(2)

        print("Your cards are: ")
        for card in self.player_cards: 
            print(card)
        print("Your current card value is:", self.calculate_value())

        self.place_wager()

        continue_round = True
        choice = ""
        while self.calculate_value() < 21 and choice not in ["stand", "surrender"] and continue_round:
            choice = input("Enter 'hit', 'stand', or 'surrender': ").lower()
            if choice == 'hit':
                self.player_cards.extend(self.deck.dealing(1))
                print("You now have:")
                for card in self.player_cards:
                    print(card)
                print("Your new value is", self.calculate_value())
            elif choice == 'stand':
                print()
                break
            elif choice == 'surrender':
                print("You have surrendered")
                self.money -= self.wager // 2
                continue_round = False  # End the round immediately
                return 1

        # Dealer's turn if the player didn't surrender
        # if continue_round:
        #     dealer_turn = Dealer(self.deck)
        #     dealer_turn.start()
        return 0

    def place_wager(self):
        while True:
            try:
                self.wager = int(input(f"You have ${self.money}. Place your wager (minimum $5): "))
                if 5 <= self.wager <= self.money:
                    break
                else:
                    print("Invalid wager. Please enter a valid amount.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

#The Dealer class gives the dealer cards as long as the value does not exceed 17 and tells the user what cards the dealer has
class Dealer:
    def __init__(self, deck):
        self.dealer_cards = []
        self.dealer_value = 0
        self.deck = deck

    def calculate_dvalue(self):
        return sum(card.value for card in self.dealer_cards)

    def start(self):
        print()
        print("Dealer's turn: ")
        while self.calculate_dvalue() < 17:
            self.dealer_cards.extend(self.deck.dealing(1))
            print("The dealer hit and has:")
            for card in self.dealer_cards: 
                print(card)
        print("\nDealer has a total value of:", self.calculate_dvalue())

#The check_winner function calculates the total value of player and dealer and prints who won the round  
def check_winner(player, dealer):



    player_value = player.calculate_value()
    dealer_value = dealer.calculate_dvalue()

    if player_value > 21:
        print("\nYou've busted! Dealer wins.")
        player.money -= player.wager
    elif dealer_value > 21:
        print("\nDealer busts. You win!")
        player.money += player.wager * 2
    elif player_value > dealer_value:
        print("\nYou win!")
        player.money += player.wager
    elif dealer_value > player_value:
        print("\nDealer wins.")
        player.money -= player.wager
    else:
        print("\nIt's a tie.")

def init(username):
    if not os.path.isfile("users.json"):  # if it doesn't exist, make the file
        print("No file found")
        with open("users.json", "w+") as f:
            f.write(json.dumps([]))

    with open("users.json", "r") as f:
        users = json.load(f)

    jsonuser = -1
    for i in users:
        if i["username"] == username:
            jsonuser = i
    if jsonuser != -1:
        pinput = input("Please enter your pin: ")
        if pinput == jsonuser["pin"]:
            print("Successfully logged in.")
            player = Player()
            player.money = jsonuser["money"]  # Update the player's money
            return player
        else:
            print("Incorrect")
            exit(1)
    else:
        pinput = input("New user detected. Please enter a pin.")
        newuser = {
            "username": username,
            "pin": pinput,
            "money": 500
        }
        users.append(newuser)
        with open("users.json", "w") as outfile:
            json.dump(users, outfile)
        return Player()

def savedata(username, money):
    with open("users.json","r") as f:
        users = json.load(f)
        for i in users:
            if (i["username"]==username):
                i["money"] = money
        
    with open("users.json","w") as outfile:
        json.dump(users, outfile)



if __name__=='__main__':

    suits_art = {'Hearts': '♥', 'Spades': '♠', 'Clubs': '♣', 'Diamonds': '♦'}
    
    user = input("Please enter a username: ")
    player_turn = init(user)
    
    # this portion of code establishes how many rounds will be played and prints the classes/functions   
    rounds = 0
    while rounds <= 0:
        rounds = int(input("How many rounds would you like to play? "))
    
    game_number = 0
    while game_number < rounds:
        game_number += 1
        print(f"Round {game_number} of {rounds}:")
        dealer_turn = Dealer(player_turn.deck)
        retcode = player_turn.start()
        if (retcode == 0):
            dealer_turn.start()
            check_winner(player_turn, dealer_turn)
        print(f"Player's remaining money: ${player_turn.money}")
        print("*" * 30)
    print("Saving money...")
    savedata(user, player_turn.money)
    
    





