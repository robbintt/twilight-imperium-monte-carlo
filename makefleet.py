"""

Take standard input and generate a properly formatted fleet.

"""


import json



def json_exporter( object1, file_name ):

    with open( str(file_name)+'.json', 'w') as f:
        json.dump( object1, f, indent=2, separators=(',',':') )
    

def retrieve_raw_input( text_string ):

    input_value = int( raw_input(text_string) )
    
    return input_value


def get_user_input( fleet ):
    """
    Get user input and export it.
    """


    fleet['name'] = raw_input('Name:')
    file_name = raw_input('Select a filename, do not include the extension:')


    fleet['Carrier'] = retrieve_raw_input('# of Carriers:')
    fleet['Fighter'] = retrieve_raw_input('# of Fighters:')
    fleet['Destroyer'] = retrieve_raw_input('# of Destroyers:')
    fleet['Cruiser'] = retrieve_raw_input('# of Cruisers:')
    fleet['Dreadnought'] = retrieve_raw_input('# of Dreadnoughts:')
    fleet['War Sun'] = retrieve_raw_input('# of War Suns:')
    fleet['Capital Ship'] = retrieve_raw_input('# of Flagships:')
    fleet['Ground Force'] = retrieve_raw_input('# of GFs:')
    fleet['Mechanized Unit'] = retrieve_raw_input('# of Mechanized Units:')
    fleet['Shock Troop'] = retrieve_raw_input('# of Shock Troops:')

    json_exporter( fleet, file_name )

def init_fleet():
    """
    Initialize a default empty fleet.
    """
    
    fleet = {
    "name" : "DEFAULT FLEET NAME",
    "Initial Strikes" : [],
    "Extra Hits" : [],
    "loss priority" : [ "Fighter","Destroyer","Carrier","Cruiser","Dreadnought","War Sun","Capital Ship", "Shock Troop", "Ground Force", "Mechanized Unit" ],
    "extra hits" : "None",
    "hit priority" : "sustain",
    "Carrier" : 0,
    "Fighter" : 0,
    "Destroyer" : 0,
    "Cruiser" : 0,
    "Dreadnought" : 0,
    "War Sun" : 0,
    "Capital Ship" : 0,
    "Ground Force" : 0,
    "Mechanized Unit" : 0,
    "Shock Troop" : 0,
  
    "Catalog":
    {
        "Carrier" :
    {   "model" : "Carrier",
        "to hit" : 9,
        "hits" : 1 }, 
    
      "Fighter" :
    {   "model" : "Fighter",
        "to hit" : 9,
        "hits" : 1 },
    
      "Destroyer" :
    {   "model" : "Destroyer",
        "to hit" : 9,
        "hits" : 1 },
    
      "Cruiser" :
    {   "model" : "Cruiser",
        "to hit" : 7,
        "hits" : 1 },
    
      "Dreadnought" :
    {   "model" : "Dreadnought",
        "to hit" : 5,
        "hits" : 1 },
    
      "War Sun" :
    {   "model" : "War Sun",
        "to hit" : 3,
        "hits" : 3 },
    
      "Capital Ship" :
    {   "model" : "Capital Ship",
        "to hit" : 5,
        "hits" : 2 },
    
      "Ground Force" :
    {   "model" : "Ground Force",
        "to hit" : 9,
        "hits" : 1 },

      "Mechanized Unit" :
    {   "model" : "Mechanized Unit",
        "to hit" : 6,
        "hits" : 2 },

      "Shock Troop" :
    {   "model" : "Shock Troop",
        "to hit" : 5,
        "hits" : 1 } } 
    }
    
    return fleet



get_user_input( init_fleet() )

