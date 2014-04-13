

prob1 = 7

tot_range = 12. # The period on the end of the number triggers float types.


rate1 = prob1 / tot_range

prob_list = [7, 7, 7]
#prob_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def generate_range( prob_list, tot_range ):


    chances = []
    for each in prob_list:
        if each > tot_range:
            raise "A probability is out of range!"
        success = tot_range - each
        chances.append( success / tot_range )

    return chances


def check_extremes( chances ):

    test_all_unnorm = 1 # initial value will be (1 * each) = each
    test_none_unnorm = 1 # initial value will be (1 * (1 - each)) = (1 - each)
    for each in chances:
        test_all_unnorm *= each
        test_none_unnorm *= (1 - each)
    test_all = test_all_unnorm / len(chances)
    test_none = test_none_unnorm * len(chances)
    test_any = 1 - test_none - test_all # does not include cases > 1 hit
    print test_any *100, "% chance that at least one hits (but not all)."
    print test_all *100, "% chance of all hits."
    print test_none *100, "% chance of no hits."
    print 100* (test_any+test_all+test_none)


def chance_of_two( chances ):
    
    chance_of_two = 0
    for each in chances:
        for item in chances:
            two_exclusive = 

    pass

chances = generate_range( prob_list, tot_range )

check_extremes( chances )
