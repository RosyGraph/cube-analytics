import sys
import os
import csv
import re

SPLIT_CARD_REGEX = re.compile(r"^([^/]+)\s//.*$")
BOOSTER_SIZE = 15
DOUBLE_SIDED_CARDNAMES = [
    "Brazen Borrower // Petty Theft",
    "Valakut Awakening // Valakut Stoneforge",
    "Archangel Avacyn // Avacyn, the Purifier",
    "Embereth Shieldbreaker // Battle Display",
    "Jace, Vryn's Prodigy // Jace, Telepath Unbound",
    "Kytheon, Hero of Akros // Gideon, Battle-Forged",
    "Murderous Rider // Swift End",
    "Giant Killer // Chop Down",
    "Bonecrusher Giant // Stomp",
    "Garruk Relentless // Garruk, the Veil-Cursed",
    "Duskwatch Recruiter // Krallenhorde Howler",
]


def get_valid_draftlogs(drafters):
    filenames = os.listdir("./draftlogs")
    log_filenames = []
    for filename in filenames:
        if any([drafter in filename for drafter in drafters]):
            log_filenames.append(filename)
    return log_filenames


def parse_picked(line):
    return line[4:-1]


def print_picks(picks):
    for drafter, cards in picks.items():
        print(drafter)
        for card in cards:
            print("\t" + card)
        print()


def get_cube_list(filename):
    with open(filename) as f:
        cards_csv = csv.reader(f)
        return {cards[0]: [0, False] for cards in cards_csv}


def process_picked_card(line, pick_number, drafter_picks, drafter, cube_list):
    cardname = line[4:].strip()
    matches = SPLIT_CARD_REGEX.match(cardname)
    if matches:
        if cardname in DOUBLE_SIDED_CARDNAMES:
            cardname = matches.group(1)
    drafter_picks[drafter].append(cardname)
    booster_remaining = BOOSTER_SIZE - pick_number
    weight = booster_remaining / BOOSTER_SIZE
    if all(cube_list[cardname]):
        weight = (cube_list[cardname][0] + weight) / 2
    card = cube_list[cardname]
    card[0] = weight
    card[1] = True


def process_draftlog(path, drafter_picks, cube_list):
    pick_indicator = "--> "
    pick_number = 0
    found_player = False
    with open(path) as f:
        for line in f.readlines():
            if line.startswith(pick_indicator):
                if not found_player:
                    drafter = parse_picked(line)
                    found_player = True
                else:
                    process_picked_card(
                        line, pick_number, drafter_picks, drafter, cube_list
                    )
                    pick_number = (pick_number + 1) % BOOSTER_SIZE
            else:
                line = line.strip()
                matches = SPLIT_CARD_REGEX.match(line)
                if matches:
                    if line in DOUBLE_SIDED_CARDNAMES:
                        line = matches.group(1)
                if cube_list.get(line):
                    cube_list[line][1] = True


def print_pick_weights(cube_list):
    sorted_cards = dict(
        sorted(cube_list.items(), key=lambda x: x[1][0], reverse=True)
    )
    for card, info in sorted_cards.items():
        pick_weight = round(info[0] * 100)
        seen = info[1]
        if seen:
            print("{:.<45}{:.>44}".format(card, pick_weight))


def print_quartiles(cards):
    picked_card_weights = []
    for card_info in cards.values():
        if card_info[1]:
            picked_card_weights.append(card_info[0])
    median = sum(picked_card_weights) / len(picked_card_weights)
    lower_half = [weight for weight in picked_card_weights if weight < median]
    upper_half = [weight for weight in picked_card_weights if weight >= median]
    lower_median = sum(lower_half) / len(lower_half)
    upper_median = sum(upper_half) / len(upper_half)
    fourths = []
    fourths.append(
        [
            cardname
            for cardname, info in cards.items()
            if info[0] >= upper_median
        ]
    )
    fourths.append(
        [
            cardname
            for cardname, info in cards.items()
            if median < info[0] < upper_median
        ]
    )
    fourths.append(
        [
            cardname
            for cardname, info in cards.items()
            if lower_median < info[0] <= median
        ]
    )
    fourths.append(
        [
            cardname
            for cardname, info in cards.items()
            if info[1] and info[0] < lower_median
        ]
    )
    for i, cardnames in enumerate(fourths):
        tier = i + 1
        print(f"tier {tier} cards:")
        for cardname in sorted(cardnames):
            print(f"\t{cardname}")
        print()


def main():
    drafters = ["RosyGraph", "Jorbas", "Waluigi"]
    drafter_picks = {drafter: [] for drafter in drafters}
    cube_list = get_cube_list("./cube_lists/cube-list_2021-01-17.csv")
    valid_draftlogs = get_valid_draftlogs(drafters)
    for draftlog_filename in valid_draftlogs:
        print(f"processing draftlog: {draftlog_filename}" + "...")
        qualified_draftlog_path = os.path.join("draftlogs", draftlog_filename)
        process_draftlog(qualified_draftlog_path, drafter_picks, cube_list)
    draftlogs_processed = len(valid_draftlogs)
    print(f"processed {draftlogs_processed} draftlogs.\n")
    #  print_picks(drafter_picks)
    #  print_pick_weights(cube_list)
    print_quartiles(cube_list)


if __name__ == "__main__":
    main()
