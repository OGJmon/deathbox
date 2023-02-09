import random
from PIL import Image #Import Pillow for Image.open
from PIL import ImageTk

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    # Implementing build in methods so that you can print a card object
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()
        
    def show(self):
        if self.value == 1:
            val = "Ace"
        elif self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"
        else:
            val = self.value

        return "{} of {}".format(val, self.suit)


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            print(card.show())

    # Generate 52 cards
    def build(self):
        self.cards = []
        for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in range(1,14):
                self.cards.append(Card(suit, val))

    # Shuffle the deck
    def shuffle(self, num=1):
        length = len(self.cards)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]
            # You can also use the build in shuffle method
            # random.shuffle(self.cards)

    # Return the top card
    def deal(self):
        if(self.cards):
            return self.cards.pop()
        else:
            return False


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def sayHello(self):
        print("Hi! My name is {}".format(self.name))
        return self

    # Draw n number of cards from a deck
    # Returns true in n cards are drawn, false if less then that
    def draw(self, deck, num=1):
        for _ in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else: 
                return False
        return True

    # Display all the cards in the players hand
    def showHand(self):
        print("{}'s hand: {}".format(self.name, self.hand))
        return self

    def discard(self):
        return self.hand.pop()

class Table(object):
    def __init__(self, deck, num=1):
        self.deck = deck.shuffle()

    def deathboxGame(self, deck):
        self.deathbox = []
        #Deal out the deathbox!
        for i in range(0, 9):
            self.deathbox.append([])
            card = deck.deal()
            if card:
                self.deathbox[i].append(card)
            else:
                print("There are no cards in the deck")

    def deathboxPlay(self, deathbox):
        #Figure out and initialize all players
        plist = myTable.players()

        #Game starts
        while(myDeck.cards):
            for player in plist:

                if (len(plist) > 1):
                    print("  ")
                    print(player.name + "'s turn!")
                    
                print("  ")
                    
                myTable.show()
                i = 0
                while(i < 3):
                    guess = myTable.makeguess(player.name)
                    if(myTable.check(myTable.location, myTable.guess, myDeck)):
                        i += 1
                    else:
                        player.score -= len(myTable.deathbox[myTable.location]) - 1
                        myTable.scoreboard(plist)
                        i = 0

                if ((player == plist[-1]) and (len(plist) > 1)):
                    myTable.scoreboard(plist)

        
        print("FINAL SCORE!")
        myTable.scoreboard(plist)

    def updateCards(self, location):
        #figure out card at given location on top of deck
        #then convert to file name for searching
        fileName = str(myTable.deathbox[location][-1])
        fileName = fileName.replace(" ", "_").lower()

        #Append the base address
        baseAddress = r'C:/Users/jrh41/Cards/'
        newAddress = baseAddress + fileName + '.png'
        image = Image.open(newAddress)

        #Resize the image using resize() method
        image = image.resize((212, 308))
        image = ImageTk.PhotoImage(image)

        return image

    def makeguess(self, name):
        valid = False
        self.checkval = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        self.checksuit = ['clubs', 'hearts', 'diamonds', 'spades']
        self.checkguess = ['higher', 'lower', 'equal']
        
        # Take card value as input and check if value is valid and present on the table
        while(valid == False):
            
            value = input(name +", what is the value of card you'd like to bet on? ").lower()

            locations = [] # Used for card validation
            
            #Check if input is valid
            if (value in self.checkval):
                value = self.checkval.index(value)
            else:
                print("Input invalid")

            #Check if value is on table
            for i in range(0,9):
                if (value == self.deathbox[i][-1].value - 1):
                    locations.append(i) #save all locations of matched value on table

            if (locations):
                #print(locations)
                valid = True
            else:
                print("This value is not present on the table")

        # Reset for Suit validation  
        valid = False

        # Take suit as input and check if value and suit matches a card on the table
        while(valid == False):
            suit = input(name +", what is the suit of card of the card you'd like to bet on? ").lower()
            for values in locations:

                if (self.deathbox[values][-1].suit.lower() == suit):    #Figure out which instance of value is correct suit
                    location = values                                   #and save location of card on the table
                    valid = True
                    break
                
                elif (values == locations[-1]):
                    print("Input invalid")

        valid = False

        while(valid == False):
            guess = input(name +", will the next card in the deck be higher, lower or equal to the card you picked? ").lower()
            if (guess in self.checkguess):
                valid = True
            else:
                print("Input invalid")

        self.location = location
        self.guess = guess

    def players(self):
        self.plist = []
        numplayers = int(input("How many people are playing?: "))
        
        for i in range(1, numplayers+1):
            name = input("Who is player "+ str(i) +": ")
            self.plist.append(Player(name))

        return self.plist
        
    def check(self, location, guess, deck):
        before = self.deathbox[location][-1].value
        
        card = deck.deal()
        self.deathbox[location].append(card)
        after = self.deathbox[location][-1].value
        result = False
        
        print(" ")
        print("A "+ card.show() +" was pulled!")
        print(" ")

        if (guess == 'higher'):
            if(after > before):
                result = True
                print("Correct!")
            else:
                print("Wrong! start over!")
        elif (guess == 'lower'):
            if(after < before):
                result = True
                print("Correct!")
            else:
                print("Wrong! start over!")
        elif (guess == 'equal'):
            if(after == before):
                result = True
                print("Correct!")
                print(" ")
            else:
                print("Wrong! start over!")
                
        print(" ")
        self.show()
        return result

    def scoreboard(self, list):
        print(" ")
        for item in list:
            print(item.name +"'s score -----> " +str(item.score))
        print(" ")
        
        
            

    def show(self):
        print(self.deathbox[0][-1].show()+ "      " +self.deathbox[1][-1].show()+ "     " +self.deathbox[2][-1].show())
        print(" ")
        print(self.deathbox[3][-1].show()+ "     " +self.deathbox[4][-1].show()+ "     " +self.deathbox[5][-1].show())
        print(" ")
        print(self.deathbox[6][-1].show()+ "     " +self.deathbox[7][-1].show()+ "     " +self.deathbox[8][-1].show())
        print(" ")


myDeck = Deck()
myTable = Table(myDeck)
myTable.deathboxGame(myDeck)
myTable.deathboxPlay(myTable.deathbox)


            
            
