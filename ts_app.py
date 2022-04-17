# App to play twilight struggle
import random
import math


class Card:
    """Base class for a generic card in a game"""

    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Card: %s>" % self.name

    def __str__(self):
        return self.name


class CardGame:
    """Base class for a collection of Card Pile objects"""

    def __init__(self, n, d):
        self.name = n
        self.date = d
        self.piles = {}

    def add_pile(self, p):
        if isinstance(p, CardPile):
            self.piles.update({p.name: p})
        else:
            raise ValueError("Could not add pile " + str(p) + " to card game " + str(self.name) + ".")

    def remove_pile(self, p):
        try:
            self.piles.pop(p.name)
        except ValueError:
            raise ValueError("Could not remove pile " + str(p) + " from card game " + str(self.name) + ".")

    def get_pile(self, n):
        pile = self.piles[n]
        return pile

    def die_roll(self):
        return random.randint(1, 6)

    def __repr__(self):
        string = "<CardGame: %s on %s>" % (self.name, self.date)
        for pile in self.piles:
            string += "\t" + repr(pile) + "\n"
        return string

    def __str__(self):
        return "%s on %s" % (self.name, self.date)


class CardPile:
    """Base class for a collection of Card objects"""

    def __init__(self, n, card_dict={}):
        self.name = n
        self.cards = {}
        for card in card_dict:
            self.add_card(card)

    def add_card(self, c):
        if isinstance(c, Card):
            self.cards.update({c.name: c})
        else:
            raise ValueError("Could not add card " + str(c) + " to card pile " + str(self) + ".")

    def remove_card(self, c):
        try:
            self.cards.pop(c.name)
        except ValueError:
            raise ValueError("Could not remove card" + str(c) + " from card pile " + str(self) + ".")

    def random_card(self):
        card_list = self.cards
        card = random.choice(list(card_list.values()))
        return card

    def get_card(self, n):
        card = self.cards[n]
        return card

    def get_pile_size(self):
        return len(self.cards)

    def get_cards_in_pile(self):
        cards_in_pile = self.cards
        return cards_in_pile

    def __repr__(self):
        string = "<CardPile: %s>" % self.name
        for card in self.cards:
            string += "\t" + repr(card) + "\n"
        return string

    def __str__(self):
        return self.name


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


class TwilightStruggleCard(Card):
    """Class of cards specific to the game Twilight Struggle"""

    def __init__(self, n, no, p, e, o, r, opt, e_turn, e_side):
        Card.__init__(self, n)

        if not no.isdigit():
            raise ValueError("Error creating Twilight Struggle Card. Number parameter must be a number")
        self.number = int(no)

        if p not in ['early war', 'mid war', 'late war']:
            raise ValueError("Error creating Twilight Struggle Card. Period parameter must be one of early war, mid war, or late war")
        self.period = p

        if e not in ['scoring', 'usa', 'ussr', 'neutral']:
            raise ValueError("Error creating Twilight Struggle Card. Event type must be scoring, usa, ussr, or neutral")
        self.event_type = e

        if not o.isdigit() and (int(o) > 4 or int(o) < 0):
            raise ValueError("Error creating Twilight Struggle Card. Ops must be a number between 0 and 4")
        self.ops = int(o)

        if not r.isdigit() and int(r) != 1 and int(r) != 0:
            raise ValueError("Error creating Twilight Struggle Card. Removed parameter must be a 1 or a 0")
        self.removed = True if int(r) == 1 else False

        if not opt.isdigit() and int(opt) != 1 and int(opt) != 0:
            raise ValueError("Error creating Twilight Struggle Card. Optional parameter must be a 1 or 0")
        self.optional = True if int(opt) == 1 else False

        if e_turn not in ['TRUE', '']:
            raise ValueError("Error creating Twilight Struggle country. Battleground must be True or False.")
        self.effect_turn = True if e_turn == 'TRUE' else False

        if e_side not in ['usa', 'ussr', 'both', 'choose', '']:
            raise ValueError("Error creating Twilight Struggle Card. Event type must be scoring, usa, ussr, or neutral")
        self.effect_side = e_side

        self.played = False
        self.effect_active = False


class TwilightStruggleChinaCard(Card):
    """Class for the china card"""

    def __init__(self, n, no, o):
        Card.__init__(self, n)

        if not no.isdigit():
            raise ValueError("Error creating Twilight Struggle China Card. Number parameter must be a number")
        self.number = int(no)

        if not o.isdigit() and (int(o) > 4 or int(o) < 0):
            raise ValueError("Error creating Twilight Struggle China Card. Ops must be a number between 0 and 4")
        self.ops = int(o)

        self.face_up = True
        self.owner = ''
        self.event_type = 'neutral'
        self.removed = False

    def flip_face_up(self):
        self.face_up = True
        log_string = "China card is face up and available to play."
        print(log_string)


class TwilightStrugglePlayer(Player):
    """Class of players specific to Twilight Struggle"""

    def __init__(self, n, s, o):
        Player.__init__(self, n)

        if s not in ['usa', 'ussr']:
            raise ValueError("Error creating Twilight Struggle country. Controlled must be 'usa' or 'ussr'")
        self.side = s

        if o not in ['usa', 'ussr']:
            raise ValueError("Error creating Twilight Struggle country. Controlled must be 'usa' or 'ussr'")
        self.opponent = o

        # Set phasing player to false
        self.phasing = False

        # Set space level to 0
        self.space_level = 0

        # Set mil ops to 0
        self.military_ops = 0

        # Set winner to false
        self.winner = False

        self.space_attempts = 0
        self.ops_adjustment = 0


class TwilightStruggleCountry(Country):
    """Class of countries specific to Twilight Struggle"""

    def __init__(self, n, r, sr, st, bg, usa_i, ussr_i, c):
        Country.__init__(self, n)

        if r not in ['Africa', 'Asia', 'Central America', 'Europe', 'Middle East', 'South America']:
            raise ValueError("Error creating Twilight Struggle country. Region must be one of: Africa, Asia, Central America, Europe, Middle East, or South America")
        self.region = r

        if sr not in ['Both Europe', 'Eastern Europe', 'Western Europe', 'Southeast Asia', '']:
            raise ValueError("Error creating Twilight Struggle country. Subregion must be one of: 'Both Europe', 'Eastern Europe', 'Western Europe', or 'Southeast Asia'")
        self.subregion = sr

        if not st.isdigit() and (int(st) > 4 or int(st) < 1):
            raise ValueError("Error creating Twilight Struggle country. Stability must be a number between 1 and 4")
        self.stability = int(st)

        if bg not in ['TRUE', 'FALSE']:
            raise ValueError("Error creating Twilight Struggle country. Battleground must be True or False.")
        self.battleground = True if bg == 'TRUE' else False

        if not usa_i.isdigit():
            raise ValueError("Error creating Twilight Struggle country. USA influence must be a number.")
        self.usa_influence = int(usa_i)

        if not ussr_i.isdigit():
            raise ValueError("Error creating Twilight Struggle country. USSR influence must be a number.")
        self.ussr_influence = int(ussr_i)

        if c not in ['usa', 'ussr', '']:
            raise ValueError("Error creating Twilight Struggle country. Controlled must be 'usa', 'ussr', or ''")
        self.controlled = c

        self.borders = []
        self.nato = False


