import itertools
import random
import time  # imports required libraries


class Player:
    def __init__(self, payed=0):
        self._hand = []
        self._hand_value = 0
        self.credit = payed
        self.bet = 0

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, cards):
        self._hand = cards
        values = []
        for c in self._hand:
            values.append(c.value)

        if "A" not in values:
            self._hand_value = sum(values)  # if there are no aces to decide, return the value of the hand
        else:
            aces = values.count("A")
            values = [x for x in values if x != "A"]  # Removes the aces from the list of values
            self._hand_value = sum(values)  # hand value is the sum of the value of the cards within
            if self._hand_value <= (11-aces):
                self._hand_value += (11 + (aces - 1))
            else:
                self._hand_value += aces

    @property
    def hand_value(self):
        return self._hand_value


class Card:
    def __init__(self, cardCode):
        self.code = cardCode
        self.name = ""
        self.value = 0

        codeValue = self.code[1]
        if codeValue == "T":  # sets the value of face cards and ten to be 10
            self.value = 10
        elif codeValue == "J":
            self.value = 10
        elif codeValue == "Q":
            self.value = 10
        elif codeValue == "K":
            self.value = 10
        elif codeValue == "A":
            self.value = "A"  # sets the value of an ace to A, so it can be decided to be 1 or 11 later
        else:
            self.value = int(codeValue)  # if not a face card or 10, the value is just the rank

        if self.code[0] == "c":  # checks the first value to find the card's suit
            suit = " of Clubs"
        elif self.code[0] == "d":
            suit = " of Diamonds"
        elif self.code[0] == "h":
            suit = " of Hearts"
        elif self.code[0] == "s":
            suit = " of Spades"

        if self.code[1] == "T":  # checks the second value to find the card's rank
            rank = "10"
        elif self.code[1] == "J":
            rank = "Jack"
        elif self.code[1] == "Q":
            rank = "Queen"
        elif self.code[1] == "K":
            rank = "King"
        elif self.code[1] == "A":
            rank = "Ace"
        else:
            rank = str(self.code[1])  # if not a face card, the rank is just the rank
        self.name = rank + suit

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
