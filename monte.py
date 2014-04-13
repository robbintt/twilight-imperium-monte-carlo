import copy
import random
import json

ship_catalog_file = "./ship_models.json"
iterations = 10000
range_size = 12 # define the size of the die

fleet1 = { 
    "loss priority" : [ "Fighter","Destroyer","Carrier","Cruiser","Dreadnought","War Sun","Custom Ship" ],
    "extra hits" : None, 
    "hit priority": "sustain", 
    "Dreadnought" : 1 }

fleet2 = { 
    "loss priority" : [ "Fighter","Destroyer","Carrier","Cruiser","Dreadnought","War Sun","Custom Ship" ],
    "extra hits" : None, 
    "hit priority": "protect", 
    "Carrier" : 1, 
    "Fighter" : 4 }




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
    if fleet['extra hits'] == None: # Only do this if none are passed.
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

    """
    # Use a hit prioritization method to calculate remaining possible fleets.
    fleet2_outcomes = []
    for each in range(0,len(hitrange1)):
        fleet2_t = copy.deepcopy(fleet2)
        # If we sustain, then sustain all hits first
        if fleet2_t['hit priority'] == "sustain":
            while fleet2_t['extra hits'] > 0 and each > 0:
                fleet2_t['extra hits'] = fleet2['extra hits'] - 1
                each -= 1
        for item in fleet2_t['loss priority']: # Silently ends if fleet destroyed.
            while fleet2_t.get(item,0) > 0 and each > 0:
                if item in [ "Dreadnought", "War Sun", "Custom Ship" ] and fleet2_t['extra hits'] > 0:
                    fleet2_t['extra hits'] = fleet2_t['extra hits'] - 1
                    each -= 1
                else:
                    fleet2_t[item] = fleet2_t[item] - 1
                    each -= 1
        fleet2_outcomes.append(fleet2_t)

    fleet1_outcomes = []
    for each in range(0,len(hitrange2)):
        fleet1_t = copy.deepcopy(fleet1)
        # If we sustain, then sustain all hits first
        if fleet1_t['hit priority'] == "sustain":
            while fleet1_t['extra hits'] > 0 and each > 0:
                fleet1_t['extra hits'] = fleet1['extra hits'] - 1
                each -= 1
        for item in fleet1_t['loss priority']: # Silently ends if fleet destroyed.
            while fleet1_t.get(item,0) > 0 and each > 0:
                if item in [ "Dreadnought", "War Sun", "Custom Ship" ] and fleet1_t['extra hits'] > 0:
                    fleet1_t['extra hits'] = fleet1_t['extra hits'] - 1
                    each -= 1
                else:
                    fleet1_t[item] = fleet1_t[item] - 1
                    each -= 1
        fleet1_outcomes.append(fleet1_t)
    """


    return ( fleet1_outcomes, fleet2_outcomes )




ship_catalog = import_json( ship_catalog_file )

print play_round( fleet1, fleet2, iterations, range_size, ship_catalog )
