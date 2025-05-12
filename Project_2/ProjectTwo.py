import math
import random
import time

RANKS = '23456789TJQKA'
SUITS = 'HDCS'
state="preflop" #states can be preflop, preturn, pre river, and result
test=0

class GameState:
    # represents thje state of the game which will be present at a node
    def __init__(self, my_hand, community, last_added_card=None):
        self.my_hand = list(my_hand)
        self.community = list(community)
        self.last_added_card = last_added_card

    def possible_next_cards(self):
        #reutrn all cards not in community and hand
        known = set(self.my_hand + self.community)
        #print( "your hand : ", self.my_hand)
        return [r + s for r in RANKS for s in SUITS if (r + s) not in known]

    def add_card(self, card):
        #adds cards to the community adn changes the last 
        self.community.extend(card)
        self.last_added = self.community[-1]

    def can_add_card(self):
        #checks whether you can add another card
        return len(self.community) < 5

class Node:
    #node class for state
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def fully_expanded(self):
        return len(self.children) == len(self.state.possible_next_cards())

    def ucb1(self, c=1.41): #calculation
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

def find_straight(values):
    values = sorted(set(values), reverse=True)
    # check for high-to-low sequences
    for i in range(len(values) - 4):
        if values[i] - values[i + 4] == 4:
            return values[i:i + 5]
    #catching edge case where there is a 5 card straight with an ace
    if set([12, 0, 1, 2, 3]).issubset(values):
        return [3, 2, 1, 0, 12]
    return None


