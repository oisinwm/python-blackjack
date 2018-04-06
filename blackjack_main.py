import itertools
import random
import time
# imports required libraries

class Card:
    def __init__(self, cardCode):
        self.code = cardCode
        self.name = ""
        self.value = 0
        self.meta = ""

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
            self.value = "A"
            # sets the value of an ace to A, so it can be decided to be 1 or 11 later
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


class Deck:
    def __init__(self, decks=1):
        suits = "cdhs"  # sets the four suits
        ranks = "A23456789TJQK"  # sets each possible rank
        cards = list("".join(card) for card in itertools.product(suits, ranks))
        self.deck = []
        for d in range(decks):
            for i in cards:
                self.deck.append(Card(i))
        # print(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop(0)

    def __str__(self):
        return str(self.deck)

    def __repr__(self):
        return str(self.deck)


class Player:
    def __init__(self, name, dealer_name, payed):
        self.name = name
        self.dealer_name = dealer_name
        self._hand = []
        self._hand_value = 0
        self.credit = payed
        self.bet = 0
        self.bust = False

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
            self.hand_value = sum(values)
            # if there are no aces to decide, return the value of the hand
        else:
            aces = values.count("A")
            values = [x for x in values if x != "A"]  # Removes the aces from the list of values
            self.hand_value = sum(values)  # hand value is the sum of the value of the cards within
            if self.hand_value <= (11-aces):
                self.hand_value += (11 + (aces - 1))
            else:
                self.hand_value += aces

    @property
    def hand_value(self):
        return self._hand_value

    @hand_value.setter
    def hand_value(self, val):
        self._hand_value = val
        if self._hand_value > 21:
            self.bust = True
            print(f"{self.name} has gone bust")
        else:
            self.bust = False

    def hit(self, num=1, silent=False):
        for i in range(num):
            command = self.dealer_name + ".deck.draw()"
            card = eval(command)
            if not silent:
                print(f"{self.name} draws a {card}")
            self.hand += [card]

    def stand(self):
        pass

    def make_bet(self, amount):
        self.bet = amount
        self.credit -= amount

    def return_cards(self):
        pseudo_hand = self.hand
        self.hand = []
        return pseudo_hand

    def __str__(self):
        return f"(Name: {self.name}, Hand: {self.hand}, Credits: {self.credit})"

    def __repr__(self):
        return f"(Name: {self.name}, Hand: {self.hand}, Credits: {self.credit})"


class Human(Player):
    def __init__(self, name, dealer_name, payed):
        Player.__init__(self, name, dealer_name, payed)

    def place_bet(self):
        print(f"{self.name} you have {self.credit} Credits to bet")
        amount = int(input("How much would you like to bet on this round?\n"))
        if amount > self.credit:
            print("You can't bet more Credits than you have\n")
            self.place_bet()
        elif amount < 50:
            print("You must bet at least 50 Credits to play\n")
            self.place_bet()
        else:
            print(f"{self.name} bets {amount}")
            self.make_bet(amount)

    def take_turn(self):
        action = input("\nChoose your action: Hit or Stand\n")  # takes the user's input
        if action.upper() == "HIT":
            self.hit()  # if the player hits, hit their hand
            print(f"{self.name}'s new hand value: {self.hand_value}")
            if not self.bust:
                self.take_turn()  # if they aren't bust, lets them take another action
        elif action.upper() == "STAND":  # if the player stands,
            print(f"{self.name} chooses to stand")  # tells the player their action
        else:
            print("Invalid action, Hit or Stand")
            self.take_turn()


