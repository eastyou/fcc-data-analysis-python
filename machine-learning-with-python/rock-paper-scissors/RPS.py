import random

# 记录对手历史出拳频率，用其最常出的一手的克制拳回应

def player(prev_play, opponent_history=[]):
    if prev_play:
        opponent_history.append(prev_play)

    if not opponent_history:
        return random.choice(['R', 'P', 'S'])

    counts = {'R': 0, 'P': 0, 'S': 0}
    for move in opponent_history[-100:]:
        if move in counts:
            counts[move] += 1

    most_common = max(counts, key=counts.get)
    counter = {'R': 'P', 'P': 'S', 'S': 'R'}
    return counter[most_common]
