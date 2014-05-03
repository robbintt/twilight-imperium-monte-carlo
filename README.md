

Run example:  $ python twilight.py example-fleet-1 example-fleet-2

Instructions:
1. You must save your fleet in a json file following the format of example-fleet-1.json and example-fleet-2.json
2. Include your fleet filenames as the first and second arguments. You may omit the .json extension in the command line arguments.
3. The output will clearly identify what percentage of the time each fleet file was destroyed by the other.



Additional notes:

Each fleet has one of two modes: protect or sustain

Sustain mode means that any sustained damage will be taken before fleets begin taking losses. This should be your default mode.

Protect mode means that sustained hits will only be used after all ships that do not sustain damage are destroyed. This is useful when your opponent has a action card to immediately destroy a ship that you have sustained damage on.  This feature might not be perfect, as you might want to sustain hits on war suns and capital ships but not dreadnoughts, depending on the language of the card.