class Dealer(Player):
    def __init__(self, instance_name, delay=1):
        Player.__init__(self, instance_name, "self", 0)
        self.deck = []
        self.humans = []
        self.comps = []
        self.allPlayers = []
        self.delay = delay

    def game_setup(self):
        num_deck = int(input("How many decks do you want to play with?\n"))
        self.deck = Deck(num_deck)
        self.deck.shuffle()
        num_h_player = int(input("How many human players?\n"))
        # num_c_player = input("How many computer players?\n")
        for i in range(num_h_player):
            nm = input(f"Enter player {i+1} name: ")
            cr = int(input(f"Enter player {nm} credits: "))
            self.humans.append(Human(nm, self.name, cr))
        # for i in range(num_c_player):
        #    self.comps.append()
        self.allPlayers = self.humans + self.comps
        random.shuffle(self.allPlayers)
        print(f"\nOrder of play: {', '.join([x.name for x in self.allPlayers])}")
        self.game_start()

    def game_start(self):
        stop = False
        roundNumber = 0
        while not stop:
            self.round_bet(roundNumber)
            self.round_play(roundNumber)
            self.round_score()
            roundNumber += 1
            check = input("\nPlay another round? (y/n)")
            if "n" in check.lower():
                stop = True

    def round_bet(self, number):
        print(f"\nRound {number} betting\n")
        offset = number % len(self.allPlayers)
        for i in range(len(self.allPlayers)):
            current = (offset + i) % len(self.allPlayers)
            if type(self.allPlayers[current]) == Human:
                print(f"\n{self.allPlayers[current].name}, place your bet.")
                self.allPlayers[current].place_bet()
            else:
                pass  # No AI yet

    def round_play(self, number):
        print(f"\nRound {number} play\n")
        offset = number % len(self.allPlayers)
        for x in range(2):
            for i in range(len(self.allPlayers)):
                current = (offset + i) % len(self.allPlayers)
                self.allPlayers[current].hit()
                time.sleep(self.delay)
            print()
            time.sleep(self.delay)
        print()
        for p in self.allPlayers:
            print(f"{p.name}: {p.hand_value}")

        self.hit(2, True)
        print(f"\nDealer shows a {self.hand[0]}")

        for i in range(len(self.allPlayers)):
            current = (offset + i) % len(self.allPlayers)
            if type(self.allPlayers[current]) == Human:
                print(f"\n{self.allPlayers[current].name}'s turn,"
                      f" their current hand: {self.allPlayers[current].hand_value}")
                self.allPlayers[current].take_turn()
            else:
                pass  # No AI yet

        print(f"\nDealer reveals a {self.hand[1]}")
        print(f"Dealer's hand value: {self.hand_value}")
        self.dealer_turn()
        self.round_score()

        for p in self.allPlayers:
            self.deck.deck += p.return_cards()
        self.deck.deck += self.return_cards()
        self.deck.shuffle()

    def dealer_turn(self):
        if self.hand_value < 17:
            print("The dealer hits")
            self.hit()
            self.dealer_turn()
        else:
            print("The dealer stands")

    def round_score(self):
        if self.bust:  # If dealer is bust, all non bust players win
            for p in self.allPlayers:
                if p.bust:
                    print(f"{p.name} loses their bet3")
                    self.credit += p.bet
                    p.bet = 0
                else:
                    if p.hand_value == 21 and len(p.hand) == 2:
                        print(f"{p.name} has a Blackjack. They win 2.5x their bet2")
                        p.credit += p.bet * 2.5
                        self.credit -= p.bet * 2.5
                        p.bet = 0
                    else:
                        print(f"{p.name} doubles their bet2")
                        p.credit += p.bet * 2
                        self.credit -= p.bet * 2
                        p.bet = 0
        else:
            for p in self.allPlayers:
                if p.bust:
                    print(f"{p.name} loses their bet2")
                    self.credit += p.bet
                    p.bet = 0
                else:
                    if p.hand_value == self.hand_value:
                        print(f"{p.name} matches the dealer, bet returned")
                        p.credit += p.bet
                        p.bet = 0
                    elif p.hand_value > self.hand_value:
                        if p.hand_value == 21 and len(p.hand) == 2:
                            print(f"{p.name} has a Blackjack. They win 2.5x their bet1")
                            p.credit += p.bet * 2.5
                            self.credit -= p.bet * 2.5
                            p.bet = 0
                        else:
                            print(f"{p.name} doubles their bet1")
                            p.credit += p.bet * 2
                            self.credit -= p.bet * 2
                            p.bet = 0
                    else:
                        print(f"{p.name} loses their bet1")
                        self.credit += p.bet
                        p.bet = 0
