from dataclasses import dataclass

test_input = """A Y
B X
C Z
"""

class Hand:
    def __init__(self, input_str: str):
        match input_str:
            case 'A' | 'X':
                self.value = 1  # Rock
            case 'B' | 'Y':
                self.value = 2  # Paper
            case 'C' | 'Z':
                self.value = 3  # Scissors
            case _:
                raise ValueError()

    def __eq__(self, other):
        return self.value == other.value
    
    def __gt__(self, other):
        match self.value:
            case 1:
                return other.value == 3
            case 2:
                return other.value == 1
            case 3:
                return other.value == 2

    def __repr__(self):
        return f'Hand({self.value})'


    def winner(self) -> 'Hand':
        """return the hand that beats me"""
        match self.value:
            case 1:
                return Hand('B')
            case 2:
                return Hand('C')
            case 3:
                return Hand('A')


    def loser(self) -> 'Hand':
        """return the hand that loses to me."""
        match self.value:
            case 1:
                return Hand('C')
            case 2:
                return Hand('A')
            case 3:
                return Hand('B')

def score_hands(my_hand: Hand, opponent_hand: Hand) -> int:
    score = 0
    if my_hand == opponent_hand:  # a draw
        score = 3  
    elif my_hand > opponent_hand:  # a win
        score = 6
    return score + my_hand.value

def score_hands_part_two(opponent_hand: Hand, desired_result: int) -> int:
    """now X, Y, Z (1 2,3) indicate loss, draw, win.
    """
    match desired_result:
        case 1:  # loss
            my_hand = opponent_hand.loser() 
        case 2:  # draw
            my_hand = opponent_hand
        case 3: # win
            my_hand = opponent_hand.winner()

    return score_hands(my_hand, opponent_hand)
            


def parse_input(input_str) -> list[list[Hand]]:
    games = []
    for line in input_str.split('\n'):
        line = line.strip()
        if line:
            opponent_hand, my_hand = line.split()
            games.append([Hand(opponent_hand), Hand(my_hand)])  
    return games


def part_one(input_str: str) -> int:
    """
    parse the raw text into a list, then score the strategy.
    """
    games = parse_input(input_str)

    score = sum(score_hands(my_hand=m, opponent_hand=o) for o,m in games)

    return score

def part_two(input_str: str) -> int:
    """
    Sadly little of the parsing carries over.
    """
    games = parse_input(input_str)

    score_2 = sum(score_hands_part_two(opponent_hand=o, desired_result=m.value) for o,m in games)

    return score_2    



assert part_one(test_input) == 15

assert part_two(test_input) == 12

if __name__ == '__main__':

    with open('input.txt') as flines:
        input_str = flines.read()

    
    print('part one:', part_one(input_str))
    print('part two:', part_two(input_str))



