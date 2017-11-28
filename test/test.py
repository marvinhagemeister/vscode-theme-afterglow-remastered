import os
import sys
import random
import math
import time

class BadInputError(Exception):
    pass

class Player():

    def __init__(self, name):
        self.id = None
        self.name = name
        self.type = 'Human'
        self.hand = Hand()
        self.legalCards = []
        self.wildCards = []
        self.valueChangeCards = []
        self.zeroCards = []
        self.canSkip = False
        self.canReverse = False
        self.canDrawTwo = False
        self.canDrawFour = False
        self.canValueChange = False
        self.drew = False
        self.scrollMax = 0
        self.points = 0
        self.forceDraw = 0

    def addCard(self, card):
        self.drew = True
        if self.forceDraw > 0:
            self.forceDraw -= 1
            self.drew = False
        self.hand.addCard(card)
        
    def beginTurn(self):
        self.drew = False
        
    def didDraw(self):
        return self.drew
        
    def getLegalCards(self, color, value, zeroChange=False):
        self.canSkip = False
        self.canReverse = False
        self.canDrawTwo = False
        self.canDrawFour = False
        self.canValueChange = False
        self.canZeroChange = False
        self.legalCards = []
        self.wildCards = []
        self.valueChangeCards = []
        self.zeroCards = []
        plusFours = []
        for card in self.hand:
            if card.isWild():
                if card.getValue() == '+4':
                    plusFours.append(card)
                else:
                    self.wildCards.append(card)
            elif zeroChange and card.isZero():
                self.canZero = True
                self.zeroCards.append(card)
            elif card.getColor() == color or card.getValue() == value:
                if card.getColor() != color:
                    self.canValueChange = True
                    self.valueChangeCards.append(card)
                if card.getValue() == "+2":
                    self.canDrawTwo = True
                elif card.getValue() == 'R':
                    self.canReverse = True
                elif card.getValue() == 'X':
                    self.canSkip = True
                self.legalCards.append(card)
        if len(self.legalCards) == 0 and len(plusFours) > 0:
            self.canDrawFour = True
            self.wildCards += plusFours
                
    def getValidCards(self):
        return self.legalCards
    
    def getAllValidCards(self):
        return self.legalCards + self.wildCards + self.zeroCards
                
    def hasLegalCard(self):
        return len(self.legalCards) > 0
        
    def addPoints(self, amount):
        if (self.points + amount) <= 999999999999999999999:
            self.points += amount
        
    def removeCard(self, index):
        return self.hand.removeCard(index)
    
    def assignID(self, identity):
        self.id = identity

    def getName(self):
        return self.name

    def getID(self):
        return self.id
    
    def getPoints(self):
        return self.points

    def getType(self):
        return self.type

    def getCardNum(self):
        return len(self.hand)

    def getHand(self, scrollNum=0, hide=False):
        return self.hand.show(scrollNum, hide)
    
    def getForceDraws(self):
        return self.forceDraw
    
    def addForceDraw(self, num):
        self.forceDraw += num
    
    def decreaseForceDraw(self):
        self.forceDraw -= 1
        
    def removeForceDraw(self):
        self.forceDraw = 0

    def checkCard(self, index):
        return self.hand.getCard(int(index))
    
    def discardHand(self):
        self.hand.discard()
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return '({},{})'.format(self.name, self.points)

class Hand():
    ''''deck' (Deck) : Card's Color (rgby)
       'numberOfCards' (int) : Card's Value (0-9, R, X, W, +2, +4)'''

    def __init__(self, deck=None,numberOfCards=0):
        self.hand = []
        if deck != None:
            self.draw(deck,numberOfCards)

    def __iter__(self):
        return iter(self.hand)

    def __len__(self):
        return len(self.hand)

    def __getitem__(self, item):
        try:
            return self.hand[item]
        except:
            return ''

    def addCard(self, card):
        self.hand.append(card) 
        
    def removeCard(self, index):
        index = int(index)
        if (0 <= index < len(self)):
            return self.hand.pop(index)      

    def discard(self):
        self.hand = []

    def show(self, scrollNum=0, hide=False):
        if scrollNum == -1:
            scrollNum = 0
        output = ''
        num = 0
        header, footer, upper, lower = '', '', '', ''
        header +=   ('\033[97m\u2666--\u2666\033[0m ')
        upper +=    ('\033[97m|<-|\033[0m ')
        lower +=    ('\033[97m|<-|\033[0m ')
        footer +=   ('\033[97m\u2666--\u2666\033[0m ')
        for i in range(10):
            indexNum = i+(10*scrollNum)
            if indexNum < len(self):
                header += (self[indexNum].getRow(0,hide)+' ')
                upper += (self[indexNum].getRow(1,hide)+' ')
        