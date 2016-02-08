from itertools import product

DREDIEL = "GHNS"


def outcomes(num_spun):
    return ["".join(tuple) for tuple in product(DREDIEL, repeat=num_spun)]


def yankFrom(string, char):
    return string.replace(char, '')


def optimize(outcome, stat):
    if (stat == 0):
        return outcome
    else:
        basis = optimize(outcome, stat - 1)
        return yankFrom(basis, 'N') if 'N' in basis else yankFrom(basis, 'S') if 'S' in basis else basis


def score(outcome):
    gimels = outcome.count('G')
    nuns = outcome.count('N')
    shins = outcome.count('S')
    return { "successes": max(gimels - nuns, 0), "complications": shins }


def has(min_successes, max_shins):
    def measure(outcome):
        s = score(outcome)
        return s["successes"] >= min_successes and s["complications"] <= max_shins
    return measure


simple_success = has(1, 100)
double_success = has(2, 100)
triple_success = has(3, 100)
uncomplicated_success = has(1, 0)


def chance_of(num_dreidels, stat, condition):
    spins = outcomes(num_dreidels)
    return num_which([optimize(spin, stat) for spin in spins], condition) / float(len(spins))


def report_chance(num_dreidels, condition_name, condition):
    chances = [chance_of(num_dreidels, stat, condition) for stat in [0, 1, 2]]
    return "chance of {0}:\t\t".format(condition_name) + "\t\t".join(["{0:.1f}%".format(100 * chance) for chance in chances])


def main():
    for d in [1, 2, 3, 4, 5, 6, 7, 8]:
        print ("\nfor {0} dreidels:\t\t\t\tSTAT=0\t\tSTAT=1\t\tSTAT=2".format(d))
        for c in [("simple_success", simple_success), ("success w/o compl", uncomplicated_success),
                  ("double_success", double_success), ("triple_success", triple_success)]:
            print(report_chance(d, c[0], c[1]))
        print("")


if __name__ == '__main__':
    main()
