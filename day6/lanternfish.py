import collections
import getopt
from collections import deque
import time
import sys

# Instead of modelling each individual fish, create a buckets for how many fish
# have x amount of days left before spawning. E.g. [1, 0, 4] means 1 fish will
# spawn next day, and 4 have 2 days left. Each cycle then just means rotating
# the list, then adding the number of fish that spawned to day 7 to reset them
# e.g. [1,0,2,0,0,0,0,0,0] -> [0,2,0,0,0,0,0,0,1] -> [0,2,0,0,0,0,1,0,1]
# e.g. [5,2,2,4,3,0,1,3,6] -> [2,2,4,3,0,1,3,6,5] -> [2,2,4,3,0,1,8,6,5]

# Get number of days to run for and the inputs
def get_options(argv):
    help_text = "lanternfish.py -d <days> -i <inputfile>"
    days = -1
    input_file = ""
    try:
        opts, args = getopt.getopt(argv, "hd:i:", ["days=", "inputfile"])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_text)
            sys.exit()
        elif opt in ("-d", "--days"):
            try:
                days = int(arg)
            except:
                print(help_text)
                sys.exit(2)
        elif opt in ("-i", "--inputfile"):
            input_file = arg
    if days == -1:
        print(help_text, file=sys.stderr)
        sys.exit(2)
    if input_file == "":
        input_file = "input.txt"

    inputs = []
    try:
        with open(input_file) as f:
            contents = f.read().split(",")
            inputs = list(map(int, contents))
    except IOError:
        print(f"Couldn't open file: {input_file}", file=sys.stderr)
        sys.exit(2)
    if len(inputs) == 0:
        print("Empty input")
        sys.exit(2)

    return days, inputs


def rotate(fish: collections.deque):
    fish.rotate(-1)
    fish[6] = fish[6] + fish[-1]
    return fish


def main(argv):
    days, input_fish = get_options(argv)

    start = time.time()

    # Create starting counts
    all_fish = deque([0, 0, 0, 0, 0, 0, 0, 0, 0])
    for x in input_fish:
        all_fish[x] = all_fish[x] + 1

    # Run for the amount of days
    print(f'Start: \t{all_fish}\n')
    for i in range(days):
        all_fish = rotate(all_fish)
        print(f'Day {i+1}: \t{all_fish}')

    # Count number of fish
    fish_count = 0
    for i in range(len(all_fish)):
        fish_count += all_fish.pop()
    print(f'Final Count: {fish_count}')

    end = time.time()
    print(f'\nTook {end - start}s')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
