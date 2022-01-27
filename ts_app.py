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
