import sys
import decimal
import copy
import random
import json

random.seed()

iterations = 10000  # Quantity of test runs to produce

death_tally = [0,0,0] # Initialize the deaths tally

range_size = 10 # define the size of the die


def parse_clargs ( args ):

    file1 = ""
    file2 = ""

    if len(args) >= 2:
        file1 = detect_json_extension( args[1] )
        if len(args) >= 3:
            file2 = detect_json_extension( args[2] )
        else:
            print "You must specify two fleets!"
            exit(1)
    else:
        print "You must specify two fleets!"
        exit(1)

    return file1, file2

def detect_json_extension( any_string ):
    
    if len(any_string) >= 5:
        if any_string[-5:] != ".json":
            any_string += ".json"
    else:
        any_string += ".json"

    return any_string


def import_file ( target_file ):

    with open(target_file, 'r') as f:
        file_string = file.read( f )
    return file_string


def count_hits ( prob_list, range_size ):
    """
    Randomly generate a count for hits.
    """
    
    hits = 0
    for each in prob_list:
        if random.randint(1, range_size) >= each:
            hits += 1
    return hits



def build_extra_hits ( fleet ):
    """
    You can prevent sustain damage for your whole fleet by specifying this value as 0 in your fleet data.

    This function will pass if extra hits is already set to any value other than None.
    """
    if fleet['extra hits'] == "None": # Only do this if none are passed... use string "None" because json requires strings.
        fleet['extra hits'] == 0
        fleet['extra hits'] = fleet.get('War Sun',0)+fleet.get('Dreadnought',0)+fleet.get('Capital Ship',0)+fleet.get('Mechanized Unit',0)

    return fleet


def generate_hit_prob_list( fleet ):
    """
    Generate the list of possible hits from a fleet list.

    The fleet data type should be a dict using the ship name as a key and the ship
    quantity as a value.
    """

    hit_chances = []

    catalog = fleet['Catalog']
     
    for name in fleet.keys():
        '''
        This if block is awful, it is trading one problem for another.
        The problem it fixes is having non-ship keys in the fleet dicts.
        The problem it creates is collisions between the catalog and fleet dicts.
        Simple solution is shape the fleet like a dict and have 'type' specified in
        both the fleet and catalog dictionaries, then take a cross section of items
        that have the ship 'type'
        '''
        if name in catalog.keys():
            for i_values in range(fleet[name] * catalog[name]['hits']):
                hit_chances.append( catalog[name]['to hit'] )
        else:
            pass # skip keys in the fleet list that aren't ships... revamp this check.

    return hit_chances


def fleet_damage_outcomes( fleet, hits ):

    fleet = build_extra_hits( fleet )

    # Use a hit prioritization method to calculate remaining possible fleets.
        
    # If we sustain, then sustain all hits first
    if fleet['hit priority'] == "sustain":
        while fleet['extra hits'] > 0 and hits > 0:
            fleet['extra hits'] = fleet['extra hits'] - 1
            hits -= 1
    for item in fleet['loss priority']: # Silently ends if fleet destroyed.
        while fleet.get(item,0) > 0 and hits > 0:
            if item in [ "Dreadnought", "War Sun", "Capital Ship", "Mechanized Unit" ] and fleet['extra hits'] > 0:
                fleet['extra hits'] = fleet['extra hits'] - 1
                hits -= 1
            else:
                fleet[item] -= 1
                hits -= 1
    for item in [x for x in fleet['Catalog'] if x not in fleet['loss priority']]:
        while fleet.get(item,0) > 0 and hits > 0:
            if item in [ "Dreadnought", "War Sun", "Capital Ship", "Mechanized Unit" ] and fleet['extra hits'] > 0:
                fleet['extra hits'] = fleet['extra hits'] - 1
                hits -= 1
            else:
                fleet[item] -= 1
                hits -= 1
    return fleet


def play_round( fleet1, fleet2, range_size ):
    """
    Run one round with two fleets.
    """
    
    # These lists of potential hits feed into the hitrange generators.
    hitprob1 = generate_hit_prob_list( fleet1 )
    hitprob2 = generate_hit_prob_list( fleet2 )

    fleet1_hits = count_hits( hitprob1, range_size )
    fleet2_hits = count_hits( hitprob2, range_size )

    fleet1 = fleet_damage_outcomes( fleet1, fleet2_hits )
    fleet2 = fleet_damage_outcomes( fleet2, fleet1_hits )

    return ( fleet1, fleet2 )


def fleet_survival_check( fleet ):
    """
    If no ships remain that are in the catalog, then the fleet is destroyed.
    """
    surviving_ships = 0
    for each in fleet['Catalog'].keys():
        
        surviving_ships += fleet.get(each,0)
    
    return surviving_ships


def play_to_death( fleet1, fleet2, range_size, death_tally ):
   
    

    while fleet_survival_check(fleet1) > 0 and fleet_survival_check(fleet2) > 0:
        fleet1, fleet2 = play_round( fleet1, fleet2, range_size )

    if fleet_survival_check(fleet1) == 0 and fleet_survival_check(fleet2) == 0:
        death_tally[2] += 1
        return death_tally
    elif fleet_survival_check(fleet1) == 0:
        death_tally[0] += 1
        return death_tally
    elif fleet_survival_check(fleet2) == 0:
        death_tally[1] += 1
        return death_tally
 


def monte_carlo_iterator(  iterations, range_size, death_tally, fleet1_s, fleet2_s ):
    """
    Serve as the iterator or controller function.
    """ 

    fleet1 = json.loads( fleet1_s )
    fleet1_static = json.loads( fleet1_s )
    fleet2 = json.loads( fleet2_s )
    fleet2_static = json.loads( fleet2_s )
 
    for i in range(iterations):
        for each in fleet1_static.keys():
            fleet1[each] = fleet1_static[each]
        for each in fleet2_static.keys():
            fleet2[each] = fleet2_static[each]
        death_tally = play_to_death( fleet1, fleet2, range_size, death_tally )

    fleet1_name = fleet1.get('name', "Fleet 1")
    fleet2_name = fleet2.get('name', "Fleet 2")

    print
    print fleet1_name, "is destroyed:\t", death_tally[0] / decimal.Decimal(iterations) * 100, "percent of iterations.\t", death_tally[0]
    print fleet2_name, "is destroyed:\t", death_tally[1] / decimal.Decimal(iterations) * 100, "percent of iterations.\t", death_tally[1]
    print "Mutual Destruction:\t", death_tally[2] / decimal.Decimal(iterations) * 100, "percent of iterations.\t", death_tally[2]
    print

fleet_1_file, fleet_2_file = parse_clargs( sys.argv )

# Import specified data:
fleet1_s = import_file( fleet_1_file )
fleet2_s = import_file( fleet_2_file )

monte_carlo_iterator(  iterations, range_size, death_tally, fleet1_s, fleet2_s )

