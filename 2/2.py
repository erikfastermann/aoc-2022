from pathlib import Path

opponent = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissor',
}

response_1 = {
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissor',
}

strategy_2 = {
    'X': 'loose',
    'Y': 'draw',
    'Z': 'win',
}

score_selected = {
    'rock': 1,
    'paper': 2,
    'scissor': 3,
}

play = {
    'loose': 0,
    'draw': 3,
    'win': 6,
}

win = {
    'rock': 'scissor',
    'paper': 'rock',
    'scissor': 'paper',
}

loose = {b: a for a, b in win.items()}

def play_round_1(other, me):
    if win[me] == other:
        return play['win']
    if me == other:
        return play['draw']
    if loose[me] == other:
        return play['loose']

def score_1(other, me):
    selection = score_selected[response_1[me]]
    played = play_round_1(opponent[other], response_1[me])
    return selection + played

def selection_2(other, strategy):
    match strategy:
        case 'loose':
            return score_selected[win[other]]
        case 'draw':
            return score_selected[other]
        case 'win':
            return score_selected[loose[other]]

def score_2(other, me):
    selection = selection_2(opponent[other], strategy_2[me])
    played = play[strategy_2[me]]
    return selection + played

rounds_raw = Path('input.txt').read_text().strip().split('\n')
rounds = [(round[0], round[2]) for round in rounds_raw]

total_score_1 = sum(score_1(other, me) for other, me in rounds)
total_score_2 = sum(score_2(other, me) for other, me in rounds)
print(total_score_1)
print(total_score_2)