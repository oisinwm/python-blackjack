import itertools, random, time #imports required libraries

class Blackjack:
    deck = [] #sets the variable deck

    pHand = [] #sets the player's empty hand
    dHand = [] #sets the dealer's empty hand

    pCredit = 100 #sets the player's starting credit
    pBet = 0
    #dCredit = 10000 #sets the credit for the dealer, currently unused
    def deal(self): # deals ths hand by taking two random cards from the deck and removing them, does this for both the player and the dealer
        self.pHand = random.sample(self.deck, 2)
        self.deck = [x for x in self.deck if x not in self.pHand]
        self.dHand = random.sample(self.deck, 2)
        self.deck = [x for x in self.deck if x not in self.dHand]
        #print(self.pHand) #debugging
        #print(self.dHand) #debugging

    def card(self, toCheck): #checks a card and returns its printable name
        toCheck = list(toCheck) #splits the card into a list of its features, suit then rank

        if toCheck[0] == "c": #checks the first value to find the card's suit
            cSuit = " of Clubs"
        elif toCheck[0] == "d":
            cSuit = " of Diamonds"
        elif toCheck[0] == "h":
            cSuit = " of Hearts"
        elif toCheck[0] == "s":
            cSuit = " of Spades"

        if toCheck[1] == "T": #checks the second value to find the card's rank
            cRank = "10"
        elif toCheck[1] == "J":
            cRank = "Jack"
        elif toCheck[1] == "Q":
            cRank = "Queen"
        elif toCheck[1] == "K":
            cRank = "King"
        elif toCheck[1] == "A":
            cRank = "Ace"
        else:
            cRank = str(toCheck[1]) #if not a face card, the rank is just the rank

        return cRank + cSuit #returns the printable name of the card

    def value(self, toValue): #checks the value of a card
        toValue = list(toValue) #splits the card into a list of its features, suit then rank
        toValue = toValue[1] #takes only the rank of the card

        if toValue == "T": #sets the value of face cards and ten to be 10
            cValue = 10
        elif toValue == "J":
            cValue = 10
        elif toValue == "Q":
            cValue = 10
        elif toValue == "K":
            cValue = 10
        elif toValue == "A":
            cValue = "A" #sets the value of an ace to A, so it can be decided to be 1 or 11
        else:
            cValue = int(toValue) #if not a face card, the value is just the rank
        return cValue #returns the value

    def handValue(self, hand): #calculates the value of the player's hand
        values = [] #sets the variable values

        for c in hand: #for each card in hand, add the value of that card to a list
            values.append(self.value(c))
        if "A" not in values:
            hValue = sum(values)
            return hValue #if there are no aces to decide, return the value of the hand
        else:
            aces = values.count("A")
            values = [x for x in values if x != "A"] #Removes the aces from the list of values
            hValue = sum(values) #hand value is the sum of the value of the cards within
            if hValue > 10: #if the value of the hand is greater than 10, then each ace must be worth 1
                hValue += aces
                return hValue
            elif hValue <= 10 and aces == 1: #if the value of the hand is <= 10 and there is one ace, the value must be 11
                hValue += 11
                return hValue
            else: #if the value of the hand is less than 10, the first ace must be 11 and all subsequent aces 1
                hValue += 11
                hValue += aces
                return hValue

    def hit(self, hand): #hit and draw a card
        card = random.sample(self.deck, 1)[0]
        hand.append(card) #adds a random card from the deck to hand
        self.deck = [x for x in self.deck if x not in card] #removes said card from the deck
        #print(hand) #debugging

    def bust(self, player):
        if self.handValue(player) > 21: #if the hand value is greater than 21, the hand's owner is bust
            if player == self.pHand: #if it's the player who's gone bust,
                print("\n"*100+"You've gone bust with a hand of:") #shows the player their loosing hand
                for c in self.pHand:
                    print(self.card(c))
                self.again() #checks if they want to play again
            else:
                print("The Dealer has gone bust, you win this round")
                print("You win the round!\nThe value of the dealer's hand was "+str(self.handValue(self.dHand))+" versus your "+str(self.handValue(self.pHand)))
                self.pCredit += self.pBet * 2 #double the bet for winning
                print("\nYou've won "+str(self.pBet*2)+" Credits! You now have "+str(self.pCredit)+" Credits")
                self.again() #checks if they want to play again

    def again(self): #lets the player decide to play another round, or quit
        print("\nPlay another round?")
        again = input("Y/N\n")
        if again.upper() == "Y":
            self.gameStart()
        elif again.upper() == "N":
            print("You leave with "+str(self.pCredit)+" credits") #displays the players leaving credits
            raise SystemExit
        else: #if the input is not 'y' or 'n' ask again
            self.again()

    def computer(self): #handles the dealer's turn, hits on <17 stands on 17
        if self.handValue(self.dHand) < 17: #if the dealer has less than 17, they hit
            print("\nThe dealer hits\n")
            self.hit(self.dHand) #dealer hits
            if self.handValue(self.dHand) < 17: #if the dealer still has less than 17, they hit again
                self.computer()
            else:
                self.bust(self.dHand) # if they are above 17 after hitting, they check if they have gone bust
        else:
            print("\nThe dealer stands\n") #if the dealer is above 17, they stand

    def bet(self): #handles the player's bets
        print("You have "+str(self.pCredit)+" Credits to bet")
        bet = input("How much would you like to bet on this round?\n")
        if int(bet) > self.pCredit:
            print("\n"*100+"You can't bet more credits than you have\n")
            self.bet()
        elif int(bet) < 5:
            print("\n"*100+"You must bet at least 5 Credits to play\n")
            self.bet()
        else:
            self.pBet = int(bet)
            self.pCredit -= self.pBet #takes the players bet form their total credits
            print("\n"*100+"You've placed a bet of "+str(self.pBet)+" Credits on this round\n")

    def gameStart(self):
        suits = "cdhs" #sets the four suits
        ranks = "23456789TJQKA" #sets each possible rank
        self.deck = list("".join(card) for card in itertools.product(suits, ranks)) #generates the starting deck, with each possible card

        print("\n"*100+"The Dealer will always stand on a 17")
        time.sleep(3)
        print("\n"*100)

        self.deal() #starts the round, dealing out 2 cards to the dealer and the player
        self.bet() #takes the player's bet

        print("You are dealt:")
        for c in self.pHand: #shows the player the cards they have been dealt
            print(self.card(c))
        print("Value of your hand: "+str(self.handValue(self.pHand))) #shows the player the value of their hand
        print("\nTotal cards in deck "+str(len(self.deck))+"    Dealer's hand: "+str(len(self.dHand))+" cards") #show the player other information they might want to know

        self.action() #lets the player choose their actions, hit or stand
        self.computer() #the dealer takes their turn, standing on a 17
        self.showdown() #handles the showdown, working out the winner and handing out any relevant prize credits

    def action(self):
        action = input("\nChoose your action: Hit or Stand\n") #takes the user's input
        if action.upper() == "HIT":
            self.hit(self.pHand) #if the player hits, hit their hand
            print("\n"*100+"Your hand is now:")
            for c in self.pHand: #shows the player their new hand
                print(self.card(c))
            print("\nValue of your hand: "+str(self.handValue(self.pHand))) #shows the player their new hand's value
            self.bust(self.pHand) #checks if the player's new hand makes them go bust
            self.action() #if they aren't bust, lets them take another action
        elif action.upper() == "STAND": #if the player stands,
            print("\n"*100+"You choose to stand") #tells the player their action
        else:
            print("\n"*100+"Invalid action, hit or stand") #if they don't choose a correct action, ask them again
            self.action()

    def showdown(self): #for finding the winner of a game
        if self.handValue(self.dHand) < self.handValue(self.pHand): #if the player has a higher valued hand than the dealer, the player wins
            print("You win the round!\nThe value of the dealer's hand was "+str(self.handValue(self.dHand))+" versus your "+str(self.handValue(self.pHand)))
            self.pCredit += self.pBet * 2
            print("\nYou've won "+str(self.pBet*2)+" Credits! You now have "+str(self.pCredit)+" Credits")
        elif self.handValue(self.dHand) > self.handValue(self.pHand): #if the dealer has a higher valued hand than the player, the player loses
            print("You lose the round\nThe value of the dealer's hand was "+str(self.handValue(self.dHand))+" versus your "+str(self.handValue(self.pHand)))
        elif self.handValue(self.dHand) == self.handValue(self.pHand) and self.handValue(self.pHand) != 21: #if the player and the dealer have the same valued hand that isn't 21 it's a push
            self.pCredit += self.pBet #the player gets back their bet
            print("It's a push, the dealer has the same total as you!\nYour bet of "+str(self.pBet)+" Credits has been returned. You now have "+str(self.pCredit)+" Credits")
        elif self.handValue(self.dHand) == 21: #if the dealer has 21
            if self.handValue(self.pHand) != 21: #if the player doesn't have 21
                print("You lose the round\nThe dealer achieved 21") #the player loses
            elif len(self.dHand) < len(self.pHand): #if the player also has 21, but has more cards than the dealer
                print("You lose the round\nThe dealer achieved 21 with less cards than you") #the player loses
            elif len(self.dHand) > len(self.pHand): #if the player also has 21, but has less cards than the dealer
                print("You win the round!\nThe you achieved 21 with less cards than the dealer") #the player wins
                if len(self.pHand) == 2: #if the player also has a natural blackjack
                    self.pCredit += round(self.pBet * 2.5) #they get an extra prize
                    print("\nYou've won "+str(round(self.pBet * 2.5))+" Credits with a natural blackjack! You now have "+str(self.pCredit)+" Credits")
                else:
                    self.pCredit += self.pBet * 2 #else they only have a normal blackjack, a normal prize
                    print("\nYou've won "+str(self.pBet*2)+" Credits! You now have "+str(self.pCredit)+" Credits")
        elif self.handValue(self.pHand) == 21: #if the player has 21, but the dealer doesn't
            if len(self.pHand) == 2: #if the player also has a natural blackjack
                self.pCredit += round(self.pBet * 2.5) #they get an extra prize
                print("\nYou've won "+str(round(self.pBet * 2.5))+" Credits with a natural blackjack! You now have "+str(self.pCredit)+" Credits")
            else:
                self.pCredit += self.pBet * 2 #else they only have a normal blackjack, a normal prize
                print("\nYou've won "+str(self.pBet*2)+" Credits! You now have "+str(self.pCredit)+" Credits")
        else:
            self.pCredit += self.pBet #else it's a push, the player gets back their bet
            print("It's a push, the dealer has the same total as you!\nYour bet of "+str(self.pBet)+" Credits has been returned. You now have "+str(self.pCredit)+" Credits")

        self.again() #checks if they want to play again

game = Blackjack()
game.gameStart() #starts the first round