class TwilightStruggleGame(CardGame):
    """Class of an individual game of Twilight Struggle"""

    turns = 10
    action_rounds = {1: 6, 2: 6, 3: 6, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7, 9: 7, 10: 7}

    def __init__(self, n, d, opt, extra):
        CardGame.__init__(self, n, d)

        if not opt.isdigit() and int(opt) != 1 and int(opt) != 0:
            raise ValueError("Error creating Twilight Struggle game. Optional cards parameter must be a 1 or a 0.")
        self.optional_cards = True if int(opt) == 1 else False

        if extra not in ['', 'bid', 'handicap']:
            raise ValueError("Error creating Twilight Struggle game. Extra influence must be one of: '', 'bid', or 'handicap'")
        self.extra_inf = extra

        self.defcon = 5
        self.score = 0
        self.turn = 1
        self.ar = 1
        self.game_active = True
        self.phase = ''
        self.phasing = ''
        self.active_player = None
        self.active_card = None
        self.action_round_complete = False
        self.conduct_operations_complete = False
        self.chernobyl = ''
        self.we_will_un_check = False
        self.norad_check = False
        self.usa_handicap = 0
        self.ussr_handicap = 0

        self.cards = {}
        self.countries = {}
        self.players = {}
        self.sides = {}
        self.opponent = {'usa': 'ussr', 'ussr': 'usa'}
        self.pile_owners = {'USA hand': 'usa',
                            'USA China': 'usa',
                            'USSR hand': 'ussr',
                            'USSR China': 'ussr'}
        self.hands = {'usa': 'USA hand',
                      'ussr': 'USSR hand'}
        self.china_owner = {'usa': 'USA China',
                            'ussr': 'USSR China'}
        self.pre_reqs = {'NATO': ['Marshall Plan', 'Warsaw Pact Formed'],
                         'Solidarity': ['John Paul II Elected Pope']}
        self.prevents = {'Arab-Israeli War': 'Camp David Accords',
                         'Socialist Governments': 'The Iron Lady',
                         'OPEC': 'North Sea Oil',
                         'Willy Brandt': 'Tear Down this Wall',
                         'Flower Power': '"An Evil Empire"',
                         'Muslim Revolution': 'AWACS Sale to Saudis'}

        self.line = '--------------------------------'

        self.__create_piles()
        self.__create_cards()
        self.__create_countries()
        self.__create_players()
        self.__set_up_game()

    def __create_cards(self):
        with open('cards/card_list.csv', 'r') as handle:
            header = handle.readline()
            lines = handle.read().splitlines()

        for line in lines:
            card = TwilightStruggleCard(*line.split(','))
            if not self.optional_cards and card.optional:
                continue
            start_pile = self.get_pile(card.period)
            if not start_pile:
                raise ValueError("Error adding card " + str(card) + " to pile " + str(start_pile) + ".")
            start_pile.add_card(card)
            self.cards.update({card.name: card})

        china_card = TwilightStruggleChinaCard('China', '6', '4')
        self.cards.update({china_card.name: china_card})

    def __create_countries(self):
        with open('countries/country_list.csv', 'r') as c_handle:
            country_header = c_handle.readline()
            c_lines = c_handle.read().splitlines()

        for c_line in c_lines:
            country = TwilightStruggleCountry(*c_line.split(','))
            self.countries.update({country.name: country})

        with open('countries/borders_list.csv', 'r') as b_handle:
            b_header = b_handle.readline()
            b_lines = b_handle.read().splitlines()

        for b_line in b_lines:
            borders_list = b_line.split(',')
            borders_list[:] = [x for x in borders_list if x]
            self.countries[borders_list[0]].borders = borders_list[1:]

    def __create_piles(self):
        pile_list = ['early war', 'mid war', 'late war', 'deck', 'discard', 'removed', 'USA hand', 'USSR hand',
                     'USA China', 'USSR China']

        for pile in pile_list:
            self.add_pile(CardPile(pile))

    def __create_players(self):
        # TODO - Change the "create players" function to allow for user input

        player_list = [['Player 1', 'ussr', 'usa'], ['Player 2', 'usa', 'ussr']]

        for p_list in player_list:
            player = TwilightStrugglePlayer(p_list[0], p_list[1], p_list[2])
            self.players.update({player.name: player})
            self.sides.update({player.side: player})

    def __set_up_game(self):
        # 3.1 Add the early war cards to the deck and deal out cards
        self.move_all_cards('deck', 'early war')
        self.deal_cards()

        # 3.1 Give the USSR player the China card
        self.piles['USSR China'].add_card(self.cards['China'])
        self.cards['China'].flip_face_up()

        # 3.2 - 3.3 Add initial influence
        with open('countries/initial_influence.csv', 'r') as i_handle:
            i_header = i_handle.readline()
            i_lines = i_handle.read().splitlines()

        for i_line in i_lines:
            initial_influence_list = i_line.split(',')
            initial_influence_list[:] = [x for x in initial_influence_list if x]

            if initial_influence_list[0] == 'usa':
                self.countries[initial_influence_list[1]].usa_influence = int(initial_influence_list[2])
            elif initial_influence_list[0] == 'ussr':
                self.countries[initial_influence_list[1]].ussr_influence = int(initial_influence_list[2])
            else:
                raise ValueError("Error adding initial influence")
            self.check_for_control(initial_influence_list[1])

        log_string = "Setup complete\n" + self.line
        print(log_string)

    # Function to adjust defcon
    def change_defcon(self, adjustment_value):
        initial_defcon = self.defcon
        self.defcon = self.defcon + adjustment_value
        log_string = "DEFCON changed by {a}".format(a=adjustment_value)
        print(log_string)

        # Adjust defcon to 5 if above 5
        if self.defcon > 5:
            self.defcon = 5

        if self.defcon < 2:
            self.defcon = 1

        log_string = "DEFCON is now {d}".format(d=self.defcon)
        print(log_string)

        self.check_defcon_game_end()

        # Event 106 - NORAD
        if initial_defcon != 2 and self.defcon == 2:
            self.norad_check = True

    def change_defcon_to_value(self, value):
        initial_defcon = self.defcon
        self.defcon = value
        self.check_defcon_game_end()
        log_string = "DEFCON is now {d}".format(d=self.defcon)
        print(log_string)

        # Event 106 - NORAD
        if initial_defcon != 2 and self.defcon == 2:
            self.norad_check = True

    def check_defcon_game_end(self):
        if self.defcon < 2:
            log_string = "Game over. Winner: {s}".format(s=self.opponent[self.phasing].upper())
            print(log_string)
            self.sides[self.opponent[self.phasing]].winner = True
            self.game_active = False
            self.action_round_complete = True

    # Functions to modify influence
    def check_for_control(self, c):
        if (self.countries[c].usa_influence - self.countries[c].ussr_influence) >= self.countries[c].stability:
            self.countries[c].controlled = 'usa'
        elif (self.countries[c].ussr_influence - self.countries[c].usa_influence) >= self.countries[c].stability:
            self.countries[c].controlled = 'ussr'
        else:
            self.countries[c].controlled = ''
        self.print_influence(c)

    def get_adjacent_controlled(self, country, side):
        """Gives list of countries that border the inputted country that are controlled by the inputted side"""
        adjacent_controlled = []
        border_list = country.borders

        for border in border_list:
            if border == 'USA' or border == 'USSR':
                pass
            elif self.countries[border].controlled == side:
                adjacent_controlled.append(self.countries[border])

        return adjacent_controlled

    def adjacent_to_superpower(self, country, side):
        adjacent = True if side.upper() in country.borders else False
        return adjacent

    def add_influence(self, country_name, side, i):
        if side == 'usa':
            self.countries[country_name].usa_influence += i
        elif side == 'ussr':
            self.countries[country_name].ussr_influence += i

        self.check_for_control(country_name)

    def add_influence_to_control(self, c, s):
        if s == 'usa':
            self.countries[c].usa_influence = self.countries[c].ussr_influence + self.countries[c].stability
        elif s == 'ussr':
            self.countries[c].ussr_influence = self.countries[c].usa_influence + self.countries[c].stability

        self.check_for_control(c)

    def remove_influence(self, c, s, i):
        if s == 'usa':
            self.countries[c].usa_influence -= i
            if self.countries[c].usa_influence < 0:
                self.countries[c].usa_influence = 0
        elif s == 'ussr':
            self.countries[c].ussr_influence -= i
            if self.countries[c].ussr_influence < 0:
                self.countries[c].ussr_influence = 0

        self.check_for_control(c)

    def remove_all_influence(self, country_name, s):
        if s == 'usa':
            self.countries[country_name].usa_influence = 0
        elif s == 'ussr':
            self.countries[country_name].ussr_influence = 0

        self.check_for_control(country_name)

    def get_influence(self, country_name, side):
        """Returns an int with the country's current influence"""
        influence = 0
        if side == 'usa':
            influence = self.countries[country_name].usa_influence
        elif side == 'ussr':
            influence = self.countries[country_name].ussr_influence
        return influence

    def get_opponent_influence(self, country_name, side):
        """Returns an int with the country's current influence"""
        influence = 0
        if side == 'usa':
            influence = self.countries[country_name].ussr_influence
        elif side == 'ussr':
            influence = self.countries[country_name].usa_influence
        return influence

    def print_influence(self, country_name):
        """Quick method to see the current influence. Takes a string"""
        usa_inf = self.get_influence(country_name, 'usa')
        ussr_inf = self.get_influence(country_name, 'ussr')
        usa_controlled = ''
        ussr_controlled = ''
        if self.countries[country_name].controlled == 'usa':
            usa_controlled = '*'
        elif self.countries[country_name].controlled == 'ussr':
            ussr_controlled = '*'
        log_string = "{c}: [ {usa_i}{usa_c} | {ussr_i}{ussr_c} ]".format(c=country_name,
                                                                         usa_i=usa_inf,
                                                                         usa_c=usa_controlled,
                                                                         ussr_i=ussr_inf,
                                                                         ussr_c=ussr_controlled)
        print(log_string)
        return log_string

    # Functions to modify the score
    def check_game_end(self):
        if self.score >= 20:
            self.sides['usa'].winner = True
            self.game_active = False
            self.action_round_complete = True
            log_string = "Game over. Winner: USA"
            print(log_string)
        elif self.score <= -20:
            self.sides['ussr'].winner = True
            self.game_active = False
            self.action_round_complete = True
            log_string = "Game over. Winner: USSR"
            print(log_string)

    def change_score(self, points):
        # Event 50 - "We Will Bury You" > give USSR 3 points first
        if self.we_will_un_check and points > 0:
            ui_string = 'Event 50 - We Will Bury You: USA did not play UN Intervention.'
            print(ui_string)
            self.change_score_by_side('ussr', 3)
            self.we_will_un_check = False
        self.score = self.score + points
        if points > 0:
            log_string = "USA scored {p} points. Score is now {score}.".format(p=points, score=self.score)
            print(log_string)
        elif points < 0:
            log_string = "USSR scored {p} points. Score is now {score}.".format(p=abs(points), score=self.score)
            print(log_string)

        self.check_game_end()

    def change_score_by_side(self, side, points):
        if side == 'usa':
            # Event 50 - "We Will Bury You" > give USSR 3 points first
            if self.we_will_un_check:
                ui_string = 'Event 50 - We Will Bury You: USA did not play UN Intervention.'
                print(ui_string)
                self.change_score_by_side('ussr', 3)
                self.we_will_un_check = False
            self.score = self.score + points
        elif side == 'ussr':
            self.score = self.score - points
        log_string = "{s} scored {p} points. Score is now {score}.".format(s=side.upper(), p=points, score=self.score)
        print(log_string)
        self.check_game_end()

    def get_score_in_regions(self):
        scores = {}
        scores.update({'Asia': [3, 7, 9, self.score_card('Asia', 3, 7, 9)]})
        scores.update({'Europe': [3, 7, 'Win', self.score_card('Europe', 3, 7, 100)]})
        scores.update({'Middle East': [3, 5, 7, self.score_card('Middle East', 3, 5, 7)]})
        scores.update({'Africa': [1, 4, 6, self.score_card('Africa', 1, 4, 6)]})
        scores.update({'Central America': [1, 3, 5, self.score_card('Central America', 1, 3, 5)]})
        scores.update({'South America': [2, 5, 6, self.score_card('South America', 2, 5, 6)]})

        if not self.which_pile(self.cards['Southeast Asia Scoring']) == 'removed':
            scores.update({'Southeast Asia': self.southeast_asia_scoring()})

        print("Current scores:")
        for score in scores:
            if score == 'Southeast Asia':
                print("{s:>3} | {n:15}".format(s=scores[score], n=score))
            else:
                print("{0:>3} | {1:15} [{2:^3}|{3:^3}|{4:^3}]".format(scores[score][3], score, scores[score][0],
                                                                      scores[score][1], scores[score][2]))

    def final_scoring(self):
        self.cards['Shuttle Diplomacy'].effect_active = False

        asia = self.score_card('Asia', 3, 7, 9, True)
        europe = self.score_card('Europe', 3, 7, 100, True)
        middle_east = self.score_card('Middle East', 3, 5, 7, True)
        central_america = self.score_card('Central America', 1, 3, 5, True)
        africa = self.score_card('Africa', 1, 4, 6, True)
        south_america = self.score_card('South America', 2, 5, 6, True)
        total = asia + europe + middle_east + central_america + africa + south_america

        log_string = 'Final scoring:'
        print(log_string)
        self.change_score(total)

        # Score china card
        owner = self.who_has_china()
        log_string = "{s} collects bonus for holding China.".format(s=owner.upper())
        print(log_string)
        self.change_score_by_side(owner, 1)

        # End the game
        self.game_active = False
        winner = ''
        if self.score < 0:
            winner = 'USSR'
            self.sides['ussr'].winner = True
        elif self.score > 0:
            winner = 'USA'
            self.sides['usa'].winner = True
        elif self.score == 0:
            winner = 'None - game ended in draw'

        self.action_round_complete = True
        log_string = "Game over. Winner: {w}".format(w=winner)
        print(log_string)

    # Functions for space race
    def space_race_awards(self, s):
        space_race_points = {1: [2, 1], 3: [2, 0], 5: [3, 1], 7: [4, 2], 8: [2, 0]}
        level = self.sides[s].space_level

        if level in space_race_points:
            if self.sides[self.opponent[s]].space_level < level:
                self.change_score_by_side(s, space_race_points[level][0])
            if self.sides[self.opponent[s]].space_level >= level:
                self.change_score_by_side(s, space_race_points[level][1])

    def increase_space_level(self, s):
        self.sides[s].space_level += 1
        self.space_race_awards(s)

    # Functions for checking access
    def countries_with_influence(self, s):
        country_list = []
        for country in self.countries.values():
            if s == 'usa' and country.usa_influence > 0:
                country_list.append(country)
            elif s == 'ussr' and country.ussr_influence > 0:
                country_list.append(country)

        return country_list

    def countries_in_region(self, region):
        countries_in_region = []
        for country in self.countries.values():
            if country.region == region:
                countries_in_region.append(country)

        return countries_in_region

    def countries_in_subregion(self, subregion):
        countries_in_subregion = []
        for country in self.countries.values():
            if country.subregion == subregion:
                countries_in_subregion.append(country)
            if (subregion == 'Eastern Europe' or subregion == 'Western Europe') and country.subregion == 'Both Europe':
                countries_in_subregion.append(country)

        return countries_in_subregion

    def battleground_countries_in_region(self, region):
        bg_countries_in_region = []
        for country in self.countries.values():
            if country.region == region and country.battleground:
                bg_countries_in_region.append(country)

        return bg_countries_in_region

    def nonbattleground_countries_in_region(self, region):
        nonbg_countries_in_region = []
        for country in self.countries.values():
            if country.region == region and not country.battleground:
                nonbg_countries_in_region.append(country)

        return nonbg_countries_in_region

    def controlled_in_region(self, region, side):
        country_list = self.countries_in_region(region)
        controlled_list = []

        for country in country_list:
            if side == 'usa' and country.controlled == 'usa':
                controlled_list.append(country)
            elif side == 'ussr' and country.controlled == 'ussr':
                controlled_list.append(country)

        return controlled_list

    def controlled_in_subregion(self, subregion, side):
        country_list = self.countries_in_subregion(subregion)
        controlled_list = []

        for country in country_list:
            if side == 'usa' and country.controlled == 'usa':
                controlled_list.append(country)
            elif side == 'ussr' and country.controlled == 'ussr':
                controlled_list.append(country)

        return controlled_list

    def not_opponent_controlled_in_region(self, region, side):
        country_list = self.countries_in_region(region)
        not_controlled_list = []

        for country in country_list:
            if country.controlled != self.opponent[side]:
                not_controlled_list.append(country)

        return not_controlled_list

    def not_opponent_controlled_in_subregion(self, subregion, side):
        country_list = self.countries_in_subregion(subregion)
        not_controlled_list = []

        for country in country_list:
            if country.controlled != self.opponent[side]:
                not_controlled_list.append(country)

        return not_controlled_list

    def battlegrounds_controlled_in_region(self, region, side):
        country_list = self.countries_in_region(region)
        controlled_list = []

        for country in country_list:
            if side == 'usa' and country.controlled == 'usa' and country.battleground:
                controlled_list.append(country)
            elif side == 'ussr' and country.controlled == 'ussr' and country.battleground:
                controlled_list.append(country)

        return controlled_list

    def accessible_countries(self, s):
        influenced_countries = self.countries_with_influence(s)
        accessible_countries = influenced_countries.copy()

        for country in influenced_countries:
            border_list = country.borders
            for border in border_list:
                if border != 'USA' and border != 'USSR':
                    if self.countries[border] not in accessible_countries:
                        accessible_countries.append(self.countries[border])

        return accessible_countries

    def total_battlegrounds_controlled(self, side):
        country_list = []

        for country in self.countries.values():
            if country.controlled == side and country.battleground:
                country_list.append(country.name)

        return len(country_list)

    def adjacent_country_objects(self, country):
        """Converts a country's list of borders from strings to the corresponding country objects"""
        adjacent_country_strings = country.borders
        adjacent_country_objects = []

        for country in adjacent_country_strings:
            adjacent_country_objects.append(self.countries[country])

        return adjacent_country_objects

    def are_all_targets_in_region(self, target_list, region):
        """Given a list of countries, checks to see if they are all in the specified region"""
        target_check = True

        if len(target_list) == 0:
            target_check = False

        for country in target_list:
            if country.region != region:
                target_check = False

        return target_check

    def are_all_targets_in_subregion(self, target_list, subregion):
        """Given a list of countries, checks to see if they are all in the specified subregion"""
        target_check = True

        if len(target_list) == 0:
            target_check = False

        for country in target_list:
            if country.subregion != subregion:
                target_check = False

        return target_check

    # Functions for moving cards around
    def scoring_cards_in_hand(self, side):
        scoring_cards = []
        hand = self.get_available_cards(side, False)

        for card in hand:
            if card.event_type == 'scoring':
                scoring_cards.append(card)

        return scoring_cards

    def which_pile(self, c):
        for pile in self.piles:
            cards_in_pile = self.piles[pile].get_cards_in_pile()

            if c.name in cards_in_pile:
                return pile

    def move_card(self, c, pile_name):
        current_pile = self.which_pile(c)
        self.piles[current_pile].remove_card(c)
        self.piles[pile_name].add_card(c)
        log_string = "{c} moved to {p}.".format(c=c.name, p=pile_name)
        print(log_string)

    def move_all_cards(self, pile_to_name, pile_from_name):
        card_list = self.piles[pile_from_name].get_cards_in_pile().copy()
        for c in card_list:
            self.piles[pile_from_name].remove_card(self.cards[c])
            self.piles[pile_to_name].add_card(self.cards[c])

    def move_china_card(self, pile_to_name, face_up=False):
        current_pile = self.which_pile(self.cards['China'])
        self.piles[current_pile].remove_card(self.cards['China'])
        self.piles[pile_to_name].add_card(self.cards['China'])
        log_string_1 = "China card given to {s}.".format(s=self.pile_owners[pile_to_name].upper())
        print(log_string_1)
        if face_up:
            self.cards['China'].flip_face_up()
        else:
            self.cards['China'].face_up = False
            log_string_2 = 'China card is face down.'
            print(log_string_2)

    def who_has_china(self):
        current_pile = self.which_pile(self.cards['China'])
        owner = ''
        if current_pile == 'USSR China':
            owner = 'ussr'
        elif current_pile == 'USA China':
            owner = 'usa'
        return owner

    def give_opponent_china_card(self, side):
        if side == 'usa':
            self.move_china_card('USSR China')
        elif side == 'ussr':
            self.move_china_card('USA China')

    def reshuffle(self):
        self.move_all_cards('deck', 'discard')

    def deal_cards(self):
        hand_limit = {1: 8, 2: 8, 3: 8, 4: 9, 5: 9, 6: 9, 7: 9, 8: 9, 9: 9, 10: 9}
        current_hand_limit = hand_limit[self.turn]
        hands = ['USSR hand', 'USA hand']

        for card_number in range(1, current_hand_limit + 1):
            for hand in hands:
                if self.piles[hand].get_pile_size() < current_hand_limit:
                    if self.piles['deck'].get_pile_size() > 0:
                        dealt_card = self.piles['deck'].random_card()
                        self.move_card(dealt_card, hand)
                    else:
                        self.reshuffle()
                        dealt_card = self.piles['deck'].random_card()
                        self.move_card(dealt_card, hand)

    def format_available_cards(self, cards_to_format):
        hand_list = []
        for card in cards_to_format:
            star = ''
            if card.removed:
                star = '*'
            entry = "{0} {1:7} {2:1} {3}".format(card.ops, card.event_type, star, card.name)
            hand_list.append(entry)

        return hand_list

    def sort_cards(self, cards_to_sort):
        sort = 'ops'
        sort_china = True

        if sort == 'ops':
            sorted_cards = sorted(cards_to_sort, key=lambda x: (x.ops, x.event_type, x.name), reverse=True)
        elif sort == 'side':
            sorted_cards = sorted(cards_to_sort, key=lambda x: (x.event_type, x.ops, x.name), reverse=True)
        elif sort == 'name':
            sorted_cards = sorted(cards_to_sort, key=lambda x: (x.name, x.event_type))
        else:
            raise ValueError("Sort type must be 'ops' or 'side'")

        if sort_china:
            if self.cards['China'] in sorted_cards:
                sorted_cards.insert(0, sorted_cards.pop(sorted_cards.index(self.cards['China'])))

        return sorted_cards

    def get_available_cards(self, side, include_china):
        available_cards = list(self.piles[self.hands[side]].get_cards_in_pile().values())
        if include_china:
            if self.cards['China'] in self.piles[self.china_owner[side]].get_cards_in_pile().values():
                available_cards.append(self.cards['China'])

        sorted_available_cards = self.sort_cards(available_cards)

        return sorted_available_cards

    def get_available_cards_in_discard(self):
        available_cards = list(self.piles['discard'].get_cards_in_pile().values())
        for card in available_cards:
            if card.event_type == 'scoring':
                available_cards.remove(card)

        sorted_available_cards = self.sort_cards(available_cards)

        return sorted_available_cards

    # Functions to change military ops
    def add_military_ops(self, side, amount):
        if side == 'usa':
            self.sides['usa'].military_ops += amount
            if self.sides['usa'].military_ops > 5:
                self.sides['usa'].military_ops = 5
        elif side == 'ussr':
            self.sides['ussr'].military_ops += amount
            if self.sides['ussr'].military_ops > 5:
                self.sides['ussr'].military_ops = 5
        else:
            raise ValueError("Side must be 'usa' or 'ussr'")

    def check_required_military_ops(self):
        usa_points = 0
        ussr_points = 0

        if self.sides['usa'].military_ops < self.defcon:
            ussr_points = self.defcon - self.sides['usa'].military_ops

        if self.sides['ussr'].military_ops < self.defcon:
            usa_points = self.defcon - self.sides['ussr'].military_ops

        points = usa_points - ussr_points
        if usa_points > ussr_points:
            self.change_score_by_side('usa', points)
        elif ussr_points > usa_points:
            self.change_score_by_side('ussr', points)

    def reset_military_ops(self):
        self.sides['usa'].military_ops = 0
        self.sides['ussr'].military_ops = 0

    # Functions to manipulate events
    def check_UN_intervention_eligible(self, side):
        hand = self.get_available_cards(side, False)
        eligible = False
        opponent_cards = 0
        for card in hand:
            if card.event_type == self.opponent[side]:
                opponent_cards = opponent_cards + 1

        if opponent_cards > 0:
            eligible = True

        return eligible

    def quagmire_bear_trap_eligible(self, side):
        eligible_cards = []
        hand = self.get_available_cards(side, False)
        # Event 49 - Missile Envy
        if self.cards['Missile Envy'].effect_active \
                and self.cards['Missile Envy'].effect_player == side \
                and self.cards['Missile Envy'] in hand \
                and (self.adjust_ops(self.cards['Missile Envy'].ops, side, 1, 4) >= 2):
            eligible_cards.append(self.cards['Missile Envy'])
        else:
            for card in hand:
                ops = self.adjust_ops(card.ops, side, 1, 4)
                if ops >= 2:
                    eligible_cards.append(card)

        return eligible_cards

    def check_event_eligibility(self, card):
        eligible = False
        if card.name in self.pre_reqs.keys():
            for pre_req in self.pre_reqs[card.name]:
                if self.cards[pre_req].played:
                    eligible = True
        elif card.name in self.prevents.keys():
            if not self.cards[self.prevents[card.name]].played:
                eligible = True
        elif card.name == 'Kitchen Debates':
            usa_battlegrounds = self.total_battlegrounds_controlled('usa')
            ussr_battlegrounds = self.total_battlegrounds_controlled('ussr')
            eligible = True if usa_battlegrounds > ussr_battlegrounds else False
        elif card.name == 'Star Wars':
            usa_space = self.sides['usa'].space_level
            ussr_space = self.sides['ussr'].space_level
            eligible = True if usa_space > ussr_space else False
        elif card.name == 'Our Man in Tehran':
            usa_controlled_middle_east = self.controlled_in_region('Middle East', 'usa')
            if len(usa_controlled_middle_east) > 0:
                eligible = True
        elif card.name == 'Wargames':
            eligible = True if self.defcon == 2 else False
        else:
            eligible = True

        return eligible

    def trigger_event(self, card):
        eligible = self.check_event_eligibility(card)
        self.active_card = card

        if eligible:
            log_string = "Event {no} - {na}.".format(no=card.number,
                                                     na=card.name)
            print(log_string)
            self.events[card.name](self)
            card.played = True
            card.effect_active = True

            # Check for active effects
            self.trigger_effect(self.cards['Flower Power'])

            # Event 60 - U2 Incident
            if card.name == 'UN Intervention' and self.cards['U2 Incident'].effect_active:
                log_string = 'Event 60 - U2 Incident activated due to UN Intervention:'
                print(log_string)
                self.change_score_by_side('ussr', 1)

            if card.removed:
                self.move_card(card, 'removed')
            else:
                if card.name == 'Missile Envy':
                    pass
                else:
                    self.move_card(card, 'discard')
        else:
            self.move_card(card, 'discard')

    def war_card(self, country, side, success, mil_ops, points, itself):
        number_adjacent = len(self.get_adjacent_controlled(country, self.opponent[side]))
        if itself:
            if country.controlled == self.opponent[side]:
                number_adjacent += 1
        if self.adjacent_to_superpower(country, self.opponent[side]):
            number_adjacent += 1

        roll = self.die_roll()
        modified_die_roll = roll - number_adjacent
        self.add_military_ops(side, mil_ops)
        log_string_1 = "{s} rolls {r}. {o} controls {a} adjacent countries. " \
                       "Modified die roll is {m}. Victory {su} - 6.".format(s=side.upper(),
                                                                            r=roll,
                                                                            o=self.opponent[side].upper(),
                                                                            a=number_adjacent,
                                                                            m=modified_die_roll,
                                                                            su=success)
        print(log_string_1)
        if modified_die_roll >= success:
            log_string_2 = "Success!"
            print(log_string_2)
            self.change_score_by_side(side, points)
            influence = self.get_influence(country.name, self.opponent[side])
            self.remove_all_influence(country.name, self.opponent[side])
            self.add_influence(country.name, side, influence)
        else:
            log_string_2 = "Failure."
            print(log_string_2)

    def score_type(self, region):
        usa_type = 'no influence'
        ussr_type = 'no influence'

        battlegrounds_in_region = len(self.battleground_countries_in_region(region))
        usa_countries = len(self.controlled_in_region(region, 'usa'))
        ussr_countries = len(self.controlled_in_region(region, 'ussr'))
        usa_bgs = len(self.battlegrounds_controlled_in_region(region, 'usa'))
        ussr_bgs = len(self.battlegrounds_controlled_in_region(region, 'ussr'))

        if usa_countries > 0:
            usa_type = 'presence'
        if (usa_countries > ussr_countries) and (usa_bgs > ussr_bgs) and (usa_countries > usa_bgs):
            usa_type = 'domination'
        if (usa_countries > ussr_countries) and usa_bgs == battlegrounds_in_region:
            usa_type = 'control'

        if ussr_countries > 0:
            ussr_type = 'presence'
        if (ussr_countries > usa_countries) and (ussr_bgs > usa_bgs) and (ussr_countries > ussr_bgs):
            ussr_type = 'domination'
        if (ussr_countries > usa_countries) and ussr_bgs == battlegrounds_in_region:
            ussr_type = 'control'

        return [usa_type, ussr_type]

    def score_card(self, region, presence, domination, control, log=False):
        usa_score_type = self.score_type(region)[0]
        ussr_score_type = self.score_type(region)[1]
        usa_adjacent_bonus = 0
        ussr_adjacent_bonus = 0
        usa_bg_bonus = len(self.battlegrounds_controlled_in_region(region, 'usa'))
        ussr_bg_bonus = len(self.battlegrounds_controlled_in_region(region, 'ussr'))
        countries_in_region = self.countries_in_region(region)

        score_dict = {'no influence': 0, 'presence': presence, 'domination': domination, 'control': control}

        for country in countries_in_region:
            border_list = country.borders
            for border in border_list:
                if border == 'USSR':
                    if country.controlled == 'usa':
                        usa_adjacent_bonus += 1
                elif border == 'USA':
                    if country.controlled == 'ussr':
                        ussr_adjacent_bonus += 1

        usa_total = score_dict[usa_score_type] + usa_adjacent_bonus + usa_bg_bonus
        ussr_total = score_dict[ussr_score_type] + ussr_adjacent_bonus + ussr_bg_bonus
        log_string = "\n{r} SCORING".format(r=region.upper())
        print(log_string)

        log_string_usa = "USA has {t}\n" \
                         "Base score:         {s}\n" \
                         "Adjacent countries: {a}\n" \
                         "Battlegrounds:      {b}\n" \
                         "Total:              {st}\n".format(t=usa_score_type.upper(),
                                                             tl=usa_score_type,
                                                             s=score_dict[usa_score_type],
                                                             a=usa_adjacent_bonus,
                                                             b=usa_bg_bonus,
                                                             st=usa_total)
        log_string_ussr = "USSR has {t}\n" \
                          "Base score:         {s}\n" \
                          "Adjacent countries: {a}\n" \
                          "Battlegrounds:      {b}\n" \
                          "Total:              {st}\n".format(t=ussr_score_type.upper(),
                                                              tl=ussr_score_type,
                                                              s=score_dict[ussr_score_type],
                                                              a=ussr_adjacent_bonus,
                                                              b=ussr_bg_bonus,
                                                              st=ussr_total)
        if log:
            print(log_string_usa)
            print(log_string_ussr)
        return usa_total - ussr_total

    def southeast_asia_scoring(self, log=False):
        usa_score = 0
        usa_thailand = 0
        ussr_score = 0
        ussr_thailand = 0
        country_list = self.countries_in_subregion('Southeast Asia')

        for country in country_list:
            if country.controlled == 'usa':
                usa_score += 1
            elif country.controlled == 'ussr':
                ussr_score += 1

        if self.countries['Thailand'].controlled == 'usa':
            usa_thailand += 1

        if self.countries['Thailand'].controlled == 'ussr':
            ussr_thailand += 1

        usa_total = usa_score + usa_thailand
        ussr_total = ussr_score + ussr_thailand

        log_string_usa = "USA controlled countries: {c}\nBonus for Thailand: {b}\nTotal: {t}\n".format(c=usa_score,
                                                                                                       b=usa_thailand,
                                                                                                       t=usa_total)
        log_string_ussr = "USSR controlled countries: {c}\nBonus for Thailand: {b}\nTotal: {t}\n".format(c=ussr_score,
                                                                                                         b=ussr_thailand,
                                                                                                         t=ussr_total)
        if log:
            print(log_string_usa)
            print(log_string_ussr)

        return usa_total - ussr_total

    # Specific events
    def event_001(self):
        """Asia Scoring"""
        points = self.score_card('Asia', 3, 7, 9, True)
        self.change_score(points)

    def event_002(self):
        """Europe Scoring"""
        points = self.score_card('Europe', 3, 7, 100, True)
        self.change_score(points)

    def event_003(self):
        """Middle East Scoring"""
        points = self.score_card('Middle East', 3, 5, 7, True)
        self.change_score(points)

    def event_004(self):
        """Duck and Cover"""
        self.change_defcon(-1)
        points = 5 - self.defcon
        self.change_score_by_side('usa', points)

    def event_005(self):
        """Five Year Plan"""
        if len(self.get_available_cards('ussr', False)) > 0:
            card = self.piles['USSR hand'].random_card()
            log_string = "USSR randomly discards {c}.".format(c=card.name)
            print(log_string)

            if card.event_type == 'usa':
                self.trigger_event(card)
            else:
                self.move_card(card, 'discard')

    def event_007(self):
        """Socialist Governments"""
        eligible_countries = self.countries_in_subregion('Western Europe')
        self.ask_to_remove_influence(eligible_countries, 3, 'ussr', 1, 2)

    def event_008(self):
        """Fidel"""
        self.remove_all_influence('Cuba', 'usa')
        self.add_influence_to_control('Cuba', 'ussr')

    def event_009(self):
        """Vietnam Revolts"""
        self.add_influence('Vietnam', 'ussr', 2)

    def event_010(self):
        """Blockade"""
        eligible_cards = []
        usa_hand = self.get_available_cards('usa', False)

        for card in usa_hand:
            if (card.ops + self.sides['usa'].ops_adjustment) >= 3:
                eligible_cards.append(card)

        if len(eligible_cards) == 0:
            self.remove_all_influence('W. Germany', 'usa')
        else:
            options = [['a', "Discard a card with operations value of 3 or more"],
                       ['b', "Remove all US influence from W. Germany"]]
            response = self.select_option(options)
            if response == 'a':
                selected_card = self.select_a_card(eligible_cards, 'usa')
                self.move_card(selected_card, 'discard')
            elif response == 'b':
                self.remove_all_influence('W. Germany', 'usa')

    def event_011(self):
        """Korean War"""
        self.war_card(self.countries['S. Korea'], 'ussr', 4, 2, 2, False)

    def event_012(self):
        """Romanian Abdication"""
        self.remove_all_influence('Romania', 'usa')
        self.add_influence_to_control('Romania', 'ussr')

    def event_013(self):
        """Arab-Israeli War"""
        self.war_card(self.countries['Israel'], 'ussr', 4, 2, 2, True)

    def event_014(self):
        """Comecon"""
        eligible_countries = self.not_opponent_controlled_in_subregion('Eastern Europe', 'ussr')
        self.ask_to_place_influence(eligible_countries, 4, 'ussr', 1, 1)

    def event_015(self):
        """Nasser"""
        usa_inf = self.countries['Egypt'].usa_influence
        inf_to_remove = math.ceil(usa_inf / 2)
        self.add_influence('Egypt', 'ussr', 2)
        self.remove_influence('Egypt', 'usa', inf_to_remove)

    def event_016(self):
        """Warsaw Pact Formed"""
        eligible_countries = self.countries_in_subregion('Eastern Europe')
        options = [['a', "Remove all USA influence from 4 countries in Eastern Europe"],
                   ['b', "Add 5 USSR influence in Eastern Europe, no more than 2 per country"]]
        response = self.select_option(options)
        if response == 'a':
            self.ask_to_remove_all_influence(eligible_countries, 4, 'ussr')
        elif response == 'b':
            self.ask_to_place_influence(eligible_countries, 5, 'ussr', 1, 2)

    def event_017(self):
        """De Gaulle Leads France"""
        self.remove_influence('France', 'usa', 2)
        self.add_influence('France', 'ussr', 1)
        self.countries['France'].nato = False

    def event_018(self):
        """Captured Nazi Scientist"""
        self.increase_space_level(self.phasing)

    def event_019(self):
        """Truman Doctrine"""
        europe_countries = self.countries_in_region('Europe')
        usa_controlled = self.controlled_in_region('Europe', 'usa')
        ussr_controlled = self.controlled_in_region('Europe', 'ussr')
        eligible_countries = []

        for country in europe_countries:
            if country not in usa_controlled and country not in ussr_controlled:
                eligible_countries.append(country)

        self.ask_to_remove_all_influence(eligible_countries, 1, 'usa')

    def event_020(self):
        """Olympic Games"""
        options = [['a', "Participate - Each player roll, sponsor adds 2 to roll. Highest modified roll receives 2 VP"],
                   ['b', "Boycott - Degrade DEFCON by 1, sponsor may conduct operations as if they played 4 op card"]]
        response = self.select_option(options)

        if response == 'a':
            while True:
                sponsor_roll = self.die_roll() + 2
                print("Sponsor {p} rolled {r1} + 2".format(p=self.phasing.upper(),
                                                           r1=(sponsor_roll - 2)))

                opponent_roll = self.die_roll()
                print("Opponent {o} rolled {r2}".format(o=self.opponent[self.phasing].upper(),
                                                        r2=opponent_roll))

                if sponsor_roll > opponent_roll:
                    print("Sponsor {p} wins!".format(p=self.phasing.upper()))
                    self.change_score_by_side(self.phasing, 2)
                    break
                elif opponent_roll > sponsor_roll:
                    print("Opponent {o} wins!".format(o=self.opponent[self.phasing].upper()))
                    self.change_score_by_side(self.opponent[self.phasing], 2)
                    break
                else:
                    log_string = 'Tied - rerolling'
                    print(log_string)
        elif response == 'b':
            self.change_defcon(-1)
            self.conduct_operations(self.phasing, 4)

    def event_021(self):
        """NATO"""
        countries = self.countries_in_region('Europe')
        for country in countries:
            country.nato = True

        if self.cards['De Gaulle Leads France'].effect_active:
            self.countries['France'].nato = False

        if self.cards['Willy Brandt'].effect_active:
            self.countries['W. Germany'].nato = False

    def event_022(self):
        """Independent Reds"""
        eligible_countries = [self.countries['Yugoslavia'],
                              self.countries['Romania'],
                              self.countries['Bulgaria'],
                              self.countries['Hungary'],
                              self.countries['Czechoslovakia']]

        target_country = self.select_a_country(eligible_countries)
        usa_inf = self.get_influence(target_country.name, 'usa')
        ussr_inf = self.get_opponent_influence(target_country.name, 'usa')
        self.add_influence(target_country.name, 'usa', (ussr_inf - usa_inf))

    def event_023(self):
        """Marshall Plan"""
        eligible_countries = self.not_opponent_controlled_in_subregion('Western Europe', 'usa')
        self.ask_to_place_influence(eligible_countries, 7, 'usa', 1, 1)

    def event_024(self):
        """Indo-Pakistani War"""
        options = [['i', "Invade India"],
                   ['p', "Invade Pakistan"]]
        response = self.select_option(options)

        if response == 'i':
            self.war_card(self.countries['India'], self.phasing, 4, 2, 2, False)
        elif response == 'p':
            self.war_card(self.countries['Pakistan'], self.phasing, 4, 2, 2, False)

    def event_025(self):
        """Containment"""
        self.sides['usa'].ops_adjustment = 1

    def event_026(self):
        """CIA Created"""
        visible_cards = self.get_available_cards('ussr', False)
        print(visible_cards)

        self.conduct_operations('usa', self.cards['CIA Created'].ops)

    def event_027(self):
        """US/Japan Mutual Defense Pact"""
        self.add_influence_to_control('Japan', 'usa')

    def event_028(self):
        """Suez Crisis"""
        eligible_countries = [self.countries['France'], self.countries['UK'], self.countries['Israel']]
        self.ask_to_remove_influence(eligible_countries, 3, 'ussr', 1, 2)

    def event_029(self):
        """East European Unrest"""
        eligible_countries = self.countries_in_subregion('Eastern Europe')
        if self.turn < 8:
            self.ask_to_remove_influence(eligible_countries, 3, 'usa', 1, 1)
        elif self.turn >= 8:
            self.ask_to_remove_influence(eligible_countries, 6, 'usa', 2, 2)

    def event_030(self):
        """Decolonization"""
        eligible_countries = self.countries_in_region('Africa') + self.countries_in_subregion('Southeast Asia')
        self.ask_to_place_influence(eligible_countries, 4, 'ussr', 1, 1)

    def event_031(self):
        """Red Scare/Purge"""
        self.sides[(self.opponent[self.phasing])].ops_adjustment = -1
        ui_string = "-1 to all {s} operations.".format(s=self.opponent[self.phasing].upper())
        print(ui_string)

    def event_032(self):
        """UN Intervention"""
        hand = self.get_available_cards(self.phasing, False)
        eligible_cards = []
        for card in hand:
            if card.event_type == self.opponent[self.phasing]:
                eligible_cards.append(card)
        selected_card = self.select_a_card(eligible_cards, self.phasing)

        adjusted_ops = self.adjust_ops(selected_card.ops, self.phasing, 1, 4)

        self.conduct_operations(self.phasing, adjusted_ops)

        self.move_card(selected_card, 'discard')

    def event_034(self):
        """Nuclear Test Ban"""
        points = self.defcon - 2
        self.change_score_by_side(self.phasing, points)
        self.change_defcon(2)

    def event_036(self):
        """Brush War"""
        eligible_countries = []
        for country in self.countries.values():
            if country.stability <= 2:
                if not country.nato:
                    eligible_countries.append(country)

        if len(eligible_countries) > 0:
            target = self.select_a_country(eligible_countries)
            self.war_card(self.countries[target.name], self.phasing, 3, 3, 1, False)

    def event_037(self):
        """Central America Scoring"""
        points = self.score_card('Central America', 1, 3, 5, True)
        self.change_score(points)

    def event_038(self):
        """Southeast Asia Scoring"""
        points = self.southeast_asia_scoring(True)
        self.change_score(points)

    def event_039(self):
        """Arms Race"""
        phasing_mil_ops = self.sides[self.phasing].military_ops
        opponent_mil_ops = self.sides[(self.opponent[self.phasing])].military_ops
        if (phasing_mil_ops > opponent_mil_ops) and (phasing_mil_ops < self.defcon):
            self.change_score_by_side(self.phasing, 1)
        elif (phasing_mil_ops > opponent_mil_ops) and (phasing_mil_ops >= self.defcon):
            self.change_score_by_side(self.phasing, 3)

    def event_041(self):
        """Nuclear Subs"""
        pass

    def event_042(self):
        """Quagmire"""
        self.cards['NORAD'].effect_active = False

    def event_043(self):
        """SALT Negotiations"""
        self.change_defcon(2)
        eligible_cards = self.get_available_cards_in_discard()
        selected_card = self.select_a_card(eligible_cards, self.phasing)
        self.move_card(selected_card, self.hands[self.phasing])

    def event_044(self):
        """Bear Trap"""
        pass

    def event_046(self):
        """How I Learned to Stop Worrying"""
        options = [['5', "Set DEFCON to 5"],
                   ['4', "Set DEFCON to 4"],
                   ['3', "Set DEFCON to 3"],
                   ['2', "Set DEFCON to 2"],
                   ['1', "Set DEFCON to 1"]]
        response = int(self.select_option(options))
        self.change_defcon_to_value(response)

    def event_047(self):
        """Junta"""
        eligible_countries = self.countries_in_region('Central America') + self.countries_in_region('South America')
        self.ask_to_place_influence(eligible_countries, 2, self.phasing, 2, 2)

        adjusted_card_ops = self.adjust_ops(self.cards['Junta'].ops, self.phasing, 1, 4)
        selected_action = self.select_action_limited(False, True, False, True, False)

        if selected_action == 'c':
            self.ask_to_coup_attempt(eligible_countries, adjusted_card_ops, self.phasing, False)
        elif selected_action == 'r':
            self.ask_to_realignment_roll(eligible_countries, adjusted_card_ops, self.phasing)

    def event_048(self):
        """Kitchen Debates"""
        usa_battlegrounds = self.total_battlegrounds_controlled('usa')
        ussr_battlegrounds = self.total_battlegrounds_controlled('ussr')

        if usa_battlegrounds > ussr_battlegrounds:
            self.change_score_by_side('usa', 2)

    def event_049(self):
        """Missile Envy"""
        opponent_hand = self.get_available_cards(self.opponent[self.phasing], False)
        highest_ops = max(card.ops for card in opponent_hand)
        eligible_cards = []

        for card in opponent_hand:
            if card.ops == highest_ops:
                eligible_cards.append(card)

        ui_string = "Choose card to give to opponent."
        print(ui_string)
        selected_card = self.select_a_card(eligible_cards, self.opponent[self.phasing])

        # Collected rulings - Missile Envy goes in opponent hand so it could be pulled by Grain Sales
        self.move_card(self.cards['Missile Envy'], self.hands[self.opponent[self.phasing]])

        if selected_card.event_type == self.opponent[self.phasing]:
            self.conduct_operations(self.phasing, self.adjust_ops(selected_card.ops, self.phasing, 1, 4))
            self.move_card(selected_card, 'discard')
        else:
            self.trigger_event(selected_card)

        self.cards['Missile Envy'].effect_active = True
        self.cards['Missile Envy'].effect_player = self.opponent[self.phasing]

    def event_050(self):
        """We Will Bury You"""
        self.change_defcon(-1)

    def event_051(self):
        """Brezhnev Doctrine"""
        self.sides['ussr'].ops_adjustment = 1

    def event_052(self):
        """Portuguese Empire Crumbles"""
        self.add_influence('Angola', 'ussr', 2)
        self.add_influence('SE African States', 'ussr', 2)

    def event_053(self):
        """South African Unrest"""
        options = [['a', "USSR adds 2 influence to South Africa"],
                   ['b', "USSR adds 1 influence to South Africa and 2 to a single country adjacent to South Africa"]]
        response = self.select_option(options)
        if response == 'a':
            self.add_influence('South Africa', 'ussr', 2)
        elif response == 'b':
            self.add_influence('South Africa', 'ussr', 1)
            targets = self.adjacent_country_objects(self.countries['South Africa'])
            self.ask_to_place_influence(targets, 2, 'ussr', 2, 2)

    def event_054(self):
        """Allende"""
        self.add_influence('Chile', 'ussr', 2)

    def event_055(self):
        """Willy Brandt"""
        self.change_score_by_side('ussr', 1)
        self.add_influence('W. Germany', 'ussr', 1)
        self.countries['W. Germany'].nato = False

    def event_056(self):
        """Muslim Revolution"""
        eligible_countries = [self.countries["Sudan"],
                              self.countries["Iran"],
                              self.countries["Iraq"],
                              self.countries["Egypt"],
                              self.countries["Libya"],
                              self.countries["Saudi Arabia"],
                              self.countries["Syria"],
                              self.countries["Jordan"]]

        self.ask_to_remove_all_influence(eligible_countries, 2, 'ussr')

    def event_057(self):
        """ABM Treaty"""
        self.change_defcon(1)
        self.conduct_operations(self.phasing, self.cards['ABM Treaty'].ops)

    def event_058(self):
        """Cultural Revolution"""
        if self.cards['China'] in self.piles['USA China'].get_cards_in_pile().values():
            self.move_china_card('USSR China', True)
        elif self.cards['China'] in self.piles['USSR China'].get_cards_in_pile().values():
            self.change_score_by_side('ussr', 1)
        else:
            raise ValueError("China card must be in USA hand or USSR hand")

    def event_059(self):
        """Flower Power"""
        pass

    def event_060(self):
        """U2 Incident"""
        self.change_score_by_side('ussr', 1)

    def event_061(self):
        """OPEC"""
        opec_list = ['Egypt', 'Iran', 'Libya', 'Saudi Arabia', 'Iraq', 'Gulf States', 'Venezuela']
        points = 0

        for country in opec_list:
            if self.countries[country].controlled == 'ussr':
                points += 1

        self.change_score_by_side('ussr', points)

    def event_062(self):
        """Lone Gunman"""
        visible_cards = self.get_available_cards('usa', False)
        print(visible_cards)

        self.conduct_operations('ussr', self.cards['"Lone Gunman"'].ops)

    def event_063(self):
        """Colonial Rear Guards"""
        eligible_countries = self.countries_in_region('Africa') + self.countries_in_subregion('Southeast Asia')
        self.ask_to_place_influence(eligible_countries, 4, 'usa', 1, 1)

    def event_064(self):
        """Panama Canal Returned"""
        self.add_influence('Panama', 'usa', 1)
        self.add_influence('Costa Rica', 'usa', 1)
        self.add_influence('Venezuela', 'usa', 1)

    def event_065(self):
        """Camp David Accords"""
        self.change_score_by_side('usa', 1)
        self.add_influence('Israel', 'usa', 1)
        self.add_influence('Jordan', 'usa', 1)
        self.add_influence('Egypt', 'usa', 1)

    def event_066(self):
        """Puppet Governments"""
        all_countries = self.countries.values()
        usa_counties = self.countries_with_influence('usa')
        ussr_countries = self.countries_with_influence('ussr')
        eligible_countries = []

        for country in all_countries:
            if country not in usa_counties and country not in ussr_countries:
                eligible_countries.append(country)

        if len(eligible_countries) > 0:
            self.ask_to_place_influence(eligible_countries, 3, 'usa', 1, 1)

    def event_067(self):
        """Grain Sales to Soviets"""
        if len(self.get_available_cards('ussr', False)) > 0:
            card = self.piles['USSR hand'].random_card()
            log_string = "USSR randomly discards {c}.".format(c=card.name)
            print(log_string)

            # In the headline phase you must return UN intervention (in FAQs)
            if self.phase == 'headline' and card.name == 'UN Intervention':
                print('UN intervention may not be played in headline phase, automatically returned.')
                response = 'b'
            else:
                options = [['a', "Play card"],
                           ['b', "Return card"]]
                response = self.select_option(options)

            if response == 'a':
                self.move_card(card, 'USA hand')
                self.conduct_operations_complete = False

                while not self.conduct_operations_complete:
                    un_eligible = self.check_UN_intervention_eligible('usa')
                    if card.name == 'UN Intervention' and not un_eligible:
                        action_options = " c| Coup attempt\n" \
                                         " i| Place influence\n" \
                                         " r| Realignment roll\n" \
                                         " s| Space race\n"
                        eligible_actions = ['c', 'i', 'r', 's']
                    else:
                        action_options = " e| Play event\n" \
                                         " c| Coup attempt\n" \
                                         " i| Place influence\n" \
                                         " r| Realignment roll\n" \
                                         " s| Space race\n"
                        eligible_actions = ['e', 'c', 'i', 'r', 's']
                    print(self.line)
                    print("Select use for " + card.name + ':')
                    print(action_options)
                    while True:
                        selected_action = input("Selection: ").lower()
                        if selected_action in eligible_actions:
                            break

                    adjusted_card_ops = self.adjust_ops(card.ops, 'usa', 1, 4)
                    if selected_action == 'e':
                        self.trigger_event(card)
                        self.conduct_operations_complete = True
                    elif selected_action == 'c':
                        self.action_coup_attempt(adjusted_card_ops, 'usa')
                    elif selected_action == 'i':
                        self.action_place_influence(adjusted_card_ops, 'usa')
                    elif selected_action == 'r':
                        self.action_realignment_roll(adjusted_card_ops, 'usa')
                    elif selected_action == 's':
                        self.action_space_race(card, adjusted_card_ops, 'usa')

                if selected_action == 'c' or selected_action == 'i' or selected_action == 'r':
                    if card.event_type == 'ussr':
                        self.trigger_event(card)
                    else:
                        self.trigger_effect(self.cards['Flower Power'])
                        self.move_card(card, 'discard')

            elif response == 'b':
                self.conduct_operations('usa', self.cards['Grain Sales to Soviets'].ops)
        else:
            self.conduct_operations('usa', self.cards['Grain Sales to Soviets'].ops)

    def event_068(self):
        """John Paul II Elected Pope"""
        self.remove_influence('Poland', 'ussr', 2)
        self.add_influence('Poland', 'usa', 1)

    def event_069(self):
        """Latin American Death Squads"""
        self.cards['Latin American Death Squads'].effect_side = self.phasing

    def event_070(self):
        """OAS Founded"""
        eligible_countries = self.countries_in_region('Central America') + self.countries_in_region('South America')
        self.ask_to_place_influence(eligible_countries, 2, 'usa', 1, 2)

    def event_071(self):
        """Nixon Plays the China Card"""
        if self.cards['China'] in self.piles['USSR China'].get_cards_in_pile().values():
            self.move_china_card('USA China', False)
        elif self.cards['China'] in self.piles['USA China'].get_cards_in_pile().values():
            self.change_score_by_side('usa', 2)
        else:
            raise ValueError("China card must be in USA hand or USSR hand")

    def event_072(self):
        """Sadat Expels Soviets"""
        self.remove_all_influence('Egypt', 'ussr')
        self.add_influence('Egypt', 'usa', 1)

    def event_074(self):
        """The Voice of America"""
        eligible_countries = (self.countries_in_region('Asia') +
                              self.countries_in_region('Middle East') +
                              self.countries_in_region('Africa') +
                              self.countries_in_region('Central America') +
                              self.countries_in_region('South America'))

        self.ask_to_remove_influence(eligible_countries, 4, 'usa', 1, 2)

    def event_075(self):
        """Liberation Theology"""
        eligible_countries = self.countries_in_region('Central America')
        self.ask_to_place_influence(eligible_countries, 3, 'ussr', 1, 2)

    def event_076(self):
        """Ussuri River Skirmish"""
        if self.cards['China'] in self.piles['USSR China'].get_cards_in_pile().values():
            self.move_china_card('USA China', True)
        elif self.cards['China'] in self.piles['USA China'].get_cards_in_pile().values():
            eligible_countries = self.countries_in_region('Asia')
            self.ask_to_place_influence(eligible_countries, 4, 'usa', 1, 2)
        else:
            raise ValueError("China card must be in USA hand or USSR hand")

    def event_077(self):
        """Ask Not What Your Country..."""
        while True:
            card_options = self.get_available_cards('usa', False)
            selected_list = []
            card_list_names = ''

            print('Discard up to entire hard:')

            while True:
                card = self.select_a_card(card_options, 'usa')
                selected_list.append(card)
                card_options.remove(card)

                if self.confirm_action('Finish discarding cards') or len(card_options) == 0:
                    break

            # Format a string with the card names
            for card in selected_list:
                card_list_names = card_list_names + card.name + '\n'

            confirmation = self.confirm_action("Discard these cards:\n{l}".format(l=card_list_names))

            if confirmation:
                for card in selected_list:
                    self.move_card(card, 'discard')
                draw_number = 0
                while draw_number < len(selected_list):
                    dealt_card = self.piles['deck'].random_card()
                    self.move_card(dealt_card, 'USA hand')
                    draw_number += 1
                break

    def event_078(self):
        """Alliance for Progress"""
        ca_battlegrounds = len(self.battlegrounds_controlled_in_region('Central America', 'usa'))
        sa_battlegrounds = len(self.battlegrounds_controlled_in_region('South America', 'usa'))
        self.change_score_by_side('usa', (ca_battlegrounds + sa_battlegrounds))

    def event_079(self):
        """Africa Scoring"""
        points = self.score_card('Africa', 1, 4, 6, True)
        self.change_score(points)

    def event_080(self):
        """One Small Step..."""
        if self.sides[self.phasing].space_level < self.sides[self.opponent[self.phasing]].space_level:
            self.sides[self.phasing].space_level += 1
            self.increase_space_level(self.phasing)

    def event_081(self):
        """South America Scoring"""
        points = self.score_card('South America', 2, 5, 6, True)
        self.change_score(points)

    def event_082(self):
        """Iranian Hostage Crisis"""
        self.remove_all_influence('Iran', 'usa')
        self.add_influence('Iran', 'ussr', 2)

    def event_083(self):
        """The Iron Lady"""
        self.add_influence('Argentina', 'ussr', 1)
        self.remove_all_influence('UK', 'ussr')
        self.change_score_by_side('usa', 1)

    def event_084(self):
        """Reagan Bombs Libya"""
        points = self.countries['Libya'].ussr_influence // 2
        self.change_score_by_side('usa', points)

    def event_085(self):
        """Star Wars"""
        eligible_cards = self.get_available_cards_in_discard()
        if len(eligible_cards) > 0:
            selected_card = self.select_a_card(eligible_cards, 'usa')
            self.trigger_event(selected_card)

    def event_086(self):
        """North Sea Oil"""
        pass

    def event_087(self):
        """The Reformer"""
        eligible_countries = self.countries_in_region('Europe')
        if self.score < 0:
            self.ask_to_place_influence(eligible_countries, 6, 'ussr', 1, 2)
        else:
            self.ask_to_place_influence(eligible_countries, 4, 'ussr', 1, 2)

    def event_088(self):
        """Marine Barracks Bombing"""
        eligible_countries = self.countries_in_region('Middle East')
        self.remove_all_influence('Lebanon', 'usa')
        self.ask_to_remove_influence(eligible_countries, 2, 'ussr', 1, 2)

    def event_089(self):
        """Soviets Shoot Down KAL-007"""
        self.change_defcon(-1)
        self.change_score_by_side('usa', 2)

        if self.countries['S. Korea'].controlled == 'usa':
            card_value = self.adjust_ops(self.cards['Soviets Shoot Down KAL-007'].ops, 'usa', 1, 4)
            selected_action = self.select_action_limited(False, False, True, True, False)

            if selected_action == 'i':
                eligible_countries = self.accessible_countries('usa')
                self.ask_to_place_influence(eligible_countries, card_value, 'usa')
            elif selected_action == 'r':
                eligible_countries = self.countries_with_influence('ussr')
                self.ask_to_realignment_roll(eligible_countries, card_value, 'usa')

    def event_090(self):
        """Glasnost"""
        self.change_defcon(1)
        self.change_score_by_side('ussr', 2)

        if self.cards['The Reformer'].effect_active:
            card_value = self.adjust_ops(self.cards['Glasnost'].ops, 'ussr', 1, 4)
            selected_action = self.select_action_limited(False, False, True, True, False)

            if selected_action == 'i':
                eligible_countries = self.accessible_countries('ussr')
                self.ask_to_place_influence(eligible_countries, card_value, 'ussr')
            elif selected_action == 'r':
                eligible_countries = self.countries_with_influence('usa')
                self.ask_to_realignment_roll(eligible_countries, card_value, 'ussr')

    def event_091(self):
        """Ortega Elected in Nicaragua"""
        self.remove_all_influence('Nicaragua', 'usa')
        adjacent_countries = self.adjacent_country_objects(self.countries['Nicaragua'])
        card_value = self.adjust_ops(self.cards['Ortega Elected in Nicaragua'].ops, 'ussr', 1, 4)
        self.ask_to_coup_attempt(adjacent_countries, card_value, 'ussr', False)

    def event_092(self):
        """Terrorism"""
        if self.piles['USA hand'].get_pile_size() > 0:
            discard = self.piles['USA hand'].random_card()
            self.move_card(discard, 'discard')
        if self.cards['Iranian Hostage Crisis'].played:
            if self.piles['USA hand'].get_pile_size() > 0:
                discard = self.piles['USA hand'].random_card()
                self.move_card(discard, 'discard')

    def event_093(self):
        """Iran-Contral Scandal"""
        pass

    def event_094(self):
        """Chernobyl"""
        options = [['1', "USSR cannot add influence in Africa"],
                   ['2', "USSR cannot add influence in Asia"],
                   ['3', "USSR cannot add influence in Central America"],
                   ['4', "USSR cannot add influence in Europe"],
                   ['5', "USSR cannot add influence in the Middle East"],
                   ['6', "USSR cannot add influence in South America"]]
        response = self.select_option(options)
        if response == '1':
            self.chernobyl = 'Africa'
        elif response == '2':
            self.chernobyl = 'Asia'
        elif response == '3':
            self.chernobyl = 'Central America'
        elif response == '4':
            self.chernobyl = 'Europe'
        elif response == '5':
            self.chernobyl = 'Middle East'
        elif response == '6':
            self.chernobyl = 'South America'

    def event_095(self):
        """Latin American Debt Crisis"""
        eligible_cards = []
        usa_hand = self.get_available_cards('usa', False)
        double_influence = False

        for card in usa_hand:
            if (card.ops + self.sides['usa'].ops_adjustment) >= 3:
                eligible_cards.append(card)

        if len(eligible_cards) == 0:
            double_influence = True
        else:
            options = [['a', "Discard a card with operations value of 3 or more"],
                       ['b', "USSR may double amount of USSR influence in 2 countries in South America"]]
            response = self.select_option(options)
            if response == 'a':
                selected_card = self.select_a_card(eligible_cards, 'usa')
                self.move_card(selected_card, 'discard')
            elif response == 'b':
                double_influence = True

        if double_influence:
            while True:
                target_list = []
                target_list_names = ''
                eligible_countries = self.countries_in_region('South America')
                targeted_countries = 0

                while targeted_countries < 2:
                    country = self.select_a_country(eligible_countries)
                    target_list.append(country)
                    eligible_countries.remove(country)
                    targeted_countries += 1

                for country in target_list:
                    target_list_names = target_list_names + country.name + '\n'

                confirmation = self.confirm_action("Double USSR influence in:\n{l}".format(l=target_list_names))

                if confirmation:
                    for country in target_list:
                        current_inf = self.get_influence(country.name, 'ussr')
                        self.add_influence(country.name, 'ussr', current_inf)
                    break

    def event_096(self):
        """Tear Down this Wall"""
        self.add_influence('E. Germany', 'usa', 3)
        self.cards['Willy Brandt'].effect_active = False

        european_countries = self.countries_in_region('Europe')
        card_value = self.adjust_ops(self.cards['Tear Down this Wall'].ops, 'usa', 1, 4)
        selected_action = self.select_action_limited(False, True, False, True, False)

        if selected_action == 'c':
            self.ask_to_coup_attempt(european_countries, card_value, 'usa', False)
        elif selected_action == 'r':
            self.ask_to_realignment_roll(european_countries, card_value, 'usa')

    def event_097(self):
        """An Evil Empire"""
        self.change_score_by_side('usa', 1)
        self.cards['Flower Power'].effect_active = False

    def event_098(self):
        """Aldrich Ames Remix"""
        eligible_cards = self.get_available_cards('usa', False)
        print(eligible_cards)

        while True:
            print("Discard a card from the USA hand.")
            card = self.select_a_card(eligible_cards, 'ussr')
            if self.confirm_action("Discard {c} from USA hand".format(c=card.name)):
                self.move_card(card, 'discard')
                break

    def event_099(self):
        """Pershing II Deployed"""
        eligible_countries = self.countries_in_subregion('Western Europe')
        self.change_score_by_side('ussr', 1)
        self.ask_to_remove_influence(eligible_countries, 3, 'ussr', 1, 1)

    def event_100(self):
        """Wargames"""
        if self.defcon == 2:
            options = [['a', "Give your opponent 6 points and immediately end game"],
                       ['b', "Pass"]]
            response = self.select_option(options)
            if response == 'a':
                self.change_score_by_side(self.active_player.opponent, 6)
                self.game_active = False

    def event_101(self):
        """Solidarity"""
        self.add_influence('Poland', 'usa', 3)

    def event_102(self):
        """Iran-Iraq War"""
        options = [['a', "Invade Iran"],
                   ['b', "Invade Iraq"]]
        response = self.select_option(options)

        if response == 'a':
            self.war_card(self.countries['Iran'], self.phasing, 4, 2, 2, False)
        elif response == 'b':
            self.war_card(self.countries['Iraq'], self.phasing, 4, 2, 2, False)

    def event_103(self):
        """Defectors"""
        if self.phase == 'ussr action round':
            self.change_score_by_side('usa', 1)

    def event_104(self):
        """The Cambridge Five"""
        scoring_conversion = {'Asia Scoring': 'Asia',
                              'Europe Scoring': 'Europe',
                              'Middle East Scoring': 'Middle East',
                              'Africa Scoring': 'Africa',
                              'Central America Scoring': 'Central America',
                              'South America Scoring': 'South America'}

        eligible_countries = []

        if self.turn < 8:
            usa_hand = self.piles['USA hand'].get_cards_in_pile()
            for card in usa_hand.values():
                if card.name == 'Southeast Asia':
                    print(card.name)
                    country_list = self.countries_in_subregion('Southeast Asia')
                    for country in country_list:
                        eligible_countries.append(country)
                elif card.name in scoring_conversion:
                    print(card.name)
                    country_list = self.countries_in_region(scoring_conversion[card.name])
                    for country in country_list:
                        eligible_countries.append(country)

            if len(eligible_countries) > 0:
                self.ask_to_place_influence(eligible_countries, 1, 'ussr', 1, 1)

    def event_105(self):
        """Special Relationship"""
        if self.countries['UK'].controlled == 'usa':
            if self.cards['NATO'].effect_active:
                eligible_countries = self.countries_in_subregion('Western Europe')
                self.ask_to_place_influence(eligible_countries, 2, 'usa', 2, 2)
                self.change_score_by_side('usa', 2)
            else:
                eligible_countries = self.adjacent_country_objects(self.countries['UK'])
                self.ask_to_place_influence(eligible_countries, 1, 'usa', 1, 1)

    def event_106(self):
        """NORAD"""
        pass


    def event_107(self):
        """Che"""
        possible_countries = (self.nonbattleground_countries_in_region('Central America') +
                              self.nonbattleground_countries_in_region('South America') +
                              self.nonbattleground_countries_in_region('Africa'))
        card_value = self.adjust_ops(self.cards['Che'].ops, 'ussr', 1, 4)

        coup_result = self.ask_to_coup_attempt(possible_countries, card_value, 'ussr', False)

        if coup_result[1]:
            possible_countries.remove(coup_result[0])
            self.ask_to_coup_attempt(possible_countries, card_value, 'ussr', False)

    def event_108(self):
        """Our Man In Tehran"""
        drawn_cards = []
        number_drawn = 0

        draw_pile = list(self.piles['deck'].get_cards_in_pile().values())
        if len(draw_pile) >= 5:
            cards_to_draw = 5
        else:
            cards_to_draw = len(draw_pile)

        print('USA draws following cards:')

        while number_drawn < cards_to_draw:
            card = self.piles['deck'].random_card()
            if card not in drawn_cards:
                drawn_cards.append(card)
                print(card.name)
                number_drawn += 1

        while True:
            target_cards = []
            target_card_names = ''
            for card in drawn_cards:
                if self.confirm_action("Discard {c}".format(c=card.name)):
                    target_cards.append(card)
                    target_card_names = target_card_names + card.name + '\n'

            if self.confirm_action("Discard the following cards:\n{c}".format(c=target_card_names)):
                for card in target_cards:
                    self.move_card(card, 'discard')
                break

    def event_109(self):
        """Yuri and Samantha"""
        pass

    def event_110(self):
        """AWACS Sale to Saudis"""
        self.add_influence('Saudi Arabia', 'usa', 2)

    # Dictionary of the events
    events = {'Asia Scoring':                   event_001,
              'Europe Scoring':                 event_002,
              'Middle East Scoring':            event_003,
              'Duck and Cover':                 event_004,
              'Five Year Plan':                 event_005,
              'Socialist Governments':          event_007,
              'Fidel':                          event_008,
              'Vietnam Revolts':                event_009,
              'Blockade':                       event_010,
              'Korean War':                     event_011,
              'Romanian Abdication':            event_012,
              'Arab-Israeli War':               event_013,
              'Comecon':                        event_014,
              'Nasser':                         event_015,
              'Warsaw Pact Formed':             event_016,
              'De Gaulle Leads France':         event_017,
              'Captured Nazi Scientist':        event_018,
              'Truman Doctrine':                event_019,
              'Olympic Games':                  event_020,
              'NATO':                           event_021,
              'Independent Reds':               event_022,
              'Marshall Plan':                  event_023,
              'Indo-Pakistani War':             event_024,
              'Containment':                    event_025,
              'CIA Created':                    event_026,
              'US/Japan Mutual Defense Pact':   event_027,
              'Suez Crisis':                    event_028,
              'East European Unrest':           event_029,
              'Decolonization':                 event_030,
              'Red Scare/Purge':                event_031,
              'UN Intervention':                event_032,
              'Nuclear Test Ban':               event_034,
              'Brush War':                      event_036,
              'Central America Scoring':        event_037,
              'Southeast Asia Scoring':         event_038,
              'Arms Race':                      event_039,
              'Nuclear Subs':                   event_041,
              'Quagmire':                       event_042,
              'SALT Negotiations':              event_043,
              'Bear Trap':                      event_044,
              'How I Learned to Stop Worrying': event_046,
              'Junta':                          event_047,
              'Kitchen Debates':                event_048,
              'Missile Envy':                   event_049,
              '"We Will Bury You"':             event_050,
              'Brezhnev Doctrine':              event_051,
              'Portuguese Empire Crumbles':     event_052,
              'South African Unrest':           event_053,
              'Allende':                        event_054,
              'Willy Brandt':                   event_055,
              'Muslim Revolution':              event_056,
              'ABM Treaty':                     event_057,
              'Cultural Revolution':            event_058,
              'Flower Power':                   event_059,
              'U2 Incident':                    event_060,
              'OPEC':                           event_061,
              '"Lone Gunman"':                  event_062,
              'Colonial Rear Guards':           event_063,
              'Panama Canal Returned':          event_064,
              'Camp David Accords':             event_065,
              'Puppet Governments':             event_066,
              'Grain Sales to Soviets':         event_067,
              'John Paul II Elected Pope':      event_068,
              'Latin American Death Squads':    event_069,
              'OAS Founded':                    event_070,
              'Nixon Plays the China Card':     event_071,
              'Sadat Expels Soviets':           event_072,
              'The Voice of America':           event_074,
              'Liberation Theology':            event_075,
              'Ussuri River Skirmish':          event_076,
              '"Ask Not What Your Country..."': event_077,
              'Alliance for Progress':          event_078,
              'Africa Scoring':                 event_079,
              '"One Small Step..."':            event_080,
              'South America Scoring':          event_081,
              'Iranian Hostage Crisis':         event_082,
              'The Iron Lady':                  event_083,
              'Reagan Bombs Libya':             event_084,
              'Star Wars':                      event_085,
              'North Sea Oil':                  event_086,
              'The Reformer':                   event_087,
              'Marine Barracks Bombing':        event_088,
              'Soviets Shoot Down KAL-007':     event_089,
              'Glasnost':                       event_090,
              'Ortega Elected in Nicaragua':    event_091,
              'Terrorism':                      event_092,
              'Iran-Contra Scandal':            event_093,
              'Chernobyl':                      event_094,
              'Latin American Debt Crisis':     event_095,
              'Tear Down this Wall':            event_096,
              '"An Evil Empire"':               event_097,
              'Aldrich Ames Remix':             event_098,
              'Pershing II Deployed':           event_099,
              'Wargames':                       event_100,
              'Solidarity':                     event_101,
              'Iran-Iraq War':                  event_102,
              'Defectors':                      event_103,
              'The Cambridge Five':             event_104,
              'Special Relationship':           event_105,
              'NORAD':                          event_106,
              'Che':                            event_107,
              'Our Man in Tehran':              event_108,
              'Yuri and Samantha':              event_109,
              'AWACS Sale to Saudis':           event_110}

    # Effects
    def effect_042(self):
        """Quagmire - Effect"""
        eligible_cards = self.quagmire_bear_trap_eligible('usa')
        scoring_cards = self.scoring_cards_in_hand('usa')
        card_options = []
        scoring = False
        ars_this_turn = self.action_rounds[self.turn]

        if len(eligible_cards) == 0 and len(scoring_cards) == 0:
            log_string = 'No eligible cards to discard to Quagmire.'
            print(log_string)
            self.action_round_complete = True
            return
        elif len(eligible_cards) == 0 and len(scoring_cards) > 0:
            card_options = scoring_cards
            scoring = True
        elif len(eligible_cards) > 0 and len(scoring_cards) == 0:
            card_options = eligible_cards
        else:
            if (ars_this_turn - self.ar + 1) == len(scoring_cards):
                card_options = scoring_cards
                scoring = True
            else:
                card_options = eligible_cards

        if scoring:
            ui_string = 'Must play scoring card'
        else:
            ui_string = "Discard to Quagmire"
        print(ui_string)

        selected_card = self.select_a_card(card_options, 'usa')
        self.active_card = selected_card

        if scoring:
            self.trigger_event(selected_card)
        else:
            self.move_card(selected_card, 'discard')
            # Event 49 - Missile Envy: turn off missile envy if it was pitched to quagmire/trap
            if selected_card == self.cards['Missile Envy'] \
                    and self.cards['Missile Envy'].effect_active \
                    and self.cards['Missile Envy'].effect_player == 'usa':
                self.cards['Missile Envy'].effect_active = False
                self.cards['Missile Envy'].effect_player = ''

            roll = self.die_roll()

            if roll <= 4:
                log_string = "SUCCESS! USA rolled {r}. Quagmire is not longer active.".format(r=roll)
                print(log_string)
                self.cards['Quagmire'].effect_active = False
            else:
                log_string = "Failure. USA rolled {r}. Quagmire remains active.".format(r=roll)
                print(log_string)

        self.action_round_complete = True

    def effect_044(self):
        """Bear Trap - Effect"""
        eligible_cards = self.quagmire_bear_trap_eligible('ussr')
        scoring_cards = self.scoring_cards_in_hand('ussr')
        card_options = []
        scoring = False
        ars_this_turn = self.action_rounds[self.turn]

        if len(eligible_cards) == 0 and len(scoring_cards) == 0:
            log_string = 'No eligible cards to discard to Bear Trap.'
            print(log_string)
            self.action_round_complete = True
            return
        elif len(eligible_cards) == 0 and len(scoring_cards) > 0:
            card_options = scoring_cards
            scoring = True
        elif len(eligible_cards) > 0 and len(scoring_cards) == 0:
            card_options = eligible_cards
        else:
            if (ars_this_turn - self.ar + 1) == len(scoring_cards):
                card_options = scoring_cards
                scoring = True
            else:
                card_options = eligible_cards

        if scoring:
            ui_string = 'Must play scoring card'
        else:
            ui_string = "Discard to Bear Trap"
        print(ui_string)

        selected_card = self.select_a_card(card_options, 'ussr')
        self.active_card = selected_card

        if scoring:
            self.trigger_event(selected_card)
        else:
            self.move_card(selected_card, 'discard')

            # Event 49 - Missile Envy: turn off missile envy if it was pitched to quagmire/trap
            if selected_card == self.cards['Missile Envy'] \
                    and self.cards['Missile Envy'].effect_active \
                    and self.cards['Missile Envy'].effect_player == 'ussr':
                self.cards['Missile Envy'].effect_active = False
                self.cards['Missile Envy'].effect_player = ''

            roll = self.die_roll()

            if roll <= 4:
                log_string = "SUCCESS! USSR rolled {r}. Bear Trap is not longer active.".format(r=roll)
                print(log_string)
                self.cards['Bear Trap'].effect_active = False
            else:
                log_string = "Failure. USSR rolled {r}. Bear Trap remains active.".format(r=roll)
                print(log_string)

        self.action_round_complete = True

    def effect_059(self):
        """Flower Power - Effect"""
        card = self.active_card
        if self.active_player.side == 'usa':
            if self.cards['Flower Power'].effect_active:
                impacted_cards = [self.cards['Arab-Israeli War'],
                                  self.cards['Korean War'],
                                  self.cards['Brush War'],
                                  self.cards['Indo-Pakistani War'],
                                  self.cards['Iran-Iraq War']]

                # Remove AI War if Camp David is in effect
                if self.cards['Camp David Accords'].effect_active:
                    impacted_cards.remove(self.cards['Arab-Israeli War'])

                if card in impacted_cards:
                    log_string = "Flower Power in effect"
                    print(log_string)
                    self.change_score_by_side('ussr', 2)

    def effect_106(self):
        """NORAD - Effect"""
        if self.cards['NORAD'].effect_active \
                and self.norad_check \
                and self.countries['Canada'].controlled == 'usa':
            ui_string = 'Event 106 - NORAD active. Add 1 influence in a single country containing USA influence.'
            print(ui_string)
            self.ask_to_place_influence(self.countries_with_influence('usa'), 1, 'usa', 1, 1)
            self.norad_check = False

    # Dictionary of the effects
    effects = {'Quagmire':      effect_042,
               'Bear Trap':     effect_044,
               'Flower Power':  effect_059,
               'NORAD':         effect_106}

    # Functions to manipulate effects
    def trigger_effect(self, effect_card):
        eligible = effect_card.effect_active
        if eligible:
            self.effects[effect_card.name](self)

    # Functions to attempt coups
    def coup_attempt(self, country, ops, side, mil_ops=True):
        doubled_stability = int(country.stability) * 2
        coup_successful = False
        adjusted_ops = ops
        latin_adjustment = 0

        # Event 006 - China Card
        if self.active_card == self.cards['China'] and country.region == 'Asia':
            log_string = "Event 6 - China card: +1 operation point."
            print(log_string)
            adjusted_ops = ops + 1

        # Event 009 - Vietnam Revolts
        if self.cards['Vietnam Revolts'].effect_active and self.cards['Vietnam Revolts'].effect_side == side:
            if country.subregion == 'Southeast Asia':
                log_string = "Event 9 - Vietnam Revolts: +1 operation point."
                print(log_string)
                adjusted_ops = ops + 1

        # Event 069 - Latin American Death Squads
        log_string_latin = ""
        if self.cards['Latin American Death Squads'].effect_active:
            if country.region == 'Central America' or country.region == 'South America':
                if self.cards['Latin American Death Squads'].effect_side == side:
                    latin_adjustment = 1
                    log_string_latin = " + 1 from Latin American Death Squads"
                elif self.cards['Latin American Death Squads'].effect_side == self.opponent[side]:
                    latin_adjustment = -1
                    log_string_latin = " - 1 from Latin American Death Squads"

        roll = self.die_roll()
        modified_roll = roll + adjusted_ops + latin_adjustment

        # Event 43 - SALT Negotiations
        log_string_salt = ""
        if self.cards['SALT Negotiations'].effect_active:
            modified_roll = modified_roll - 1
            log_string_salt = " - 1 from SALT Negotiations"

        opponent_inf = self.get_opponent_influence(country.name, side)
        log_string = "Modified roll must be more than {d}. " \
                     "{s} rolled {r}{latin} + {o} ops{salt}, total of {t}.".format(d=doubled_stability,
                                                                                    s=side.upper(),
                                                                                    r=roll,
                                                                                   latin=log_string_latin,
                                                                                    o=adjusted_ops,
                                                                                    salt=log_string_salt,
                                                                                    t=modified_roll)
        print(log_string)

        if modified_roll > doubled_stability:
            coup_successful = True
            log_string = 'Coup result: Success!'
            print(log_string)
            influence_to_remove = modified_roll - doubled_stability
            if influence_to_remove > opponent_inf:
                influence_to_add = influence_to_remove - opponent_inf
                self.remove_influence(country.name, self.opponent[side], influence_to_remove)
                self.add_influence(country.name, side, influence_to_add)
            else:
                self.remove_influence(country.name, self.opponent[side], influence_to_remove)

        else:
            log_string = 'Coup result: Failure'
            print(log_string)

        if mil_ops:
            self.add_military_ops(side, adjusted_ops)

        if country.battleground:
            # Event 41 - Nuclear Subs
            if self.cards['Nuclear Subs'].effect_active and side == 'usa':
                log_string = 'DEFCON unchanged due to Event 41 - Nuclear Subs.'
                print(log_string)
                pass
            else:
                self.change_defcon(-1)

        # Event 109 - Yuri and Samantha
        if self.cards['Yuri and Samantha'].effect_active:
            if side == 'usa':
                log_string = "Event 109 - Yuri and Samantha activated due to USA coup:"
                print(log_string)
                self.change_score_by_side('ussr', 1)

        return coup_successful

    def action_coup_attempt(self, ops, side):
        attempt_completed = False
        while not attempt_completed:
            print("Coup Attempt")
            target_list = self.countries_with_influence(self.opponent[side])
            eligible_targets = self.checked_coup_targets(target_list, side, True)
            target = self.select_a_country(eligible_targets)

            if target is None:
                break
            else:
                confirmation = self.confirm_action("Attempt coup in {t}".format(t=target.name))
                if confirmation:
                    self.coup_attempt(target, ops, side)
                    attempt_completed = True
                    self.action_round_complete = True
                    self.conduct_operations_complete = True

    def ask_to_coup_attempt(self, country_list, ops, side, defcon_restrictions):
        attempt_completed = False
        coup_successful = False
        target = None
        eligible_targets = self.checked_coup_targets(country_list, side, defcon_restrictions)

        if len(eligible_targets) > 0:
            while not attempt_completed:
                print("Coup Attempt")
                target = self.select_a_country(eligible_targets, False)

                confirmation = self.confirm_action("Attempt coup in {t}".format(t=target.name))
                if confirmation:
                    coup_successful = self.coup_attempt(target, ops, side, False)
                    attempt_completed = True

        return [target, coup_successful]

    def checked_coup_targets(self, country_list, side, defcon_restrictions):
        eligible_targets = []

        for country in country_list:
            if self.check_coup_attempt(country, side, defcon_restrictions):
                eligible_targets.append(country)

        return eligible_targets

    def check_coup_attempt(self, country, side, defcon_restrictions):
        opponent_influence = self.get_opponent_influence(country.name, side)
        eligible = True

        if opponent_influence == 0:
            eligible = False

        if defcon_restrictions:
            if self.defcon < 5:
                if country.region == 'Europe':
                    eligible = False
                else:
                    if self.defcon < 4:
                        if country.region == 'Asia':
                            eligible = False
                        else:
                            if self.defcon < 3:
                                if country.region == 'Middle East':
                                    eligible = False

        # Effect 021 - NATO
        if country.nato and country.controlled == 'usa':
            eligible = False

        # Effect 027 - US/Japan Mutual Defense Pact
        if country.name == 'Japan' and self.cards['US/Japan Mutual Defense Pact'].effect_active:
            eligible = False

        # Effect 087 - The Reformer
        if country.region == 'Europe' and self.cards['The Reformer'].effect_active:
            eligible = False

        return eligible

    # Functions to attempt realignment rolls
    def realignment_roll(self, country, side):
        offense_roll = self.die_roll()
        defense_roll = self.die_roll()
        offense_influence = self.get_influence(country.name, side)
        defense_influence = self.get_opponent_influence(country.name, side)
        offense_more_inf = 0
        defense_more_inf = 0
        offense_adjacent_superpower = 0
        defense_adjacent_superpower = 0
        offense_iran_contra = 0
        defense_iran_contra = 0

        # Effect 93 - Iran-Contra Scandal
        if self.cards['Iran-Contra Scandal'].effect_active:
            if side == 'usa':
                offense_iran_contra = -1
            else:
                defense_iran_contra = -1

        # + 1 for each adjacent controlled country
        offense_adjacent_controlled = len(self.get_adjacent_controlled(country, side))
        defense_adjacent_controlled = len(self.get_adjacent_controlled(country, self.opponent[side]))

        # + 1 for having more influence in the target country
        if offense_influence > defense_influence:
            offense_more_inf = 1
        elif defense_influence > offense_influence:
            defense_more_inf = 1

        # + 1 for superpower adjacent
        if self.adjacent_to_superpower(country, side):
            offense_adjacent_superpower = 1
        if self.adjacent_to_superpower(country, self.opponent[side]):
            defense_adjacent_superpower = 1

        offense_roll_modified = (offense_roll +
                                 offense_adjacent_controlled +
                                 offense_more_inf +
                                 offense_adjacent_superpower +
                                 offense_iran_contra)
        defense_roll_modified = (defense_roll +
                                 defense_adjacent_controlled +
                                 defense_more_inf +
                                 defense_adjacent_superpower +
                                 defense_iran_contra)

        log_string = "{s} realignment attempt in {c}\n" \
                     "{o:4}\n" \
                     "Rolled:              {o1}\n" \
                     "Adjacent controlled: {o2}\n" \
                     "More influence:      {o3}\n" \
                     "Adjacent superpower: {o4}\n" \
                     "Iran-Contra effect:  {o5}\n" \
                     "\n" \
                     "{d:4}\n" \
                     "Rolled:              {d1}\n" \
                     "Adjacent controlled: {d2}\n" \
                     "More influence:      {d3}\n" \
                     "Adjacent superpower: {d4}\n" \
                     "Iran-Contra effect:  {d5}\n" \
                     "\n" \
                     "             TOTAL = {t}\n".format(s=side.upper(),
                                                         c=country.name,
                                                         o=side.upper(),
                                                         o1=offense_roll,
                                                         o2=offense_adjacent_controlled,
                                                         o3=offense_more_inf,
                                                         o4=offense_adjacent_superpower,
                                                         o5=offense_iran_contra,
                                                         d=self.opponent[side].upper(),
                                                         d1=defense_roll,
                                                         d2=defense_adjacent_controlled,
                                                         d3=defense_more_inf,
                                                         d4=defense_adjacent_superpower,
                                                         d5=defense_iran_contra,
                                                         t=offense_roll_modified - defense_roll_modified)
        print(log_string)

        if offense_roll_modified > defense_roll_modified:
            self.remove_influence(country.name, self.opponent[side], (offense_roll_modified - defense_roll_modified))
        elif defense_roll_modified > offense_roll_modified:
            self.remove_influence(country.name, side, (defense_roll_modified - offense_roll_modified))

    def action_realignment_roll(self, ops, side):
        possible_targets = self.countries_with_influence(self.opponent[side])
        attempts_made = self.ask_to_realignment_roll(possible_targets, ops, side)
        if attempts_made < ops:
            self.action_round_complete = True
            self.conduct_operations_complete = True

    def ask_to_realignment_roll(self, country_list, ops, side):
        realignments_completed = False
        realignments_to_attempt = ops
        cancellation = False
        china_bonus_given = False
        china_bonus_taken = False
        vietnam_bonus_given = False
        vietnam_bonus_taken = False

        while not realignments_completed:
            possible_targets = []
            targeted_countries = []
            for country in country_list:
                possible_targets.append(country)

            while realignments_to_attempt >= 0:
                eligible_targets = self.checked_realignment_targets(possible_targets, side)
                if len(eligible_targets) == 0:
                    realignments_completed = True
                    break

                if realignments_to_attempt == 0:
                    if self.active_card == self.cards['China'] and not china_bonus_taken:
                        check_for_china_bonus = self.are_all_targets_in_region(targeted_countries, 'Asia')
                        if check_for_china_bonus:
                            print('China bonus')
                            realignments_to_attempt = 1
                            china_bonus_given = True
                        else:
                            realignments_completed = True
                            break
                    else:
                        if self.cards['Vietnam Revolts'].effect_active and side == 'ussr' and not vietnam_bonus_taken:
                            vietnam_bonus = self.are_all_targets_in_subregion(targeted_countries, 'Southeast Asia')
                            if vietnam_bonus:
                                print('Vietnam bonus')
                                realignments_to_attempt = 1
                                vietnam_bonus_given = True
                            else:
                                realignments_completed = True
                                break

                        else:
                            realignments_completed = True
                            break
                elif realignments_to_attempt < ops:
                    continue_confirmation = self.confirm_action("Continue realignment attempts")
                    if not continue_confirmation:
                        realignments_completed = True
                        break

                print("Attempt a realignment roll ({r} remaining)".format(r=realignments_to_attempt))

                if china_bonus_given:
                    eligible_targets = self.checked_realignment_targets(self.countries_in_region('Asia'), side)

                if vietnam_bonus_given:
                    eligible_targets = self.checked_realignment_targets(self.countries_in_subregion('Southeast Asia'), side)

                target = self.select_a_country(eligible_targets)
                print(target)
                if target is None:
                    cancellation = True
                    break

                target_confirmation = self.confirm_action("Attempt a realignment in {t}".format(t=target.name))
                if target_confirmation:
                    self.realignment_roll(target, side)
                    realignments_to_attempt = realignments_to_attempt - 1

                    if target not in targeted_countries:
                        targeted_countries.append(target)
                    if china_bonus_given:
                        china_bonus_taken = True
                    if vietnam_bonus_given:
                        vietnam_bonus_taken = True

            if cancellation:
                continue_confirmation = self.confirm_action("Continue realignment attempts")
                if not continue_confirmation:
                    realignments_completed = True

        return realignments_to_attempt

    def checked_realignment_targets(self, country_list, side):
        eligible_targets = []

        for country in country_list:
            if self.check_realignment_roll(country, side):
                eligible_targets.append(country)

        return eligible_targets

    def check_realignment_roll(self, country, side):
        opponent_influence = self.get_opponent_influence(country.name, side)
        eligible = True

        if opponent_influence == 0:
            eligible = False

        if self.defcon < 5:
            if country.region == 'Europe':
                eligible = False
            else:
                if self.defcon < 4:
                    if country.region == 'Asia':
                        eligible = False
                    else:
                        if self.defcon < 3:
                            if country.region == 'Middle East':
                                eligible = False

        # Effect 021 - NATO
        if country.nato and country.controlled == 'usa':
            eligible = False

        # Effect 027 - US/Japan Mutual Defense Pact
        if country.name == 'Japan' and self.cards['US/Japan Mutual Defense Pact'].effect_active:
            eligible = False

        return eligible

    # Functions to place influence
    def action_place_influence(self, ops, side):
        placement_completed = False
        while not placement_completed:
            influence_to_place = ops
            target_list = []
            targeted_countries = []
            cancelled = False
            china_bonus_given = False
            vietnam_bonus_given = False

            if self.cards['Chernobyl'].effect_active and self.cards['Chernobyl'].effect_side == side:
                log_string = "Event 94 - Chernoble in effect. {s} cannot place influece in {r}.".format(s=side.upper(),
                                                                                                     r=self.chernobyl)
                print(log_string)
                all_countries = self.accessible_countries(side)
                possible_targets = []
                for country in all_countries:
                    if country.region != self.chernobyl:
                        possible_targets.append(country)
            else:
                possible_targets = self.accessible_countries(side)

            while influence_to_place > 0:
                print("Place {i} influence".format(i=influence_to_place))
                target = self.select_a_country(possible_targets)
                if target is None:
                    cancelled = True
                    break
                amount = self.select_influence_amount(target, influence_to_place)
                if amount is None:
                    break
                target_list.append([target, amount])
                targeted_countries.append(target)
                possible_targets.remove(target)
                influence_to_place = influence_to_place - amount

                if influence_to_place == 0:
                    check_for_china_bonus = self.are_all_targets_in_region(targeted_countries, 'Asia')
                    check_for_vietnam_bonus = self.are_all_targets_in_subregion(targeted_countries, 'Southeast Asia')
                    if self.active_card == self.cards['China'] and check_for_china_bonus and not china_bonus_given:
                        log_string = "Event 6 - China bonus"
                        print(log_string)
                        influence_to_place = 1
                        china_bonus_given = True
                        possible_targets = []
                        for country in self.accessible_countries(side):
                            if country.region == 'Asia':
                                possible_targets.append(country)
                    elif self.cards['Vietnam Revolts'].effect_active and side == 'ussr' and check_for_vietnam_bonus and not vietnam_bonus_given:
                        log_string = "Event 9 - Vietnam bonus"
                        print(log_string)
                        influence_to_place = 1
                        vietnam_bonus_given = True
                        possible_targets = []
                        for country in self.accessible_countries(side):
                            if country.subregion == 'Southeast Asia':
                                possible_targets.append(country)

            if cancelled:
                break
            elif self.check_influence_targets_add(target_list, side):
                if influence_to_place == 0:
                    confirmation = self.confirm_action("Place influence in {t}".format(t=target_list))
                    if confirmation:
                        self.place_influence_from_list(target_list, side)
                        placement_completed = True
                        self.action_round_complete = True
                        self.conduct_operations_complete = True
            else:
                user_input = input('Invalid influence placement. Restart influence placement? (y/n): ').lower()
                if user_input == 'n':
                    break

    def ask_to_place_influence(self, country_list, influence, side, min_inf=None, max_inf=None):
        placement_completed = False
        while not placement_completed:
            influence_to_place = influence
            target_list = []
            possible_targets = []
            for country in country_list:
                possible_targets.append(country)

            while influence_to_place > 0:
                print("Place {i} influence".format(i=influence_to_place))
                target = self.select_a_country(possible_targets)
                if target is None:
                    break
                amount = self.select_influence_amount(target, influence_to_place, min_inf, max_inf)
                if amount is None:
                    break
                target_list.append([target, amount])
                possible_targets.remove(target)
                influence_to_place = influence_to_place - amount

            if self.check_influence_targets_add(target_list, side):
                if influence_to_place == 0:
                    confirmation = self.confirm_action("Place influence in {t}".format(t=target_list))
                    if confirmation:
                        self.place_influence_from_list(target_list, side)
                        placement_completed = True
            else:
                user_input = input('Invalid influence placement. Restart influence placement? (y/n): ').lower()
                if user_input == 'n':
                    break

    def ask_to_remove_influence(self, country_list, influence, side, min_inf=None, max_inf=None):
        removal_completed = False
        while not removal_completed:
            influence_to_remove = influence
            target_list = []
            possible_targets = []
            for country in country_list:
                if self.get_opponent_influence(country.name, side) > 0:
                    possible_targets.append(country)

            while influence_to_remove > 0:
                print("Remove {i} influence".format(i=influence_to_remove))
                target = self.select_a_country(possible_targets)
                if target is None:
                    break
                amount = self.select_influence_amount(target, influence_to_remove, min_inf, max_inf)
                if amount is None:
                    break
                target_list.append([target, amount])
                possible_targets.remove(target)
                influence_to_remove = influence_to_remove - amount
                if len(possible_targets) == 0:
                    break

            if self.check_influence_targets_remove(target_list, side):
                if influence_to_remove == 0 or len(possible_targets) == 0:
                    confirmation = self.confirm_action("Remove influence in {t}".format(t=target_list))
                    if confirmation:
                        self.remove_influence_from_list(target_list, side)
                        removal_completed = True
            else:
                print('Invalid influence removal. Restart influence removal')

    def ask_to_remove_all_influence(self, country_list, number_of_countries, side):
        removal_completed = False
        while not removal_completed:
            countries_to_remove = number_of_countries
            target_list = []
            possible_targets = []
            for country in country_list:
                if self.get_opponent_influence(country.name, side) > 0:
                    possible_targets.append(country)

            while countries_to_remove > 0:
                print("Remove all influence in {n} countries".format(n=countries_to_remove))
                target = self.select_a_country(possible_targets)
                if target is None:
                    break
                target_list.append(target)
                possible_targets.remove(target)
                countries_to_remove = countries_to_remove - 1
                if len(possible_targets) == 0:
                    break

            if countries_to_remove == 0 or len(possible_targets) == 0:
                # Logging
                log_countries = '\n'
                for country in target_list:
                    log_countries = log_countries + country.name + '\n'

                confirmation = self.confirm_action(
                    "Remove all {s} influence in:{t}".format(s=self.opponent[side].upper(),
                                                             t=log_countries))
                if confirmation:
                    self.remove_all_influence_from_list(target_list, side)
                    removal_completed = True

    def place_influence_from_list(self, country_list, side):
        for item in country_list:
            country = item[0]
            amount = item[1]
            influence_used = 0
            while influence_used < amount:
                if country.controlled == self.opponent[side]:
                    self.add_influence(country.name, side, 1)
                    influence_used = influence_used + 2
                else:
                    self.add_influence(country.name, side, 1)
                    influence_used = influence_used + 1

    def remove_influence_from_list(self, country_list, side):
        for item in country_list:
            country = item[0]
            amount = item[1]
            self.remove_influence(country.name, self.opponent[side], amount)

    def remove_all_influence_from_list(self, country_list, side):
        for country in country_list:
            self.remove_all_influence(country.name, self.opponent[side])

    def check_enough_influence_to_add(self, country, side, influence):
        eligible = True
        side_inf = self.get_influence(country.name, side)
        opp_inf = self.get_opponent_influence(country.name, side)
        stability = country.stability
        influence_to_add = influence

        while influence_to_add > 0:
            if (opp_inf - side_inf) >= stability:
                if influence_to_add < 2:
                    eligible = False
                    break
                else:
                    side_inf = side_inf + 1
                    influence_to_add = influence_to_add - 2
            else:
                influence_to_add = influence_to_add - 1

        return eligible

    def check_enough_influence_to_remove(self, country, side, influence):
        eligible = True
        opp_inf = self.get_opponent_influence(country.name, side)

        if opp_inf < influence:
            eligible = False

        return eligible

    def check_influence_targets_add(self, country_list, side):
        eligible = True

        for item in country_list:
            country = item[0]
            amount = item[1]
            if not self.check_enough_influence_to_add(country, side, amount):
                eligible = False

        return eligible

    def check_influence_targets_remove(self, country_list, side):
        eligible = True

        for item in country_list:
            country = item[0]
            amount = item[1]
            if not self.check_enough_influence_to_remove(country, side, amount):
                eligible = False

        return eligible

    def select_influence_amount(self, country, ops, min_inf=None, max_inf=None):
        influence_amount = None
        while True:
            user_input = input("How much influence in {c}: ".format(c=country.name))
            if user_input.isdigit():
                selection_amount = int(user_input)
                if max_inf is None and min_inf is None:
                    if selection_amount <= ops:
                        influence_amount = selection_amount
                        break
                elif min_inf is None:
                    if selection_amount <= ops and selection_amount <= max_inf:
                        influence_amount = selection_amount
                        break
                elif max_inf is None:
                    if selection_amount <= ops and selection_amount >= min_inf:
                        influence_amount = selection_amount
                        break
                else:
                    if selection_amount <= ops and selection_amount >= min_inf and selection_amount <= max_inf:
                        influence_amount = selection_amount
                        break
            elif user_input.lower() == 'x':
                break
        return influence_amount

    # Function to conduct operations
    def conduct_operations(self, side, ops):
        self.conduct_operations_complete = False

        while not self.conduct_operations_complete:
            selected_action = self.select_operation()
            adjusted_card_ops = self.adjust_ops(ops, side, 1, 4)
            if selected_action == 'c':
                self.action_coup_attempt(adjusted_card_ops, side)
            elif selected_action == 'i':
                self.action_place_influence(adjusted_card_ops, side)
            elif selected_action == 'r':
                self.action_realignment_roll(adjusted_card_ops, side)

    # Functions for the headline phase
    def headline_phase(self):
        self.phase = 'headline'
        print('HEADLINE PHASE')
        if self.sides['usa'].space_level >= 4 and self.sides['ussr'].space_level < 4:
            ussr_headline = self.select_a_headline('ussr')
            print(ussr_headline.name)
            usa_headline = self.select_a_headline('usa')
        elif self.sides['ussr'].space_level >= 4 and self.sides['usa'].space_level < 4:
            usa_headline = self.select_a_headline('usa')
            print(usa_headline.name)
            ussr_headline = self.select_a_headline('ussr')
        else:
            usa_headline = self.select_a_headline('usa')
            ussr_headline = self.select_a_headline('ussr')

        headline_order = self.evaluate_headlines(usa_headline, ussr_headline)

        for headline in headline_order:
            self.phasing = headline[0]
            self.active_card = headline[1]
            self.trigger_event(headline[1])
            if headline[1].name == 'Defectors':
                self.move_card(ussr_headline, 'discard')

    def select_a_headline(self, side):
        eligible_cards = self.get_available_cards(side, False)
        if self.cards['UN Intervention'] in eligible_cards:
            eligible_cards.remove(self.cards['UN Intervention'])

        headline = self.select_a_card(eligible_cards, side)
        return headline

    def evaluate_headlines(self, usa_headline, ussr_headline):
        order = []

        if usa_headline.name == 'Defectors':
            order = [['usa', usa_headline]]
        elif usa_headline.ops > ussr_headline.ops or usa_headline.ops == ussr_headline.ops:
            order = [['usa', usa_headline], ['ussr', ussr_headline]]
        elif ussr_headline.ops > usa_headline.ops:
            order = [['ussr', ussr_headline], ['usa', usa_headline]]

        return order

    # Functions to manage action rounds
    def action_round(self, side):
        self.action_round_complete = False
        self.phase = "{s} action round".format(s=side)
        self.phasing = side
        self.active_player = self.sides[side]
        self.active_card = None
        self.norad_check = False
        log_string = self.phase.upper()
        print(log_string)
        print(self.line)

        # Event 42 - Quagmire
        if self.cards['Quagmire'].effect_active and side == 'usa':
            self.trigger_effect(self.cards['Quagmire'])
            selected_action = ''

        # Event 44 - Bear Trap
        if self.cards['Bear Trap'].effect_active and side == 'ussr':
            self.trigger_effect(self.cards['Bear Trap'])
            selected_action = ''

        # Event 50 - "We Will Bury You"
        if self.cards['"We Will Bury You"'].effect_active and side == 'usa':
            ui_string = "! Event 50 - We Will Bury You active. USA must play UN Intervention or USSR scores 3 points!"
            print(ui_string)
            self.we_will_un_check = True

        while not self.action_round_complete:
            # Set eligible cards
            if self.cards['Missile Envy'].effect_active and side == self.cards['Missile Envy'].effect_player:
                # Event 49 - Missile Envy
                eligible_cards = [self.cards['Missile Envy']]
            else:
                eligible_cards = self.get_available_cards(side, True)

            # Check to see if UN intervention is in hand, if it is, make sure you can play it
            for card in eligible_cards:
                if card.name == 'UN Intervention':
                    un_eligible = self.check_UN_intervention_eligible(self.phasing)
                    if not un_eligible:
                        eligible_cards.remove(card)

            # Check to see if China is face up
            if self.cards['China'] in eligible_cards:
                if not self.cards['China'].face_up:
                    eligible_cards.remove(self.cards['China'])

            selected_card = self.select_a_card(eligible_cards, side)
            self.active_card = selected_card
            adjusted_card_ops = self.adjust_ops(selected_card.ops, side, 1, 4)

            if selected_card.event_type == 'scoring':
                confirmation = self.confirm_action('Play {c}'.format(c=selected_card.name))
                if confirmation:
                    self.trigger_event(selected_card)
                    selected_action = 'e'
                    break
                else:
                    selected_action = 'x'
            else:
                if selected_card.event_type == self.opponent[side]:
                    selected_action = self.select_action(selected_card, True)
                    if selected_action == 'e':
                        self.trigger_event(selected_card)
                        self.action_round_complete = False
                        while not self.action_round_complete:
                            selected_action = self.select_action_limited(False, True, True, True, False)
                            if selected_action == 'c':
                                self.action_coup_attempt(adjusted_card_ops, side)
                            elif selected_action == 'i':
                                self.action_place_influence(adjusted_card_ops, side)
                            elif selected_action == 'r':
                                self.action_realignment_roll(adjusted_card_ops, side)
                    elif selected_action == 'c':
                        self.action_coup_attempt(adjusted_card_ops, side)
                        self.trigger_event(selected_card)
                    elif selected_action == 'i':
                        self.action_place_influence(adjusted_card_ops, side)
                        self.trigger_event(selected_card)
                    elif selected_action == 'r':
                        self.action_realignment_roll(adjusted_card_ops, side)
                        self.trigger_event(selected_card)
                    elif selected_action == 's':
                        self.action_space_race(selected_card, adjusted_card_ops, side)
                    elif selected_action == 'x':
                        pass

                elif selected_card.name == 'China':
                    selected_action = self.select_action_limited(False, True, True, True, True)
                    if selected_action == 'c':
                        self.action_coup_attempt(adjusted_card_ops, side)
                    elif selected_action == 'i':
                        self.action_place_influence(adjusted_card_ops, side)
                    elif selected_action == 'r':
                        self.action_realignment_roll(adjusted_card_ops, side)
                    elif selected_action == 's':
                        self.action_space_race(selected_card, adjusted_card_ops, side)
                    elif selected_action == 'x':
                        pass

                elif self.cards['Missile Envy'].effect_active and side == self.cards['Missile Envy'].effect_player:
                    # Event 49 - Missile Envy
                    selected_action = self.select_action_limited(False, True, True, True, True)
                    if selected_action == 'c':
                        self.action_coup_attempt(adjusted_card_ops, side)
                        self.move_card(selected_card, 'discard')
                    elif selected_action == 'i':
                        self.action_place_influence(adjusted_card_ops, side)
                        self.move_card(selected_card, 'discard')
                    elif selected_action == 'r':
                        self.action_realignment_roll(adjusted_card_ops, side)
                        self.move_card(selected_card, 'discard')
                    elif selected_action == 's':
                        self.action_space_race(selected_card, adjusted_card_ops, side)

                else:
                    selected_action = self.select_action(selected_card)
                    if selected_action == 'e':
                        # Event 50 - "We Will Bury You" > turn off UN check if UN is played
                        if selected_card.name == 'UN Intervention':
                            self.we_will_un_check = False
                        self.trigger_event(selected_card)
                        break
                    elif selected_action == 'c':
                        self.action_coup_attempt(adjusted_card_ops, side)
                        self.move_card(selected_card, 'discard')
                    elif selected_action == 'i':
                        self.action_place_influence(adjusted_card_ops, side)
                        self.move_card(selected_card, 'discard')
                    elif selected_action == 'r':
                        self.action_realignment_roll(adjusted_card_ops, side)
                        self.move_card(selected_card, 'discard')
                    elif selected_action == 's':
                        self.action_space_race(selected_card, adjusted_card_ops, side)
                    elif selected_action == 'x':
                        pass

        if selected_action == 'e' or selected_action == 'c' or selected_action == 'i' or selected_action == 'r':
            self.trigger_effect(self.cards['Flower Power'])

        # Selected action is '' only when Bear Trap or Quagmire are in play
        if selected_action != '':
            if selected_card.name == 'China':
                self.give_opponent_china_card(side)

            # Event 49 - Missile Envy (turn off missile envy)
            if self.cards['Missile Envy'].effect_active \
                    and selected_card == self.cards['Missile Envy'] \
                    and side == self.cards['Missile Envy'].effect_player:
                self.cards['Missile Envy'].effect_active = False
                self.cards['Missile Envy'].effect_player = ''

        # Event 50 - "We Will Bury You"
        if self.cards['"We Will Bury You"'].effect_active and side == 'usa':
            # If the USA played a card other than UN intervention that did not have a scoring element, score 3 to USSR
            # If the card had a scoring element, the USSR will have already received points
            if self.we_will_un_check:
                ui_string = 'Event 50 - We Will Bury You: USA did not play UN Intervention.'
                print(ui_string)
                self.change_score_by_side('ussr', 3)
            self.cards['"We Will Bury You"'].effect_active = False
            self.we_will_un_check = False

        # Event 106 - NORAD
        self.trigger_effect(self.cards['NORAD'])

        log_string = "Action round complete."
        print(log_string)
        print(self.line)

    def select_a_card(self, card_list, side):
        available_cards = card_list
        card_strings = self.format_available_cards(available_cards)
        available_card_numbers = []
        selected_card = None

        print("{s} select a card:".format(s=side.upper()))

        cards_printed = 0
        while cards_printed < len(card_strings):
            output_string = "{c:>2}| {s}".format(c=(cards_printed + 1),
                                                 s=card_strings[cards_printed])
            print(output_string)
            available_card_numbers.append(cards_printed + 1)
            cards_printed += 1

        while True:
            user_input = input("Selection: ")
            if user_input.isdigit():
                selected_number = int(user_input)
                if selected_number in available_card_numbers:
                    selected_card = available_cards[selected_number - 1]
                    break
                elif 10 in available_card_numbers and selected_number == 0:
                    selected_card = available_cards[9]
                    break

        return selected_card

    def select_a_country(self, country_list, allow_cancelling=True):
        sorted_country_list = sorted(country_list, key=lambda x: x.name)
        available_country_numbers = []
        selected_country = None

        print("Select a country to target:")

        countries_printed = 0
        while countries_printed < len(sorted_country_list):
            output_string = "{c:>2}| {s}".format(c=(countries_printed + 1),
                                                 s=sorted_country_list[countries_printed].name)
            print(output_string)
            available_country_numbers.append(countries_printed + 1)
            countries_printed += 1

        if allow_cancelling:
            print(" x| --Cancel--")
        while True:
            user_input = input("Selection: ")
            if user_input.isdigit():
                selected_number = int(user_input)
                if selected_number in available_country_numbers:
                    selected_country = sorted_country_list[selected_number - 1]
                    break
            else:
                if allow_cancelling:
                    if user_input.lower() == 'x':
                        break

        return selected_country

    def select_option(self, option_list):
        option = None
        available_options = []

        print("Select an option:")
        for option in option_list:
            print("{l}| {t}".format(l=option[0], t=option[1]))
            available_options.append(option[0])

        while True:
            user_input = input("Selection: ").lower()
            if user_input in available_options:
                return user_input
                break

    def check_space_race(self, ops, side):
        max_space_attempts = 1
        phasing_space_level = self.sides[side].space_level
        opponent_space_level = self.sides[self.opponent[side]].space_level
        required_ops = {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4}

        if phasing_space_level >= 2 and opponent_space_level < 2:
            max_space_attempts = 2

        if (self.sides[side].space_attempts < max_space_attempts and
                ops >= required_ops[(phasing_space_level + 1)]):
            return True
        else:
            return False

    def action_space_race(self, card, ops, side):
        if self.check_space_race(ops, side):
            confirmation = self.confirm_action("Make a space race attempt with {c}".format(c=card.name))
            if confirmation:
                self.space_race_attempt(side)
                self.move_card(card, 'discard')
                self.action_round_complete = True

    def space_race_attempt(self, side):
        roll_requirements = {1: 3, 2: 4, 3: 3, 4: 4, 5: 3, 6: 4, 7: 3, 8: 2}
        max_roll = roll_requirements[(self.sides[side].space_level + 1)]

        roll = self.die_roll()
        log_string = "Roll between 1-{l}. {s} rolled {r}.".format(s=side.upper(), r=roll, l=max_roll)
        print(log_string)

        if roll <= max_roll:
            log_string = 'Space race attempt result: Success!'
            print(log_string)
            self.increase_space_level(side)
        else:
            log_string = 'Space race attempt result: Failure.'
            print(log_string)
        self.sides[side].space_attempts += 1

    def select_action(self, card, opponent=False):
        if opponent:
            action_options = " e| Trigger opponent event first\n" \
                             " c| Coup attempt\n" \
                             " i| Place influence\n" \
                             " r| Realignment roll\n" \
                             " s| Space race\n" \
                             " x| --Choose another card--"
        else:
            action_options = " e| Play event\n" \
                             " c| Coup attempt\n" \
                             " i| Place influence\n" \
                             " r| Realignment roll\n" \
                             " s| Space race\n" \
                             " x| --Choose another card--"
        print(self.line)
        print("Select use for " + card.name + ':')
        print(action_options)
        while True:
            selected_action = input("Selection: ").lower()
            if selected_action in ['e', 'c', 'i', 'r', 's', 'x']:
                return selected_action

    def select_action_limited(self, event, coup, influence, realignment, space):
        action_options = ""
        selectable_actions = []

        if event:
            action_options = action_options + " e| Play event\n"
            selectable_actions.append('e')

        if coup:
            action_options = action_options + " c| Coup attempt\n"
            selectable_actions.append('c')

        if influence:
            action_options = action_options + " i| Place influence\n"
            selectable_actions.append('i')

        if realignment:
            action_options = action_options + " r| Realignment roll\n"
            selectable_actions.append('r')

        if space:
            action_options = action_options + " s| Space race\n"
            selectable_actions.append('s')

        print(self.line)
        print("Select action:")
        print(action_options)
        while True:
            selected_action = input("Selection: ").lower()
            if selected_action in selectable_actions:
                return selected_action

    def select_operation(self):
        operation_options = " c| Coup attempt\n" \
                            " i| Place influence\n" \
                            " r| Realignment roll\n"

        print(self.line)
        print("Select operation:")
        print(operation_options)
        while True:
            selected_action = input("Selection: ").lower()
            if selected_action in ['c', 'i', 'r']:
                return selected_action

    def confirm_action(self, text):
        while True:
            confirmation = input("Confirm action - {t} (y/n): ".format(t=text)).lower()
            if confirmation == 'y':
                return True
            elif confirmation == 'n':
                return False

    def adjust_ops(self, card_ops, side, low, high):
        adjusted_ops = card_ops + self.sides[side].ops_adjustment
        if card_ops == 0:
            adjusted_ops = 0
        elif adjusted_ops < low:
            adjusted_ops = low
        elif adjusted_ops > high:
            adjusted_ops = high

        return adjusted_ops

    def check_held_cards(self):
        ussr_hand = self.get_available_cards('ussr', False)
        usa_hand = self.get_available_cards('usa', False)
        ussr_held_scoring = False
        usa_held_scoring = False

        if len(ussr_hand) > 0:
            for card in ussr_hand:
                if card.event_type == 'scoring':
                    ussr_held_scoring = True

        if len(usa_hand) > 0:
            for card in usa_hand:
                if card.event_type == 'scoring':
                    usa_held_scoring = True

        if usa_held_scoring and not ussr_held_scoring:
            self.sides['ussr'].winner = True
            self.game_active = False
            self.action_round_complete = True
            log_string = "Game over due to USA holding a score card. Winner: USSR"
            print(log_string)
        elif ussr_held_scoring and not usa_held_scoring:
            self.sides['usa'].winner = True
            self.game_active = False
            self.action_round_complete = True
            log_string = "Game over due to USSR holding a score card. Winner: USA"
            print(log_string)
        elif ussr_held_scoring and usa_held_scoring:
            self.sides['usa'].winner = True
            self.game_active = False
            self.action_round_complete = True
            log_string = "Game over due to both sides holding a score card. Winner: USA"
            print(log_string)

    def turn_cleanup(self):
        for side in self.sides.values():
            side.space_attempts = 0
            side.ops_adjustment = 0

        # Turn off all turn based effects
        for card in self.cards.values():
            if card.name == 'China':
                pass
            elif card.effect_turn and card.effect_active:
                card.effect_active = False
                log_string = "{c} is no longer active.".format(c=card.name)
                print(log_string)

    # Initial influence placement
    def extra_initial_influence(self):
        if self.extra_inf == 'bid':
            self.bid_for_sides()
        elif self.extra_inf == 'handicap':
            options = [['a', "Give USA bonus influence"],
                       ['b', "Give USSR bonus influence"]]
            response = self.select_option(options)
            if response == 'a':
                side = 'usa'
            elif response == 'b':
                side = 'ussr'

            while True:
                user_input = input("How many bonus influence to give to {s}?: ".format(s=side.upper()))
                if user_input.isdigit():
                    selection_amount = int(user_input)
                    break

            if side == 'usa':
                self.usa_handicap = selection_amount
            elif side == 'ussr':
                self.ussr_handicap = selection_amount

    def bid_for_sides(self):
        pass

    def initial_placement(self):
        self.ask_to_place_influence(self.countries_in_subregion('Eastern Europe'), 6, 'ussr')
        if self.ussr_handicap > 0:
            self.ask_to_place_influence(self.countries_with_influence('ussr'), self.ussr_handicap, 'ussr')

        self.ask_to_place_influence(self.countries_in_subregion('Western Europe'), 7, 'usa')
        if self.usa_handicap > 0:
            self.ask_to_place_influence(self.countries_with_influence('usa'), self.usa_handicap, 'usa')


