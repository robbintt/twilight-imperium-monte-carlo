
===========================
HOW TO RUN THE APPLICATION:
===========================
$ python twilight.py fleets/example-fleet-1 fleets/example-fleet-2

(you can leave the .json extension in and use tab completion if you wish)

This will run the application on the example fleets, which you can modify as you wish or use as templates and rename.

=============
INSTRUCTIONS:
=============
1. You must save your fleet as a json file following the format of example-fleet-1.json and example-fleet-2.json
2. Include your fleet filenames as the first and second arguments. You may omit the .json extension in the command line arguments.
3. The output will clearly identify what percentage of the time each fleet file was destroyed by the other.

=============================
UNDERSTANDING THE FLEET FILE:
=============================
1. The name can be whatever you want.
2. The filename should be something easy to remember.
3. The "loss priority" recommends what should get hit first. Leftmost dies first. Any unit not on this list will be randomly killed after the whole "loss priority" list has been exhausted.
4. Generally set "hit priotity" to "sustain". sustain/protect signifies whether multi-hit ships sustain before the hit prioritization list comes into effect. More information is below in Additional notes.

====================
ADDING CUSTOM UNITS:
====================
1. Add the unit to the 'Catalog' following the format of the other units.
2. Add the unit in the unit list area at the top, and a quantity for that fleet or 0.
3. Optionally put the unit in the "loss priority".


=================
ADDITIONAL NOTES:
=================

Each fleet has one of two modes: protect or sustain

Sustain mode means that any sustained damage will be taken before fleets begin taking losses. This should be your default mode.

Protect mode means that sustained hits will only be used after all ships that do not sustain damage are destroyed. This is useful when your opponent has a action card to immediately destroy a ship that you have sustained damage on.  This feature might not be perfect, as you might want to sustain hits on war suns and capital ships but not dreadnoughts, depending on the language of the card.
