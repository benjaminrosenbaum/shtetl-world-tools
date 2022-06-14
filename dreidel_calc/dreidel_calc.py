from itertools import product

DREDIEL = "GHNS"


def outcomes(num_spun):
    return ["".join(tuple) for tuple in product(DREDIEL, repeat=num_spun)]


def yankFrom(string, char):
    return string.replace(char, '', 1)


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
    return {"successes": max(gimels - nuns, 0), "complications": shins}


def has(min_successes, max_shins):
    def measure(outcome):
        s = score(outcome)
        return s["successes"] >= min_successes and s["complications"] <= max_shins
    return measure


simple_success = has(1, 100)
double_success = has(2, 100)
triple_success = has(3, 100)
uncomplicated_success = has(1, 0)


def results(num_dreidels, stat):
    return [optimize(spin, stat) for spin in outcomes(num_dreidels)]


def avg_over_possibles(possibles, func):
    return sum(func(outcome) for outcome in possibles) / float(len(possibles))


def chance_of(num_dreidels, stat, condition):
    return avg_over_possibles(results(num_dreidels, stat), condition)


def avg_complications_for_success(num_dreidels, stat):
    return avg_over_possibles(
        [result for result in results(num_dreidels, stat) if score(result)["successes"] > 0],
        lambda outcome: score(outcome)["complications"])


def report_chance(num_dreidels, condition_name, condition):
    chances = [chance_of(num_dreidels, stat, condition) for stat in [0, 1, 2]]
    return "chance of {0}:\t\t".format(condition_name) + "\t\t".join(["{0:.1f}%".format(100 * chance) for chance in chances])


def report_avg_complications(num_dreidels):
    avgs = [avg_complications_for_success(num_dreidels, stat) for stat in [0, 1, 2]]
    return "average complications for success:\t" + "\t\t".join(["{0:.0f}".format(avg) for avg in avgs])


def main():
    for d in [n + 1 for n in range(12)]:
        print ("\nfor {0} dreidels:\t\t\t\tSTAT=0\t\tSTAT=1\t\tSTAT=2".format(d))
        for c in [("simple_success", simple_success), ("success w/o compl", uncomplicated_success),
                  ("double_success", double_success), ("triple_success", triple_success)]:
            print(report_chance(d, c[0], c[1]))
        print(report_avg_complications(d))
        print("")


if __name__ == '__main__':
    main()
