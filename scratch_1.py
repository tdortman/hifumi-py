import random

BOT_PREFIX = ('?')
TOKEN = 'NjQxNDA5MzMwODg4ODM1MDgz.XcIEjQ.I9hMnFyYzHJnd1PkifnVeHAiE9Q'

async def cmd_rps

you = ''
options = ['Sc', 'St', 'P']
def run(games = 1):
    # Loop
    print('Willkommen zu Schere Stein Papier in Python:')
    print('Starten Sie durch die Eingabe einer der unteren Begriffe : \n Sc -> Schere\n St -> '
          'Stein\n ' 'P -> Papier')

    # Datenbank für temporäre Speicherung der Scores
    x, y, z = 0, 0, 0
    score = {'du': x, 'computer': y, 'unentschieden': z}
    while True:
        print('Runde # {}. Wähle \'Sc\', \'St\', oder \'P\''.
            format(games))
        games += 1
        computer = random.choice(options)
        you = input().upper()
        if you == 'X':
            print("Spiel wird abgebrochen...")
            print('Dein Score = {} Computer score = {} Unentschieden = {}'.
                      format(score['du'], score['computer'], score['unentschieden']))
            exit(0)
        elif not(you == 'Sc' or you == 'St' or you == 'P'):
            print("\n{} ist nicht zulässig!".format(you))
            print('Dein Score = {} Computer score = {} Unentschieden = {}'.
                  format(score['du'], score['computer'], score['unentschieden']))
            print("Abbruch...")
            exit(0)
        else:
            if you == 'Sc' and computer == 'Sc':
                score['unentschieden'] += 1
                print('Computer wählt {}'.format(computer))
                print('UNENTSCHIEDEN')
            elif you == 'St' and computer == 'St':
                score['unentschieden'] += 1
                print('Computer wählt {}'.format(computer))
                print('UNENTSCHIEDEN')
            elif you == 'P' and computer == 'P':
                score['unentschieden'] += 1
                print('Computer wählt {}'.format(computer))
                print('UNENTSCHIEDEN')
            elif you == 'Sc' and computer == 'St':
                score['computer'] += 1
                print('Computer wählt {}'.format(computer))
                print('Computer gewinnt! Stein schleift Schere!')
            elif you == 'St' and computer == 'P':
                score['computer'] += 1
                print('Computer wählt {}'.format(computer))
                print('Computer gewinnt! Papier umwickelt Stein!')
            elif you == 'St' and computer == 'Sc':
                score['du'] += 1
                print('Computer wählt {}'.format(computer))
                print('Du gewinnst! BOOM. Stein zerschmettert Schere!')
            elif you == 'P' and computer == 'Sc':
                 score['computer'] += 1
                 print('Computer wählt {}'.format(computer))
                 print('Computer gewinnt! Schere schneidet Papier!')
            elif you == 'St'and computer == 'P':
                score['computer'] += 1
                print('Computer chooses {}'.format(computer))
                print('Computer gewinnt! Papier umwickelt Stein!')
            elif you == 'P' and computer == 'St':
                score['du'] += 1
                print('Computer wählt {}'.format(computer))
                print('Du gewinnst! Papier umwickelt Stein!')
game_rules = ('\n'
              'Schere Stein Papier Regeln:\n\n'
              'Sc = Schere, St = Stein, P = Papier\n'
              'Sc vs Sc = unentschieden\nP vs P = unentschieden\nSt vs St = unentschieden\n'
              'Sc vs P = P gewinnt\n'
              'St vs P = St gewinnt\n'
              'St vs Sc = St gewinnt\n')
print(game_rules)
print('Willst du spielen? Schreibe \'J\' um zu spielen oder \'N\' um das Spiel abzubrechen\n')
start = input().upper()
if start == 'J':
    run()
elif start == 'N':
    print('You''\'ve entered {} so exiting...'.format(start))
else:
    print('Du hast {} eingegeben, dies ist ungültig und das Spiel wird vorzeitig abgebrochen'
          '.'.format(start))