def main():
    game = TwilightStruggleGame("Game 2022-02-01", "2022-02-01", "1", "")

    game.extra_initial_influence()
    game.initial_placement()

    for turn in range(1, game.turns + 1):
        game.turn = turn

        log_string = "\n--- TURN {t} ---\n".format(t=turn)
        print(log_string)

        # Phase A - Improve DEFCON Status
        game.change_defcon(1)

        if turn > 1:
            # Phase B - Deal Cards
            game.deal_cards()

        # Phase C - Headline Phase
        game.headline_phase()

        # Phase D - Action Rounds
        for ar in range(1, game.action_rounds[game.turn] + 1):
            game.ar = ar
            log_string = "\n--- TURN {t} | ACTION ROUND {a} ---".format(t=turn, a=ar)
            print(log_string)

            log_string = "Score: {s}\nDEFCON: {d}\n".format(s=game.score, d=game.defcon)
            print(log_string)

            game.action_round('ussr')
            game.action_round('usa')

        if game.cards['North Sea Oil'].effect_active:
            if len(game.get_available_cards('usa', False)) > 0:
                log_string = 'Bonus USA action round from North Sea Oil'
                print(log_string)
                game.action_round('usa')

        game.turn_cleanup()

        # Phase E - Check Military Operations
        game.check_required_military_ops()
        game.reset_military_ops()

        # Phase F - Check held card
        game.check_held_cards()

        # Phase G - Flip China Card
        game.cards['China'].flip_face_up()

        # Phase H - Advance turn marker (add in mid/late game cards)
        if turn == 3:
            game.move_all_cards('deck', 'mid war')
        elif turn == 7:
            game.move_all_cards('deck', 'late war')

    game.final_scoring()


main()
