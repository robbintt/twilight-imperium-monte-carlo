import copy
import random
import json

# Rough tally for now.
death_tally = [0,0,0]

ship_catalog_file = "./ship_models.json"
fleet_1_file = "./test_fleet_1.json"
fleet_2_file = "./test_fleet_2.json"

iterations = 10000
range_size = 12 # define the size of the die


def import_json ( target_file ):

    with open(target_file, 'r') as f:
        json_dict = json.load( f )
    return json_dict


def count_hits( prob_list, range_size ):
    """
    Randomly generate a count for hits.
    """
    
    hits = 0
    for each in prob_list:
        if random.randint(1, range_size) >= each:
            hits += 1
    return hits


def generate_hitrange( prob_list, times, range_size):
    """
    Generate a hit probability spectrum for a prob_list
    """
    
    hitrange = [0]*(len(prob_list)+1)
    for i in range(times):
        hitrange[ count_hits( prob_list, range_size ) ] += 1
 
    return hitrange


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


def build_extra_hits ( fleet ):
    """
    Generate the extra hits for the fleet based on the number of ships
    that can sustain damage.

    If this value is specified already, skip this.
    """
    if fleet['extra hits'] == "None": # Only do this if none are passed... use string "none" because json requires strings.
        fleet['extra hits'] = fleet.get('War Sun',0)+fleet.get('Dreadnought',0)+fleet.get('Custom Ship',0)

    return fleet


def fleet_damage_outcomes( target_fleet, hitrange, ship_catalog ):


    build_extra_hits( target_fleet )

    # Use a hit prioritization method to calculate remaining possible fleets.
    fleet_outcomes = []
    for each in range(0,len(hitrange)):
        fleet = copy.deepcopy(target_fleet)
        # If we sustain, then sustain all hits first
        if fleet['hit priority'] == "sustain":
            while fleet['extra hits'] > 0 and each > 0:
                fleet['extra hits'] = fleet['extra hits'] - 1
                each -= 1
        for item in fleet['loss priority']: # Silently ends if fleet destroyed.
            while fleet.get(item,0) > 0 and each > 0:
                if item in [ "Dreadnought", "War Sun", "Custom Ship" ] and fleet['extra hits'] > 0:
                    fleet['extra hits'] = fleet['extra hits'] - 1
                    each -= 1
                else:
                    fleet[item] = fleet[item] - 1
                    each -= 1
        fleet_outcomes.append(fleet)

    return fleet_outcomes

def fleet_survival_check( fleet, ship_catalog ):
    """
    If no ships remain that are in the catalog, then the fleet is destroyed.
    """

    surviving_ships = 0
    for each in ship_catalog.keys():
        surviving_ships += fleet.get(each,0)
    
    return surviving_ships


def play_round( fleet1, fleet2, iterations, range_size, ship_catalog ):
    """
    Run one round with two fleets.
    """


    # These lists of potential hits feed into the hitrange generators.
    hitprob1 = generate_hit_prob_list( fleet1, ship_catalog )
    hitprob2 = generate_hit_prob_list( fleet2, ship_catalog )

    # RNG is used to generate approximate probability distributions.
    hitrange1 = generate_hitrange( hitprob1, iterations, range_size )
    hitrange2 = generate_hitrange( hitprob2, iterations, range_size )

    fleet1_outcomes = fleet_damage_outcomes( fleet1, hitrange2, ship_catalog )
    fleet2_outcomes = fleet_damage_outcomes( fleet2, hitrange1, ship_catalog )

    return ( fleet1_outcomes, fleet2_outcomes )


def play_to_death( fleet1, fleet2, iterations, range_size, ship_catalog, death_tally ):

    fleet1_outcomes, fleet2_outcomes = play_round( fleet1, fleet2, iterations, range_size, ship_catalog )

    # Discrete list of all outcomes.
    all_outcomes = []
    for each in fleet1_outcomes:
        for item in fleet2_outcomes:
            all_outcomes.append( [each, item] )

    # Strip out the miss/miss scenario at all times.
    all_outcomes.pop(0)

    for each in all_outcomes:
        if fleet_survival_check(each[0], ship_catalog) > 0 and fleet_survival_check(each[1], ship_catalog) > 0:
            death_tally = play_to_death( each[0], each[1], iterations, range_size, ship_catalog, death_tally )
        else:
            if fleet_survival_check(each[0], ship_catalog) == 0 and fleet_survival_check(each[1], ship_catalog) == 0:
                death_tally[2] += 1
                return death_tally
            if fleet_survival_check(each[0], ship_catalog) == 0:
                death_tally[0] += 1
                return death_tally
            if fleet_survival_check(each[1], ship_catalog) == 0:
                death_tally[1] += 1
                return death_tally


# Import specified data:
ship_catalog = import_json( ship_catalog_file )
fleet1 = import_json( fleet_1_file )
fleet2 = import_json( fleet_2_file )


print play_to_death( fleet1, fleet2, iterations, range_size, ship_catalog, death_tally )
