# App to play twilight struggle

defcon = 5
score = 0

game_active = True

countries = {}
players = {}
sides = {}
space_race_points = {}


def adjust_defcon(adjustment_value):
    global defcon
    defcon = defcon + adjustment_value

    # Adjust defcon to 5 if above 5
    if defcon > 5:
        defcon = 5

    if defcon < 2:
        if sides['usa'].phasing:
            sides['ussr'].winner = True
        elif sides['ussr'].phasing:
            sides['usa'].winner = True

        global game_active
        game_active = False


class CardGame:
    """Base class for a collection of Card Pile objects"""
    # TODO Finish the CardGame class with piles

    def __init__(self, n, d):
        self.name = n
        self.date = d
        self.piles = []


class Country:
    """Base class for a country in a game"""
    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Country: %s>" % self.name

    def __str__(self):
        return self.name


class Player:
    """Base class for a player in a game"""
    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Player: %s>" % self.name

    def __str__(self):
        return self.name


class TwilightStrugglePlayer(Player):
    """Class of players specific to Twilight Struggle"""

    def __init__(self, n, s):
        Player.__init__(self, n)

        if s not in ['usa', 'ussr']:
            raise ValueError("Error creating Twilight Struggle country. Controlled must be 'usa' or 'ussr'")
        self.side = s

        # Set phasing player to false
        self.phasing = False

        # Set space level to 0
        self.space_level = 0

        # Set winner to false
        self.winner = False


class TwilightStruggleCountry(Country):
    """Class of countries specific to Twilight Struggle"""

    def __init__(self, n, r, sr, st, bg, usa_i, ussr_i, c):
        Country.__init__(self, n)

        if r not in ['Africa', 'Asia', 'Central America', 'Europe', 'Middle East', 'South America']:
            raise ValueError("Error creating Twilight Struggle country. Region must be one of: Africa, Asia, Central America, Europe, Middle East, or South America")
        self.region = r

        if sr not in ['Both Europe', 'Eastern Europe', 'Western Europe', 'Southeast Asia', '']:
            raise ValueError("Error creating Twilight Struggle country. Subregion must be one of: 'Both Europe', 'Eastern Europe', 'Western Europe', or 'Southeast Asia'")
        if sr == '':
            pass
        else:
            self.subregion = sr

        if not st.isdigit() and (int(st) > 4 or int(st) < 1):
            raise ValueError("Error creating Twilight Struggle country. Stability must be a number between 1 and 4")
        self.stability = int(st)

        if bg not in ['TRUE', 'FALSE']:
            raise ValueError("Error creating Twilight Struggle country. Battleground must be True or False.")
        self.battleground = True if bg == 'True' else False

        if not usa_i.isdigit():
            raise ValueError("Error creating Twilight Struggle country. USA influence must be a number.")
        self.usa_influence = int(usa_i)

        if not ussr_i.isdigit():
            raise ValueError("Error creating Twilight Struggle country. USSR influence must be a number.")
        self.ussr_influence = int(ussr_i)

        if c not in ['usa', 'ussr', '']:
            raise ValueError("Error creating Twilight Struggle country. Controlled must be 'usa', 'ussr', or ''")
        self.controlled = c


class TwilightStruggleGame(CardGame):
    """Class of an individual game of Twilight Struggle"""

    turns = 10
    action_rounds = {1: 6, 2: 6, 3: 6, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7, 9: 7, 10: 7}

    def __init__(self, n, d, opt):
        CardGame.__init__(self, n, d)

        if not opt.isdigit() and int(opt) != 1 and int(opt) != 0:
            raise ValueError("Error creating Twilight Struggle game. Optional cards parameter must be a 1 or a 0.")
        self.optional_cards = True if opt == 1 else False

        self.__create_countries()
        self.__create_players()

    def __create_countries(self):
        with open('countries/country_list.csv', 'r') as handle:
            header = handle.readline()
            lines = handle.read().splitlines()

        for line in lines:
            country = TwilightStruggleCountry(*line.split(','))
            countries.update({country.name: country})

    def __create_players(self):
        # TODO - Change the "create players" function to allow for user input

        player_list = [['Player 1', 'ussr'], ['Player 2', 'usa']]

        for list in player_list:
            player = TwilightStrugglePlayer(list[0], list[1])
            players.update({player.name: player})
            sides.update({player.side: player})

    # Functions to modify influence
    def check_for_control(self, c):
        if (countries[c].usa_influence - countries[c].ussr_influence) >= countries[c].stability:
            countries[c].controlled = 'usa'
        elif (countries[c].ussr_influence - countries[c].usa_influence) >= countries[c].stability:
            countries[c].controlled = 'ussr'
        else:
            countries[c].controlled = ''

    def add_influence(self, c, s, i):
        if s == 'usa':
            countries[c].usa_influence += i
        elif s == 'ussr':
            countries[c].ussr_influence += i

        self.check_for_control(c)

    def add_influence_to_control(self, c, s):
        if s == 'usa':
            countries[c].usa_influence = countries[c].ussr_influence + countries[c].stability
        elif s == 'ussr':
            countries[c].ussr_influence = countries[c].usa_influence + countries[c].stability

        self.check_for_control(c)

    def remove_influence(self, c, s, i):
        if s == 'usa':
            countries[c].usa_influence -= i
            if countries[c].usa_influence < 0:
                countries[c].usa_influence = 0
        elif s == 'ussr':
            countries[c].ussr_influence -= i
            if countries[c].ussr_influence < 0:
                countries[c].ussr_influence = 0

        self.check_for_control(c)

    def remove_all_influence(self, c, s):
        if s == 'usa':
            countries[c].usa_influence = 0
        elif s == 'ussr':
            countries[c].ussr_influence = 0

        self.check_for_control(c)

    # Functions to modify the score
    def check_game_end(self):
        global game_active
        if score >= 20:
            sides['usa'].winner = True
            game_active = False
        elif score <= -20:
            sides['ussr'].winner = True
            game_active = False

    def change_score(self, s, p):
        global score
        if s == 'usa':
            score = score + p
        elif s == 'ussr':
            score = score - p

        self.check_game_end()

    # Functions for space race
    space_race_points = {1: [2, 1], 3: [2, 0], 5: [3, 1], 7: [4, 2], 8: [2, 0]}

    def space_race_awards(self, s):
        if s == 'usa':
            opponent = 'ussr'
        elif s == 'ussr':
            opponent = 'usa'
        else:
            raise ValueError("Side must be 'usa' or 'ussr'")

        level = sides[s].space_level

        if level in space_race_points:
            if sides[opponent].space_level < level:
                self.change_score(s, space_race_points[level][0])
            if sides[opponent].space_level >= level:
                self.change_score(s, space_race_points[level][1])

    def increase_space_level(self, s):
        if s == 'usa':
            sides['usa'].space_level += 1
            self.space_race_awards('usa')
        elif s == 'ussr':
            sides['ussr'].space_level += 1
            self.space_race_awards('ussr')

game = TwilightStruggleGame("default_name", "2022-01-27", "0")