# -*- coding: utf-8 -*-

import random
from collections import namedtuple

def pack():
    Card = namedtuple('Card', ['rank', 'suit'])
    cards = []
    for i in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
        for suit in ['♠', '♣', '♥', '♦']:
            cards.append(Card(i, suit))
    while cards:
        yield cards.pop(random.randrange(0, len(cards)))
        
def print_card(card):
    Card = namedtuple('Card', ['rank', 'suit'])
    suit = card.suit
    rank = str(card.rank)
    if rank == '11': rank = 'J'
    if rank == '12': rank = 'Q'
    if rank == '13': rank = 'K'
    if rank == '14': rank = 'A'
    return Card(rank, suit)
    
def print_pile(station):
    output = ''
    for i in station.pile:
        a = print_card(i)
        output = output + str(a.rank) + str(a.suit) + ' '
    return output

class station():
    def __init__(self):
        self.pile = []
    
    def add(self, card):
        self.pile.append(card)
        
    def remove(self):
        return self.pile.pop()
    
    def suit(self):
        if self.not_empty(): return self.pile[-1].suit
        else: return None
    
    def rank(self):
        if self.not_empty(): return self.pile[-1].rank
        else: return None
        
    def not_empty(self):
        if self.pile: return True
        return False
        
    def __len__(self):
        return len(self.pile)
        
    def __lt__(self, compare): 
        # less than only makes sense if it is the same suit
        if self.not_empty() and compare.not_empty():
            assert(self.pile[-1].suit == compare.suit())
            if self.pile[-1].rank < compare.rank():
                return True
            else: return False
        else: raise Exception("Less than on empty value")
    
    def __eq__(self, compare):
        if self.not_empty() and compare.not_empty():
            if self.pile[-1].suit == compare.suit():
                return True
            else: return False
        else: raise Exception("Equal on empty value")
        
    def __str__(self):
        if self.pile: return str(self.pile[-1].rank) + str(self.pile[-1].suit)
        return None

def move_candidate(s1, s2, s3, s4):
    candidates = [s1, s2, s3, s4]
    candidates2 = [x for x in candidates if len(x) > 1]
    if len(candidates2) == 0: return None
    max = 0
    candidate = None
    for i in candidates2:
        if i.rank() > max:
            max = i.rank()
            candidate = i
    return candidate
        
def game(verbose = False, stats_mode = False):
    discard = station()
    cards = pack()
    stations = [station(), station(), station(), station()]
    for _i in range(0, 52, 4):
        stations[0].add(next(cards))
        stations[1].add(next(cards))
        stations[2].add(next(cards))
        stations[3].add(next(cards))
        
        while True:
            change_flag = 0
            for compare in [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]:
                if verbose: print(compare)
                if stations[compare[0]].not_empty() and stations[compare[1]].not_empty():
                    if verbose: print(print_pile(stations[compare[0]]))
                    if verbose: print(print_pile(stations[compare[1]]))
                    if stations[compare[0]] == stations[compare[1]]:
                        if verbose: print("Same suit")
                        change_flag = 1
                        if stations[compare[0]] < stations[compare[1]]:
                            discard.add(stations[compare[0]].remove())
                            if verbose: print("Discarding first comparator")
                        else:
                            discard.add(stations[compare[1]].remove())
                            if verbose: print("Discarding second comparator")
        
            # if any are empty, replace with highest from somewhere else   
            for i in stations:
                if len(i) == 0:
                    can = move_candidate(stations[0], stations[1], stations[2], stations[3])
                    if can is not None:
                        i.add(can.remove())
                        change_flag = 1
            if change_flag == 0: break 
        
    if verbose: print("++ END ++")
    if stats_mode:
        if len(discard) == 48: return 1
        return 0
    for i in stations:
        print(print_pile(i))
            
    print("Size of discard", len(discard))

def statistics(count):
    results = []
    for i in range(0, count):
        results.append(game(stats_mode=True))
    total = sum(results)
    length = len(results)
    if total == 0: raise Exception("No successful run in results")
    mean = total/length
    print("successes:", total)
    print("number of runs", length)
    print("mean:", mean)
