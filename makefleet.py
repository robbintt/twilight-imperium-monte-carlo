"""

Take standard input and generate a properly formatted fleet.

"""




def get_user_input( fleet ):
    """
    Get user input into a dict and pass it along.
    """


    fleet['name'] = raw_input('Name:')

    fleet['Carrier'] = raw_input('# of Carriers:')
    fleet['Fighter'] = raw_input('# of Fighters:')
    fleet['Destroyer'] = raw_input('# of Destroyers:')
    fleet['Cruiser'] = raw_input('# of Cruisers')
    fleet['Dreadnought'] = raw_input('# of Dreadnoughts')
    fleet['War Sun'] = raw_input('# of War Suns')
    fleet['Capital Ship'] = raw_input('# of Flagships')
    fleet['Ground Force'] = raw_input('# of GFs')
    fleet['Mechanized Unit'] = raw_input('# of Mechanized Units')
    fleet['Shock Troop'] = raw_input('# of Shock Troops')

    print fleet


def init_fleet():
    """
    Initialize a default empty fleet.
    """
    
    catalog = {
    "name" : "DEFAULT FLEET NAME",
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
        "hits" : 1 }

    } }
    
    return fleet


get_user_input( init_fleet() )

