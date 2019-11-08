import random

BOT_PREFIX=('?')
TOKEN = 'NjQxNDA5MzMwODg4ODM1MDgz.XcIEjQ.I9hMnFyYzHJnd1PkifnVeHAiE9Q'

@client.command(name='RPS'


sets = ['spock', 'rock', 'scissors', 'lizard', 'paper']
sc_dict = {'sc': 'scissors', 'pa': 'paper', 'ro': 'rock',
           'sp': 'spock', 'li': 'lizard'}
n = len(sets)
win_range = 2


def scissors(pc_score=0, player_score=0):
    while True:
        pc = random.choice(sets)
        pc_id = sets.index(pc) + 1

        try:
            key = input('Your choice: ').lower()

            # game quit condition
            if key == 'x' or key == 'quit' or key == 'exit':
                print('Quitting game! See you next time!~')
                score(pc_score, player_score, True)
                return
            else:

                # shortcut check
                if key not in sets and key in sc_dict:
                    key = sc_dict[key]

                player_id = sets.index(key) + 1

        except ValueError:
            print('\nWrong input! If you want to quit the game, '
                  'enter "quit" or "exit"!\n')
            scissors(pc_score, player_score)
            return

        if player_id > pc_id:
            pc_id += n

        elif player_id == pc_id:
            print('DRAW! PC chose:', pc)
            score(pc_score, player_score)
            print()
            scissors(pc_score, player_score)
            return

        if pc_id - player_id <= win_range:
            print('Player won! PC chose:', pc)
            player_score += 1
        else:
            print('PC won! PC chose:', pc)
            pc_score += 1

        score(pc_score, player_score)
        print()


def score(pc, player, finished=False):
    if finished:
        end = 'Final'
    else:
        end = 'Current'
    print('{} score: PC: {}  Player: {}'.format(end, pc, player))


scissors())
