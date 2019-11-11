import random

guessesTaken = 1
NUMBER = random.randint(1, 100)

print('Welcome! Time to guess some numbers!I am thinking of a number between 1 and 100.')

while guessesTaken <= 100:
    print('Round: {}'.format(guessesTaken))
    guess = int(input('Try guessing the number:'))

    if guess < NUMBER:
        print('Awww, too bad! Try guessing higher next time!')
    elif guess > NUMBER:
        print('Unlucky! Try a lower number!')
    if guess == NUMBER:
        guessesTaken = str(guessesTaken)
        print('Yes!! You guessed right!\nWon after {} rounds!'.format(guessesTaken))

guessesTaken += 1