def Simulate(cards):
    #cards are number then suit
    values = sorted([RANKS.index(c[0]) for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    # frequency count
    value_counts = {}
    for v in values:
        #dictionary containing key as vaclue and value as count 
        value_counts[v] = value_counts.get(v, 0) + 1

    items = value_counts.items()
    #sorts the items by value first and then by key for any tie breakers
    card_dict = sorted(items, key=lambda x: (-x[1], -x[0]))
    # print(card_dict)

    flush = False
    for suit in SUITS:            # e.g. 'H','D','C','S'
        count = 0
        for card_suit in suits:  # your list of suits
            if card_suit == suit:
                count += 1
        if count >= 5:
            flush = True
            break
    straight = find_straight(values)

    # hand ranking from highest (9) to lowest (0) 10 hands therefore covers all hands
    if flush and straight:
        if max(straight) == 12:# Royal Flush
            return (9, straight) 
        return (8, straight)# Straight Flush
    if card_dict[0][1] == 4:# four of a kind
        return (7, [card_dict[0][0]])
    if card_dict[0][1] == 3 and len(card_dict) > 1 and card_dict[1][1] >= 2:# full house
        return (6, [card_dict[0][0], card_dict[1][0]])
    if flush:# flush
        return (5, values)
    if straight:# straight
        return (4, straight)
    if card_dict[0][1] == 3:# three of a kind
        return (3, [card_dict[0][0]])
    if card_dict[0][1] == 2 and len(card_dict) > 1 and card_dict[1][1] == 2: # two pair
        return (2, [card_dict[0][0], card_dict[1][0]])
    if card_dict[0][1] == 2:# one pair
        return (1, [card_dict[0][0], card_dict[1][0], card_dict[2][0]])
    return (0, values)# high card

def compare(hand1, hand2):
    #h1 beats h2 true 
    rank1, tie1 = Simulate(hand1)
    rank2, tie2 = Simulate(hand2)
    # print("Rank1: ", rank1)
    # print("Rank2: ", rank2)
    # print("Tie1: ", tie1)
    # print("Tie2: ", tie2)
    if rank1 != rank2:
        return rank1 > rank2
    elif tie1 != tie2:
        return tie1 > tie2
    else:
        return 


def selection(node):
#node.state.can_add_card() and node.fully_expanded() or
    # selects the next node to explore based on UCB1
    if len(node.children) ==  math.perm(50, 3) and state=="preflop":
        node = max(node.children, key=lambda n: n.ucb1())
        
    elif len(node.children) == math.perm(47, 1) and state=="preturn":
        node = max(node.children, key=lambda n: n.ucb1())
        
    elif len(node.children) == math.perm(46, 1) and state=="river":
        node = max(node.children, key=lambda n: n.ucb1())
        
    return node


def expand(node):# this node will always be what you are woring off of, whether that be your hand, or your hand with parrts of the comuntiy in it
    deck=[r + s for r in RANKS for s in SUITS if (r + s)]
    seen=[]
    turn=None
    river=None
    global test
    if  state=="preflop":
        # print("                                                                                ENTERED")
        # print("flop" +str(len(node.state.community)))
        while True:
            card1=deck.pop(random.randrange(len(deck)))
            card2=deck.pop(random.randrange(len(deck)))
            card3=deck.pop(random.randrange(len(deck)))
            if card1!=node.state.my_hand[0] and card1!=node.state.my_hand[1] and card2!=node.state.my_hand[0] and card2!=node.state.my_hand[1] and card3!=node.state.my_hand[0] and card3!=node.state.my_hand[1]:
                break
        flop=GameState(my_hand=node.state.my_hand, community=node.state.community)
        flop.add_card([card1, card2, card3])
        flop_child = Node(flop, parent=node)
        seen.append(card1)
        seen.append(card2)
        seen.append(card3)
        # print("                   CHILDREN COUNTER: ", len(node.children))
        test+=1
        # print("test: ", test)
        node.children.append(flop_child)
        # print("seen cards: ", seen)   
        return flop_child

    elif state=="preflop" or state=="preturn":
        # print("turn" +str(len(node.state.community)))
        while True:
            # print("                                                 "+str(len(deck)))
            card4=deck.pop(random.randrange(len(deck)))
            if card4 not in node.state.community and card4 not in seen and card4 not in node.state.my_hand:
                break

        turn = GameState(my_hand=node.state.my_hand, community=node.state.community)
        turn.add_card([card4]) 
        seen.append(card4)
        turn_child = Node(turn, parent=node)
        node.children.append(turn_child) 
        return turn_child
                
    elif state=="preflop" or state=="preturn" or state=="river":
        # print("river" +str(len(node.state.community)))
        while True:
            card5=deck.pop(random.randrange(len(deck)))
            if card5 not in node.state.community and card5 not in seen and card5 not in node.state.my_hand:
                break
        river = GameState(my_hand=node.state.my_hand, community=node.state.community)
        river.add_card([card5])
        seen.append(card5)
        river_child = Node(river, parent=node)
        node.children.append(river_child)   
        # print("seen cards: ", seen)     
        return river_child
            




    return node

def simulate_random_playout(game_state):
    global state
    # print("Community length ", len(game_state.community[:]))
    known_cards = set(game_state.my_hand + game_state.community)
    deck = []
    # opp=['4D','2H']
    # deck = ['2H', '2D', '2C','3H', '3D', '3C', '3S','4H', '4C', '4S','5H', '5D', '5C', '5S','6H', '6C', '6S','7H', '7C', '7S','8H', '8D', '8S',
    # '9H', '9D', '9C','TH', 'TD', 'TC', 'TS','JC', 'JS','QH', 'QD', 'QC', 'QS','KH', 'KD', 'KC', 'KS','AD', 'AC', 'AS']   
    for r in RANKS:
        for s in SUITS:
            card = r + s
            #and card not in (['9S','JH','4D','8C'])
            if card not in known_cards :
                # and card not in opp 
                deck.append(card)

    opp = [deck.pop(random.randrange(len(deck))), deck.pop(random.randrange(len(deck)))]
    if state=="resultplayout":
        print("opponent hand: ", opp)
    
    if compare(game_state.my_hand + game_state.community, opp + game_state.community):
        return 1  # Win
    else:
        return 0


#this is fine its given in slides
def backpropagate(node, result):
    while node:
        node.visits += 1
        node.wins += result
        node = node.parent


def main():
    global state
    preflop_poss= math.comb(50, 3)
    preturn_poss= math.comb(47, 2)
    river_poss= math.comb(46, 1)
    total_wins=0
    total_visits=0
    #['9S','JH','4D','8C','JD']
    init_state = GameState(my_hand=['2S', '7C'], community=[])
    root = Node(init_state)
    start=time.time()

    #just contains the loop that preforms MCTS
    while time.time()-start< 10 and root.visits < preflop_poss+ preturn_poss+ river_poss:
        if state=="preflop":      
            leaf = selection(root)
            child = expand(leaf)
            result = simulate_random_playout(child.state)
            backpropagate(child, result)
        else:
            child = expand(root)
            result = simulate_random_playout(child.state)
            backpropagate(child, result)
        # print(result)
        # print(str(time.time()-start) +"                             LENGTH OF ROOD>CHILDREN: ", len(root.children))
        if state =="preflop" and len(root.children) >= preflop_poss:
            #for now just hard code flop 
            win_rate = root.wins / root.visits
            total_wins+=root.wins
            total_visits+=root.visits
            print("----------PREFLOP----------")
            print("Total simulations:", root.visits)
            print("Wins:", root.wins)
            print(f"Estimated win rate: {win_rate * 100:.2f}%")
            print("your hand: ", root.state.my_hand)
            
            #assign new root randomly
            flop_root=random.choice(root.children)
            # flop_root.state.community = flop_root.state.community[:2]# only grabs first 3 cards so sets the flop as consistant
            root = flop_root
            print("flop: ", flop_root.state.community)
            state="preturn"

        if state =="preturn" and len(root.children) >= preturn_poss:
            win_rate = root.wins / root.visits
            total_wins+=root.wins
            total_visits+=root.visits
            print("----------TURN----------")
            print("Total simulations:", root.visits)
            print("Wins:", root.wins)
            print(f"Estimated win rate: {win_rate * 100:.2f}%")
            print("your hand: ", root.state.my_hand)
            #assign new root
            turn_root=random.choice(root.children)
            # turn_root.state.community = turn_root.state.community[:3]
            root = turn_root
            print("turn: ", turn_root.state.community)
            state="river"
            
        if state =="river" and len(root.children) >= river_poss:
            win_rate = root.wins / root.visits
            total_wins+=root.wins
            total_visits+=root.visits
            print("----------RIVER----------")
            print("Total simulations:", root.visits)
            print("Wins:", root.wins)
            print(f"Estimated win rate: {win_rate * 100:.2f}%")
            print("your hand: ", root.state.my_hand)
            #assign new root
            river_root=random.choice(root.children)
            # river_root.state.community = river_root.state.community[:4]
            root = river_root
            print("river: ", river_root.state.community)
            if win_rate >= 0.5:
                print("stay")
            else:
                print("fold")
            break
    print("--------------------------------------------------")
    win_rate = total_wins / total_visits
    print("Total simulations:", total_visits)
    print("Wins:", total_visits)
    print("--------------------------------------------------")
    print("Lets do a random playout with this community and hand")
    print("your hand: ", root.state.my_hand)
    print("community: ", root.state.community)
    state="resultplayout"
    

    result = simulate_random_playout(root.state)
    if result ==1:
        print("win")
    elif result ==0:
        print("loss")
    
if __name__ == "__main__":
    main()
