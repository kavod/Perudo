import numpy as np
import math

from PerudoExcept import *

MAX_PLAYERS = 6
MAX_DICES = 5

class PerudoGame(object):
    def __init__(self,nb_players):
        if not isinstance(nb_players, int):
            raise Exception("nb_players must be an integer")
        if nb_players < 2 or nb_players > MAX_PLAYERS:
            raise Exception("nb_players must be between 2 and " + str(MAX_PLAYERS))
        self.nb_players = nb_players
        self.nb_dices = [MAX_DICES]*self.nb_players
        for i in range(MAX_PLAYERS-nb_players):
            self.nb_dices.append(0)
        self.turn = 0
        self.lastPredict = (0,0)
        self.roll()
    
    def isDead(self,player_id):
        return self.nb_dices[player_id]<1
    
    def count(self,val):
        nb_dices = np.sum(self.dices == val)
        if not self.PerIsPer:
            nb_dices = nb_dices + np.sum(self.dices == 1)
        return nb_dices
    
    def roll(self):
        self.PerIsPer = ( self.nb_dices[self.turn] == 1 )
        self.dices = np.random.randint(low=1,high=7,size=(MAX_PLAYERS,MAX_DICES))
        for i in range(MAX_PLAYERS):
            if self.isDead(i):
                self.dices[i]=0
            else:
                self.dices[i,self.nb_dices[i]:]=0
        self.start = True
    
    def isOver(self):
        if sum(i > 0 for i in self.nb_dices)<2:
            for winner in range(self.nb_players):
                if self.nb_dices[winner]>0:
                    raise PerudoWinner("Player " + str(winner)+" wins",winner)
        
    
    def next(self):
        self.isOver()
        next_turn = (self.turn + 1)%6
        while self.isDead(next_turn):
            next_turn = (next_turn + 1)%6
        return next_turn
    
    def prev(self):
        self.isOver()
        prev_turn = (self.turn - 1)%6
        while self.isDead(prev_turn):
            prev_turn = (prev_turn - 1)%6
        return prev_turn
    
    def possiblePlay(self,max_inc=1,init=1):
        result = []
        minVal = 1 if self.PerIsPer else 2
        if not self.start:
            result.append({"nb":0,"val":0,"no":True,"pile":False})
            result.append({"nb":0,"val":0,"no":False,"pile":True})
            if self.lastPredict[1]>1 or self.PerIsPer:
                for i in range(self.lastPredict[1]+1,7):
                    result.append({"nb":self.lastPredict[0],"val":i,"no":False,"pile":False})
                for i in range(1,max_inc+1):
                    for j in range(minVal,7):
                        result.append({"nb":self.lastPredict[0]+i,"val":j,"no":False,"pile":False})
                if not self.PerIsPer:
                    result.append({"nb":math.ceil(self.lastPredict[0]/2),"val":1,"no":False,"pile":False})
            else:
                for i in range(1,max_inc+1):
                    for j in range(minVal,7):
                        result.append({"nb":self.lastPredict[0]*2+i,"val":j,"no":False,"pile":False})
                result.append({"nb":self.lastPredict[0]+1,"val":1,"no":False,"pile":False})
        else:
            for i in range(1,math.ceil(sum(self.nb_dices)/2)+1):
                for j in range(minVal,7):
                    result.append({"nb":i,"val":j,"no":False,"pile":False})
        return result
    
    def lost(self,player_id):
        self.nb_dices[player_id] = self.nb_dices[player_id]-1
        self.turn = player_id
        if self.isDead(player_id):
            self.turn = self.next()
    
    def play(self,nb=0,val=0,no=False,pile=False):
        if self.start and (no or pile):
            raise Exception("No prediction")
        if not no and not pile:
            if not isinstance(nb, int):
                raise Exception("nb must be an integer")
            if nb < 1:
                raise Exception("nb must be greater than 1")
            if not isinstance(val, int):
                raise Exception("val must be an integer")
            if val < 1 or val > 6:
                raise Exception("val must be between 1 and 6")
            if self.start:
                if val == 1 and not self.PerIsPer:
                    raise Exception("Perudo cannot be played as first choice")
            else:
                if not self.PerIsPer and self.lastPredict[1] == 1 and val > 1: # Perudo to normal
                    minNb = self.lastPredict[0]*2 + 1
                    if nb < minNb:
                        raise Exception("val must be at least " + str(minNb))
                elif not self.PerIsPer and self.lastPredict[1] > 1 and val == 1: # normal to Perudo
                    minNb = math.ceil(self.lastPredict[0]/2)
                    if nb < minNb:
                        raise Exception("val must be at least " + str(minNb))
                else:
                    if nb < self.lastPredict[0]:
                        raise Exception("nb must be at least " + str(self.lastPredict[0]))
                    elif nb == self.lastPredict[0] and val <= self.lastPredict[1]:
                        raise Exception("nb must be at least " + str(self.lastPredict[0] + 1) + " for val " + str(val))
            self.lastPredict = (nb,val)
            self.turn = self.next()
            self.start = False
        elif pile:
            if np.sum(self.dices == self.lastPredict[1]) == self.lastPredict[0]:
                self.nb_dices[self.turn] = min(self.nb_dices[self.turn]+1,MAX_DICES)
            else:
                self.lost(self.turn)
                #self.nb_dices[self.turn] = self.nb_dices[self.turn]-1
                #if self.isDead(self.turn):
                #    self.turn = self.next()
            self.roll()
        elif no:
            if self.count(self.lastPredict[1]) > self.lastPredict[0]:
                self.lost(self.turn)
                #self.nb_dices[self.turn] = self.nb_dices[self.turn]-1
                #if self.isDead(self.turn):
                #    self.turn = self.next()
            else:
                self.lost(self.prev())
                #self.nb_dices[self.prev()] = self.nb_dices[self.prev()]-1
                #if not self.isDead(self.prev()):
                #    self.turn = self.prev()
            self.roll()
        self.isOver()