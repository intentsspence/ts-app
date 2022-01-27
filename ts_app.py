# App to play twilight struggle

defcon = 5
phasing_player = 'USA'


def adjust_defcon(adjustment_value):
    global defcon
    defcon = defcon + adjustment_value

    # Adjust defcon to 5 if above 5
    if defcon > 5:
        defcon = 5

    # Check to see if the defcon has ended the game
    # TODO - Add game ending conditions if defcon = 1


class Country:
    """Base class for a country in a game"""
    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Country: %s>" % self.name

    def __str__(self):
        return self.name


class TwilightStruggleCountry(Country):
    """Class of countries specific to Twilight Struggle"""

    def __init__(self, n, r, sr, st, bg, usa_i, ussr_i):
        Country.__init__(self, n)

        if r not in ['Africa', 'Asia', 'Central America', 'Europe', 'Middle East', 'South America']:
            raise ValueError("Error creating Twilight Struggle country. Region must be one of: Africa, Asia, Central America, Europe, Middle East, or South America")
        self.region = r

        if sr not in ['Both Europe', 'Eastern Europe', 'Western Europe', 'Southeast Asia']:
            raise ValueError("Error creating Twilight Struggle country. Subregion must be one of: 'Both Europe', 'Eastern Europe', 'Western Europe', or 'Southeast Asia'")
        self.subregion = sr

        if not st.isdigit() and (int(st) > 4 or int(st) < 1):
            raise ValueError("Error creating Twilight Struggle country. Stability must be a number between 1 and 4")
        self.stability = st

        if bg not in ['True', 'False']:
            raise ValueError("Error creating Twilight Struggle country. Battleground must be True or False.")
        self.battleground = True if bg == 'True' else False

        if not usa_i.isdigit():
            raise ValueError("Error creating Twilight Struggle country. USA influence must be a number.")
        self.usa_influence = usa_i

        if not ussr_i.isdigit():
            raise ValueError("Error creating Twilight Struggle country. USSR influence must be a number.")
        self.ussr_influence = ussr_i


    # def __init__(self):
    #     self.__create_countries()
    #
    # def __create_countries(self):
    #     with open('countries/country_list.csv') as handle:
    #         header = handle.readline()
    #         lines = handle.read().splitlines()
    #
    #         for line in lines:
    #             sdf


