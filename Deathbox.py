from tkinter import *
from PIL import Image #Import Pillow for Image.open
from PIL import ImageTk
import random

#Prompt user for entry
def promptnEntry(string):
    #variable to wait for
    button_pressed = StringVar()

    #initialize prompt, entry box and enter button
    prompt = Label(root, text = string, width=30, height=5)
    userInput = Entry(root, width=10)
    button = Button(root, text="Enter", command=lambda: button_pressed.set("button pressed"))

    #place prompt entry box and button
    prompt.place(x=0,y=0)
    button.place(x=600,y=27)
    userInput.place(x=530,y=30)

    #wait for input
    button.wait_variable(button_pressed)

    #Save input to val then clear the entry box
    val = userInput.get()
    userInput.delete(first=0,last=len(val))

    #Clean up
    button.destroy()
    prompt.destroy()
    userInput.destroy()

    return val


def promptnGuess(string, table):

    #Figure out the card to make a guess on
    location=IntVar()
    prompt = Label(root, text = string, width=30, height=5)
    prompt.place(x=0,y=0)
    updateLabel(string, prompt)

    images = []
    cards = []

    for i in range(0,9):
        images.append(table.updateCards(i))
        cards.append(0)

        #cards.append(Button(root, image=images[i], command=lambda: location.set(i)))
        
    cards[0] = Button(root, image=images[0], command=lambda: location.set(0))
    cards[1] = Button(root, image=images[1], command=lambda: location.set(1))
    cards[2] = Button(root, image=images[2], command=lambda: location.set(2))
    cards[3] = Button(root, image=images[3], command=lambda: location.set(3))
    cards[4] = Button(root, image=images[4], command=lambda: location.set(4))
    cards[5] = Button(root, image=images[5], command=lambda: location.set(5))
    cards[6] = Button(root, image=images[6], command=lambda: location.set(6))
    cards[7] = Button(root, image=images[7], command=lambda: location.set(7))
    cards[8] = Button(root, image=images[8], command=lambda: location.set(8))

    for i in range(0,9):
        #Figures out positioning of button based on index
        x=10+(i%3)*220
        r = i-i%3
        y=100+(r/3)*250
        
        cards[i].place(x=x,y=y)


    root.wait_variable(location)
    print(location.get())

    #Make guess on the card
    guess = IntVar()
    updateLabel("Higher, Lower or Equal?", prompt)

    buttons = [0, 0, 0]
    buttons[0] = Button(root, text='Higher', width=8, command=lambda: guess.set(1))
    buttons[1] = Button(root, text='Equal', width=8, command=lambda: guess.set(0))
    buttons[2] = Button(root, text='Lower', width=8, command=lambda: guess.set(-1))

    for i in range(0,3):
        r = location.get() % 3
        col = r
        row = int((location.get() - r) / 3)
        x = 164+220*col
        y = 150+250*row+i*50
        buttons[i].place(x=x,y=y)

    root.wait_variable(guess)

    #Cleanup
    buttons[0].destroy()
    buttons[1].destroy()
    buttons[2].destroy()
    for i in range(0,9):
        cards[i].destroy()

    prompt.destroy()

        
    return [location.get(), guess.get()]


def updateLabel(newText, label):
    label.config(text = str(newText))

    

####### CARD GAMES #######

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

    def deathboxPlay(self, deathbox, deck, plist, prompt):
        #Figure out and initialize all players

        #Game starts
        while(deck.cards):
            for player in plist:

                string = ''
                if (len(plist) > 1):
                    string = player.name + "'s turn! Make a guess!"
    
                i = 0
                before = 0
                after = 0
                
                while(i < 3):
                    if (string == (player.name + "'s turn! Make a guess!")):
                        guess = promptnGuess(string, self)
                        string = ''
                    elif ((i == 0) and (before > after)):
                        guess = promptnGuess("Wrong! "+player.name+', try again!', self)
                    elif (i == 0):
                        guess = promptnGuess(player.name+', make a guess!', self)
                    else:
                        guess = promptnGuess("Correct! "+player.name+', make another guess!', self)
                        
                    self.location = guess[0]
                    self.guess = guess[1]
                    correct = self.check(self.location, self.guess, deck)
                    if(correct == 69):
                        break
                    elif(correct):
                        i += 1
                    else:
                        before = player.score
                        player.score -= len(self.deathbox[self.location]) - 1
                        self.scoreboard(plist)
                        after = player.score
                        i = 0

        updateLabel('',prompt)
        prompt = Label(root, text = 'FINAL SCORE!')
        prompt.place(x=300,y=20)
        self.scoreboard(plist)


    def updateCards(self, location):
        #figure out card at given location on top of deck
        #then convert to file name for searching
        fileName = str(self.deathbox[location][-1])
        fileName = fileName.replace(" ", "_").lower()

        #Append the base address
        baseAddress = r'Cards/'
        newAddress = baseAddress + fileName + '.png'
        image = Image.open(newAddress)

        #Resize the image using resize() method
        image = image.resize((150, 218))
        image = ImageTk.PhotoImage(image)
        return image

        
    def check(self, location, guess, deck):
        card = deck.deal()
        result = False
        
        before = self.deathbox[location][-1].value
        self.deathbox[location].append(card)
        if(deck.cards):
            after = self.deathbox[location][-1].value
        else:
            return 69
        
        if(guess == 1):  #Player guessed higher
            if(after > before):
                result = True
        elif(guess == 0):
            if(after == before):
                result = True
        elif(guess == -1):
            if(after < before):
                result = True
        return result


    def scoreboard(self, list):
        i=0
        scoreboards = []
        for player in list:
            text = player.name + "'s score: " + str(player.score)
            scoreboards.append(Label(root, text=text, width=30, height=1))
            scoreboards[i].place(x=400,y=20*i)
            i += 1



########## GUI SECTION #########

if __name__ == "__main__": 

    root = Tk()
    root.title('Card Games!')
    root.geometry('675x850')
    root.resizable('False','False')
    myDeck = Deck()
    myTable = Table(myDeck)
    myTable.deathboxGame(myDeck)

    prompt = Label(root, text = '', width=30, height=5)
    prompt.place(x=0,y=0)

    players = []
    num = promptnEntry("How many people are playing? (1-6)")
    numplayers = int(num)
    for i in range(0, numplayers):
        string = "Who is Player " + str(i+1) + "?"
        players.append(Player(promptnEntry(string)))
        
    myTable.deathboxPlay(myTable.deathbox, myDeck, players, prompt)
    root.mainloop()











