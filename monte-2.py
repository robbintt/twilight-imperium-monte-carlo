import decimal
import copy
import random
import json

random.seed()

# Rough tally for now.
death_tally = [0,0,0]

ship_catalog_file = "./ship_models.json"
fleet_1_file = "./test_fleet_1.json"
fleet_2_file = "./test_fleet_2.json"

iterations = 10000
range_size = 12 # define the size of the die


def import_file ( target_file ):

    with open(target_file, 'r') as f:
        file_string = file.read( f )
    return file_string


def count_hits( prob_list, range_size ):
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
    Generate the extra hits for the fleet based on the number of ships
    that can sustain damage.

    If this value is specified already, skip this.
    """
    if fleet['extra hits'] == "None": # Only do this if none are passed... use string "None" because json requires strings.
        fleet['extra hits'] == 0
        fleet['extra hits'] = fleet.get('War Sun',0)+fleet.get('Dreadnought',0)+fleet.get('Custom Ship',0)

    return fleet


def generate_hit_prob_list( fleet, ship_catalog ):
    """
    Generate the list of possible hits from a fleet list.

    The ship catalog is a dict of dicts imported from a json file.

    The fleet data type should be a dict using the ship name as a key and the ship
    quantity as a value.
    """

    hit_chances = []
    for name, quantity in fleet.items():
        name = name.encode('ascii','replace')
        '''
        This if block is awful, it is trading one problem for another.
        The problem it fixes is having non-ship keys in the fleet dicts.
        The problem it creates is collisions between the ship_catalog and fleet dicts.
        Simple solution is shape the fleet like a dict and have 'type' specified in
        both the fleet and catalog dictionaries, then take a cross section of items
        that have the ship 'type'
        '''
        if name in ship_catalog.keys():
            try:
                hit_prob = ship_catalog[name]['to hit']
            except:
                raise

            hit_chances += ( [hit_prob] * quantity * ship_catalog[name]['hits'] )
        else:
            pass # skip keys in the fleet list that aren't ships... revamp this data format.

    return hit_chances


def fleet_damage_outcomes( fleet, fleet1_hits, ship_catalog ):

    fleet = build_extra_hits( fleet )

    # Use a hit prioritization method to calculate remaining possible fleets.
        
    # If we sustain, then sustain all hits first
    if fleet['hit priority'] == "sustain":
        while fleet['extra hits'] > 0 and fleet1_hits > 0:
            fleet['extra hits'] = fleet['extra hits'] - 1
            fleet1_hits -= 1
    for item in fleet['loss priority']: # Silently ends if fleet destroyed.
        while fleet.get(item,0) > 0 and fleet1_hits > 0:
            if item in [ "Dreadnought", "War Sun", "Custom Ship" ] and fleet['extra hits'] > 0:
                fleet['extra hits'] = fleet['extra hits'] - 1
                fleet1_hits -= 1
            else:
                fleet[item] = fleet[item] - 1
                fleet1_hits -= 1
    return fleet


def play_round( fleet1, fleet2, range_size, ship_catalog ):
    """
    Run one round with two fleets.
    """
    
    # These lists of potential hits feed into the hitrange generators.
    hitprob1 = generate_hit_prob_list( fleet1, ship_catalog )
    hitprob2 = generate_hit_prob_list( fleet2, ship_catalog )

    fleet1_hits = count_hits( hitprob1, range_size )
    fleet2_hits = count_hits( hitprob2, range_size )

    fleet1 = fleet_damage_outcomes( fleet1, fleet2_hits, ship_catalog )
    fleet2 = fleet_damage_outcomes( fleet2, fleet1_hits, ship_catalog )

    return ( fleet1, fleet2 )


def fleet_survival_check( fleet, ship_catalog ):
    """
    If no ships remain that are in the catalog, then the fleet is destroyed.
    """
    surviving_ships = 0
    for each in ship_catalog.keys():
        
        surviving_ships += fleet.get(each,0)
    
    return surviving_ships


def play_to_death( fleet1, fleet2, range_size, ship_catalog, death_tally ):
   
    while fleet_survival_check(fleet1, ship_catalog) > 0 and fleet_survival_check(fleet2, ship_catalog) > 0:
        fleet1, fleet2 = play_round( fleet1, fleet2, range_size, ship_catalog )

    if fleet_survival_check(fleet1, ship_catalog) == 0 and fleet_survival_check(fleet2, ship_catalog) == 0:
        death_tally[2] += 1
        return death_tally
    elif fleet_survival_check(fleet1, ship_catalog) == 0:
        death_tally[0] += 1
        return death_tally
    elif fleet_survival_check(fleet2, ship_catalog) == 0:
        death_tally[1] += 1
        return death_tally
 


def monte_carlo_iterator(  iterations, range_size, ship_catalog, death_tally, fleet1_s, fleet2_s ):
    """
    Serve as the iterator or controller function.
    """ 

 
    for i in range(iterations):
        fleet1 = json.loads( fleet1_s )
        fleet2 = json.loads( fleet2_s )
        death_tally = play_to_death( fleet1, fleet2, range_size, ship_catalog, death_tally )

    print "Fleet 1 losses:", death_tally[0], death_tally[0] / decimal.Decimal(iterations) * 100, "percent."
    print "Fleet 2 losses:", death_tally[1], death_tally[1] / decimal.Decimal(iterations) * 100, "percent."
    print "Mutual Destruction:", death_tally[2], death_tally[2] / decimal.Decimal(iterations) * 100, "percent."


# Import specified data:
ship_catalog_s = import_file( ship_catalog_file )
ship_catalog_dict = json.loads( ship_catalog_s )
print "Ship Catalog:", ship_catalog_dict

fleet1_s = import_file( fleet_1_file )
fleet2_s = import_file( fleet_2_file )


print fleet1_s, "Fleet 1"
print fleet2_s, "Fleet 2"


monte_carlo_iterator(  iterations, range_size, ship_catalog_dict, death_tally, fleet1_s, fleet2_s )

