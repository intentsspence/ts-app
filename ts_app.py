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

    def __init__(self, n, no, p, e, o, r, opt):
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

        self.played = False


class TwilightStruggleChinaCard(Card):
    """Class for the china card"""
    # TODO - change name of china card to 'The China Card' here and in rest of program. Maybe

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

    def __init__(self, n, s):
        Player.__init__(self, n)

        if s not in ['usa', 'ussr']:
            raise ValueError("Error creating Twilight Struggle country. Controlled must be 'usa' or 'ussr'")
        self.side = s

        # Set phasing player to false
        self.phasing = False

        # Set space level to 0
        self.space_level = 0

        # Set mil ops to 0
        self.military_ops = 0

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


class TwilightStruggleGame(CardGame):
    """Class of an individual game of Twilight Struggle"""

    turns = 10
    action_rounds = {1: 6, 2: 6, 3: 6, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7, 9: 7, 10: 7}

    def __init__(self, n, d, opt):
        CardGame.__init__(self, n, d)

        if not opt.isdigit() and int(opt) != 1 and int(opt) != 0:
            raise ValueError("Error creating Twilight Struggle game. Optional cards parameter must be a 1 or a 0.")
        self.optional_cards = True if int(opt) == 1 else False

        self.defcon = 5
        self.score = 0
        self.turn = 1
        self.game_active = True
        self.phasing = ''

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
        self.pre_reqs = {'NATO':        ['Marshall Plan', 'Warsaw Pact Formed'],
                         'Solidarity':  ['John Paul II Elected Pope']}
        self.prevents = {'Arab Israeli War':        'Camp David Accords',
                         'Socialist Governments':   'The Iron Lady',
                         'OPEC':                    'North Sea Oil',
                         'Willy Brandt':            'Tear Down This Wall',
                         'Flower Power':            'An Evil Empire',
                         'Muslim Revolution':       'AWACS Sale to Saudis'}

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
        pile_list = ['early war', 'mid war', 'late war', 'deck', 'discard', 'removed', 'USA hand', 'USSR hand', 'USA China', 'USSR China']

        for pile in pile_list:
            self.add_pile(CardPile(pile))

    def __create_players(self):
        # TODO - Change the "create players" function to allow for user input

        player_list = [['Player 1', 'ussr'], ['Player 2', 'usa']]

        for p_list in player_list:
            player = TwilightStrugglePlayer(p_list[0], p_list[1])
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

        log_string = "Setup complete\n-----------------------------------"
        print(log_string)

    # Function to adjust defcon
    def change_defcon(self, adjustment_value):
        self.defcon = self.defcon + adjustment_value

        # Adjust defcon to 5 if above 5
        if self.defcon > 5:
            self.defcon = 5

        if self.defcon < 2:
            if self.sides['usa'].phasing:
                self.sides['ussr'].winner = True
            elif self.sides['ussr'].phasing:
                self.sides['usa'].winner = True

            self.defcon = 1
            self.game_active = False

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
            if self.countries[border].controlled == side or border == side.upper():
                adjacent_controlled.append(self.countries[border])

        return adjacent_controlled

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

    def get_influence(self, country, side):
        """Returns an int with the country's current influence"""
        influence = 0
        if side == 'usa':
            influence = country.usa_influence
        elif side == 'ussr':
            influence = country.ussr_influence
        return influence

    def print_influence(self, country_name):
        """Quick method to see the current influence. Takes a string"""
        usa_inf = self.get_influence(self.countries[country_name], 'usa')
        ussr_inf = self.get_influence(self.countries[country_name], 'ussr')
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
            log_string = "Game over. Winner: USA"
            print(log_string)
        elif self.score <= -20:
            self.sides['ussr'].winner = True
            self.game_active = False
            log_string = "Game over. Winner: USSR"
            print(log_string)

    def change_score(self, points):
        self.score = self.score + points

        self.check_game_end()

    def change_score_by_side(self, side, points):
        if side == 'usa':
            self.score = self.score + points
        elif side == 'ussr':
            self.score = self.score - points
        log_string = "{s} scored {p} points. Score is now {score}.".format(s=side.upper(), p=points, score=self.score)
        print(log_string)
        self.check_game_end()

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

        return countries_in_subregion

    def battleground_countries_in_region(self, region):
        bg_countries_in_region = []
        for country in self.countries.values():
            if country.region == region and country.battleground:
                bg_countries_in_region.append(country)

        return bg_countries_in_region

    def controlled_in_region(self, region, side):
        country_list = self.countries_in_region(region)
        controlled_list = []

        for country in country_list:
            if side == 'usa' and country.controlled == 'usa':
                controlled_list.append(country)
            elif side == 'ussr' and country.controlled == 'ussr':
                controlled_list.append(country)

        return controlled_list

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
                if border not in accessible_countries and border != 'USA' and border != 'USSR':
                    accessible_countries.append(self.countries[border])
        return accessible_countries

    def total_battlegrounds_controlled(self, side):
        country_list = []

        for country in self.countries.values():
            if country.controlled == side and country.battleground:
                country_list.append(country.name)

        return len(country_list)

    # Functions for moving cards around
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
            log_string_2 = 'China card is face down.'
            print(log_string_2)

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
            entry = "| {0} {1:7} {2:1} {3}".format(card.ops, card.event_type, star, card.name)
            print(entry)
            hand_list.append(entry)

        return hand_list

    def sort_cards(self, cards_to_sort, sort='ops', sort_china=True):

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

    def get_available_cards(self, side, sort):
        available_cards = list(self.piles[self.hands[side]].get_cards_in_pile().values())
        if self.cards['China'] in self.piles[self.china_owner[side]].get_cards_in_pile().values():
            available_cards.append(self.cards['China'])

        sorted_available_cards = self.sort_cards(available_cards, sort)

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
        else:
            eligible = True

        return eligible

    def trigger_event(self, card):
        eligible = self.check_event_eligibility(card)

        if eligible:
            log_string = "Event {no} - {na}.".format(no=card.number,
                                                            na=card.name)
            print(log_string)
            self.events[card.name](self)
            card.played = True

            if card.removed:
                self.move_card(card, 'removed')
            else:
                self.move_card(card, 'discard')
        else:
            self.move_card(card, 'discard')

    def war_card(self, country, side, success, mil_ops, points, itself):
        number_adjacent = len(self.get_adjacent_controlled(country, self.opponent[side]))
        if itself:
            if country.controlled == self.opponent[side]:
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
            influence = self.get_influence(country, self.opponent[side])
            self.remove_all_influence(country.name, self.opponent[side])
            self.add_influence(country.name, side, influence)
        else:
            log_string_2 = "Failure."
            print(log_string_2)

    def score_type(self, region):
        usa_countries = 0
        ussr_countries = 0
        usa_bgs = 0
        ussr_bgs = 0
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

    def score_card(self, region, presence, domination, control):
        usa_total = 0
        ussr_total = 0
        usa_score_type = self.score_type(region)[0]
        ussr_score_type = self.score_type(region)[1]
        usa_adjacent_bonus = 0
        ussr_adjacent_bonus = 0
        usa_bg_bonus = len(self.battlegrounds_controlled_in_region(region, 'usa'))
        ussr_bg_bonus = len(self.battlegrounds_controlled_in_region(region, 'ussr'))
        countries_in_region = self.countries_in_region(region)

        score_dict = {'no influence': 0, 'presence': presence, 'domination': domination,'control': control}

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

        log_string_usa = "USA has {t}.\nScore for {tl}: {s}\n" \
                         "Adjacent countries: {a}\nBattlegrounds: {b}\nTotal: {st}\n".format(t=usa_score_type.upper(),
                                                                                             tl=usa_score_type,
                                                                                             s=score_dict[usa_score_type],
                                                                                             a=usa_adjacent_bonus,
                                                                                             b=usa_bg_bonus,
                                                                                             st=usa_total)
        log_string_ussr = "USSR has {t}.\nScore for {tl}: {s}\n" \
                          "Adjacent countries: {a}\nBattlegrounds: {b}\nTotal: {st}\n".format(t=ussr_score_type.upper(),
                                                                                              tl=ussr_score_type,
                                                                                              s=score_dict[ussr_score_type],
                                                                                              a=ussr_adjacent_bonus,
                                                                                              b=ussr_bg_bonus,
                                                                                              st=ussr_total)
        print(log_string_usa)
        print(log_string_ussr)
        if usa_total > ussr_total:
            self.change_score_by_side('usa', usa_total - ussr_total)
        if ussr_total > usa_total:
            self.change_score_by_side('ussr', ussr_total - usa_total)

    # Specific events
    def event_001(self):
        """Asia Scoring"""
        self.score_card('Asia', 3, 7, 9)

    def event_002(self):
        """Europe Scoring"""
        self.score_card('Europe', 3, 7, 100)

    def event_003(self):
        """Middle East Scoring"""
        self.score_card('Middle East', 3, 5, 7)

    def event_004(self):
        """Duck and Cover"""
        self.change_defcon(-1)
        points = 5 - self.defcon
        self.change_score_by_side('usa', points)

    def event_008(self):
        """Fidel"""
        self.remove_all_influence('Cuba', 'usa')
        self.add_influence_to_control('Cuba', 'ussr')

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

    def event_015(self):
        """Nasser"""
        usa_inf = self.countries['Egypt'].usa_influence
        inf_to_remove = math.ceil(usa_inf / 2)
        self.add_influence('Egypt', 'ussr', 2)
        self.remove_influence('Egypt', 'usa', inf_to_remove)

    def event_018(self):
        """Captured Nazi Scientist"""
        self.increase_space_level(self.phasing)

    def event_034(self):
        """Nuclear Test Ban"""
        points = self.defcon - 2
        self.change_score_by_side(self.phasing, points)
        self.change_defcon(2)

    def event_037(self):
        """Central America Scoring"""
        self.score_card('Central America', 1, 3, 5)

    def event_038(self):
        """Southeast Asia Scoring"""
        usa_score = 0
        usa_thailand = 0
        usa_total = 0
        ussr_score = 0
        ussr_thailand = 0
        ussr_total = 0
        country_list = self.countries_in_subregion('Southeast Asia')

        for country in country_list:
            if country.controlled == 'usa':
                usa_score += 1
            elif country.controlled == 'ussr':
                ussr_score += 1

        if self.countries['Thailand'].controlled == 'usa':
            usa_thailand += 1
            log_string_usa_2 = {"Bonus for Thailand: 1"}

        if self.countries['Thailand'].controlled == 'ussr':
            ussr_thailand += 1
            log_string_usa_2 = {"Bonus for Thailand: 1"}

        usa_total = usa_score + usa_thailand
        ussr_total = ussr_score + ussr_thailand

        log_string_usa = "USA controlled countries: {c}\nBonus for Thailand: {b}\nTotal: {t}\n".format(c=usa_score,
                                                                                                       b=usa_thailand,
                                                                                                       t=usa_total)
        log_string_ussr = "USSR controlled countries: {c}\nBonus for Thailand: {b}\nTotal: {t}\n".format(c=ussr_score,
                                                                                                         b=ussr_thailand,
                                                                                                         t=ussr_total)
        print(log_string_usa)
        print(log_string_ussr)
        if usa_total > ussr_total:
            self.change_score_by_side('usa', usa_total - ussr_total)
        if ussr_total > usa_total:
            self.change_score_by_side('ussr', ussr_total - usa_total)

    def event_039(self):
        """Arms Race"""
        phasing_mil_ops = self.sides[self.phasing].military_ops
        opponent_mil_ops = self.sides[(self.opponent[self.phasing])].military_ops
        if (phasing_mil_ops > opponent_mil_ops) and (phasing_mil_ops < self.defcon):
            self.change_score_by_side(self.phasing, 1)
        elif (phasing_mil_ops > opponent_mil_ops) and (phasing_mil_ops >= self.defcon):
            self.change_score_by_side(self.phasing, 3)

    def event_048(self):
        """Kitchen Debates"""
        usa_battlegrounds = self.total_battlegrounds_controlled('usa')
        ussr_battlegrounds = self.total_battlegrounds_controlled('ussr')

        if usa_battlegrounds > ussr_battlegrounds:
            self.change_score_by_side('usa', 2)

    def event_052(self):
        """Portuguese Empire Crumbles"""
        self.add_influence('Angola', 'ussr', 2)
        self.add_influence('SE African States', 'ussr', 2)

    def event_054(self):
        """Allende"""
        self.add_influence('Chile', 'ussr', 2)

    def event_058(self):
        """Cultural Revolution"""
        if self.cards['China'] in self.piles['USA China'].get_cards_in_pile().values():
            self.move_china_card('USSR China', True)
        elif self.cards['China'] in self.piles['USSR China'].get_cards_in_pile().values():
            self.change_score_by_side('ussr', 1)
        else:
            raise ValueError("China card must be in USA hand or USSR hand")

    def event_061(self):
        """OPEC"""
        opec_list = ['Egypt', 'Iran', 'Libya', 'Saudi Arabia', 'Iraq', 'Gulf States', 'Venezuela']
        points = 0

        for country in opec_list:
            if self.countries[country].controlled == 'ussr':
                points += 1

        self.change_score_by_side('ussr', points)

    def event_064(self):
        """Panama Canal Returned"""
        self.add_influence('Panama', 'usa', 1)
        self.add_influence('Costa Rica', 'usa', 1)
        self.add_influence('Venezuela', 'usa', 1)

    def event_068(self):
        """John Paul II Elected Pope"""
        self.remove_influence('Poland', 'ussr', 2)
        self.add_influence('Poland', 'usa', 1)

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

    def event_078(self):
        """Alliance for Progress"""
        ca_battlegrounds = len(self.battlegrounds_controlled_in_region('Central America', 'usa'))
        sa_battlegrounds = len(self.battlegrounds_controlled_in_region('South America', 'usa'))
        self.change_score_by_side('usa', (ca_battlegrounds + sa_battlegrounds))

    def event_079(self):
        """Africa Scoring"""
        self.score_card('Africa', 1, 4, 6)

    def event_080(self):
        """One Small Step..."""
        if self.sides[self.phasing].space_level < self.sides[self.opponent[self.phasing]].space_level:
            self.sides[self.phasing].space_level += 1
            self.increase_space_level(self.phasing)

    def event_081(self):
        """South America Scoring"""
        self.score_card('South America', 2, 5, 6)

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

    def event_092(self):
        """Terrorism"""
        if self.piles['USA hand'].get_pile_size() > 0:
            discard = self.piles['USA hand'].random_card()
            self.move_card(discard, 'discard')
        if self.cards['Iranian Hostage Crisis'].played:
            if self.piles['USA hand'].get_pile_size() > 0:
                discard = self.piles['USA hand'].random_card()
                self.move_card(discard, 'discard')

    def event_101(self):
        """Solidarity"""
        self.add_influence('Poland', 'usa', 3)

    # Dictionary of the events
    events = {'Asia Scoring':               event_001,
              'Europe Scoring':             event_002,
              'Middle East Scoring':        event_003,
              'Duck and Cover':             event_004,
              'Socialist Governments':      event_008,
              'Korean War':                 event_011,
              'Romanian Abdication':        event_012,
              'Arab-Israeli War':           event_013,
              'Nasser':                     event_015,
              'Captured Nazi Scientist':    event_018,
              'Nuclear Test Ban':           event_034,
              'Central America Scoring':    event_037,
              'Southeast Asia Scoring':     event_038,
              'Arms Race':                  event_039,
              'Kitchen Debates':            event_048,
              'Portuguese Empire Crumbles': event_052,
              'Allende':                    event_054,
              'Cultural Revolution':        event_058,
              'OPEC':                       event_061,
              'Panama Canal Returned':      event_064,
              'John Paul II Elected Pope':  event_068,
              'Nixon Plays the China Card': event_071,
              'Sadat Expels Soviets':       event_072,
              'Alliance for Progress':      event_078,
              'Africa Scoring':             event_079,
              '"One Small Step..."':        event_080,
              'South America Scoring':      event_081,
              'Iranian Hostage Crisis':     event_082,
              'The Iron Lady':              event_083,
              'Reagan Bombs Libya':         event_084,
              'Terrorism':                  event_092,
              'Solidarity':                 event_101}

    # Functions to manage action rounds
    def action_round(self, side):
        # TODO - add check active action round effects
        hand = self.format_hand()
        print(hand)


g = TwilightStruggleGame("Game 2022-02-01", "2022-02-01", "1")
clist = g.get_available_cards('ussr', 'ops')
g.format_available_cards(clist)
