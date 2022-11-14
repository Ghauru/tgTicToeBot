from text_const import messages as m


def check_victory(playerpos):
    # All probable winning combinations
    solution = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    playerchoice = []
    for i in range(len(playerpos)):
        if playerpos[i] == m.X:
            playerchoice.append(i+1)
    for tap in solution:
        k = 0
        for i in tap:
            if i in playerchoice:
                k += 1
                if k == 3:
                    return m.X
    playerchoice = []
    for i in range(len(playerpos)):
        if playerpos[i] == m.O:
            playerchoice.append(i+1)
    for tap in solution:
        k = 0
        for i in tap:
            if i in playerchoice:
                k += 1
                if k == 3:
                    return m.O
    return False


def check_tie(playerpos):
    taken_spots = [i for i in playerpos if i != m.STAR]
    if len(taken_spots) == 9:
        return True
    return False


def who_won(playerpos, curplayer):
    if check_victory(playerpos):
        if curplayer == check_victory(playerpos):
            return curplayer
        else:
            return check_victory(playerpos)
    if check_tie(playerpos):
        return 'D'
