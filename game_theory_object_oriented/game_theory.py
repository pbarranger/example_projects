import time
import random

# Define the base comp_player class
class comp_player:
    '''Defines the base attributes of all computer players.'''
    def __init__(self):
        self.name = None
        self.score = 0
        self.bet = 1

# Define sub-classes of competitors
class copy_cat(comp_player):

    def __init__(self):
        self.character = 'Copy Cat'
        comp_player.__init__(self)
        self.bet = 1 #self.copy_cat_bid_method()
        self.blurb = '''Copy Cat always starts with contribute (1)
        and then will copy the last move from the other player for
        the remainder of the match '''

    def get_bid(self, player_prev_move):
        #Bid method is to copy player's last move
        if player_prev_move == 1:
            self.bet = 1
        else:
            self.bet = 0

class always_contr(comp_player):

    def __init__(self):
        self.character = 'Always Contribute'
        comp_player.__init__(self)
        self.bet = 1
        self.blurb = '''Always Contribute assumes the best in everyone and
        always bids contribute (1).'''

    def get_bid(self, player_prev_move):
        pass

class always_cheat(comp_player):

    def __init__(self):
        self.character = 'Always Cheat'
        comp_player.__init__(self)
        self.bet = 0
        self.blurb = '''Always Cheats will always cheat (0), it\'s all in
         the name.'''

    def get_bid(self, player_prev_move):
        pass

class grudger(comp_player):

    def __init__(self):
        self.character = 'Grudger'
        comp_player.__init__(self)
        self.bet = 1
        self.blurb = '''Grudger always starts with contribute (1) and will
        continue to bid contribute (1) until cheated. After being cheated,
        Grudger will only cheat (0), in revenge! '''
        #boolean for if char should flip strategy to all cheat
        self.revenge = 0


    def get_bid(self, player_prev_move):
        #Checks if player ever cheated and then bids
        if player_prev_move == 0:
            self.revenge = 1

        if self.revenge == 1:
            self.bet = 0
        else:
            self.bet = 1

class detective(comp_player):

    def __init__(self):
        self.character = 'Detective'
        comp_player.__init__(self)
        self.bet = 1
        self.blurb = '''Detective always plays the same sequence of opening
        moves - (1,1,0,1). If you cheat during one of the initial 4 rounds,
        Detective will copy your previous move. If you don't cheat,
        Detective will cheat for the remainder of the game.'''
        #tracks iterations through bidding logic
        self.bids_complete = 0
        #boolean to determine if it has been cheated
        self.been_cheated = 0

    def get_bid(self, player_prev_move):
        #base bid is 1 so start_seq is the remaining 1,0,1
        start_seq = [1,0,1]
        if player_prev_move == 0:
            self.been_cheated = 1
        #logic for bids after opening set
        if self.bids_complete < 3:
            self.bet = start_seq[self.bids_complete]
            self.bids_complete += 1
        #if cheated -plays as copy cat
        elif self.bids_complete >= 3 and self.been_cheated == 1:
            if player_prev_move == 1:
                self.bet = 1
            else:
                self.bet = 0
        #if never cheated then bids always cheat
        else:
            self.bet = 0

# Define player
class player_stats:
    '''Base attributes of a player.'''
    def __init__(self):
        self.bet = 1
        self.score = 0

# Define Game class
class game:
    '''Game class for Prisoner's dilemma simulation'''
    def __init__(self, comp = None):
        possible_character_list = [detective(), always_contr(), copy_cat(),
        always_cheat(), grudger()]
        #Determines order of characters to be played
        self.character_list = random.sample(possible_character_list,
            len(possible_character_list))
        #generates a player and comp class
        self.player = player_stats()
        self.round = 0
        self.match = 0
        self.character_gen()
        #sets 1st match number of rounds
        self.rand_round = random.randint(4,7)

    def ask(self):
        '''Method to take in player input w/ checks'''
        while True:
            try:
                user_input = int(input('''Would you like to contribute (1) or cheat (0)? \n'''))
                break
            except ValueError:
                print("Please enter eithe 1 to contribute or 0 to cheat. \n")
                continue

        if user_input == 1 or user_input == 0:
            self.player.bet = user_input
        else:
            print("Please enter eithe 1 to contribute or 0 to cheat. \n")
            self.ask()

        return self.player.bet

    def simulation(self):
        '''Runs one match of simulation'''
        if self.round < self.rand_round:
            if self.round == 0:
                self.player.score = 0
                print('\n\nA new character has been generated for you to play!')
            self.player.bet = self.ask()
            self.math_check(self.player.bet , self.comp.bet)
            self.match_score()
            self.round += 1
            self.comp.get_bid(self.player.bet)
        else:
            self.round = 0
            self.rand_round = random.randint(3,7)
            self.match += 1
            print('\nYou have completed this match!')
            self.score_board()

    def match_score(self):
        '''Method to hold the running score of a match.'''
        print('Round:', self.round + 1)
        print('Your score this match is:', self.player.score)
        print('The competitor\'s score this match:',
         self.comp.score, '\n')


    def score_board(self):
        '''Method for scoreboard at the end of the match'''
        if self.match < 5:
            print('Your score is', self.player.score)
            print('The competitor\'s score was', self.comp.score)
            print('The competitor you played was', self.comp.character)
            print("Here is a brief description of their style:", self.comp.blurb)
            self.character_gen()
        else:
            print('Your score is', self.player.score)
            print('The competitor\'s score was', self.comp.score)
            print('The competitor you played was', self.comp.character)
            print("Here is a brief description of their style:", self.comp.blurb)


    def character_gen(self):
        '''Method to generate next competitor'''
        character = self.character_list[self.match]
        self.comp = character

    def math_check(self, user_bid, comp_bet):
        '''Grading logic based on comp and player bids.'''
        if user_bid == 1 and comp_bet == 1:
            self.comp.score += 2
            self.player.score += 2
        elif user_bid == 1 and comp_bet == 0:
            self.player.score += -1
            self.comp.score += 3
        elif user_bid == 0 and comp_bet == 1:
            self.player.score += 3
            self.comp.score += -1
        else:
            self.player.score += 0
            self.comp.score += 0


# GAMEPLAY!!!!
print('\n\nWelcome to the Prisoner\'s Dilemma - a Game Theory simulator!')
time.sleep(1)
print('''\n\nIn front of you is a machine with another player on the other side.
You both can either choose to CONTRIBUTE (put in coin),
or CHEAT (don't put in coin).
If you both put in a coin: you both get 2 coins out.
If one player contributes and the other cheats: The cheater gets 3 coins and
the other loses a coin (-1).
If you both cheat: You both get nothing out (0).''')
time.sleep(2)
print('''\n\nYou'll be playing against 5 different opponents, each with their
own game "strategy". With each opponent, you'll play anywhere between
3 to 7 rounds. (You won't know in advance when the last round is)
Can you trust them? Or rather... can they trust you?''')
time.sleep(2)
print('\n\nReady to play? Press \'Y\' to start.')
game_on = input().lower()
if game_on == 'y':
    new_game = game()
    new_game.simulation()
    #Number of matches set and looped through until complete
    while new_game.match < 5:
        new_game.simulation()
    print('''\n\n\nGame Over!\nThank you for playing!\nYou have played against
    all five simulated characters.\n\n''')
else:
    pass
