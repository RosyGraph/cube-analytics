import sys
import os
import csv
import re
import datetime

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
    "Nissa, Vastwood Seer // Nissa, Sage Animist",
    "Valki, God of Lies // Tibalt, Cosmic Impostor",
    "Legion's Landing // Adanto, the First Fort",
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
                process_unpicked_card(line, cube_list)


def process_unpicked_card(s, cards):
    s = s.strip()
    matches = SPLIT_CARD_REGEX.match(s)
    if matches:
        if s in DOUBLE_SIDED_CARDNAMES:
            s = matches.group(1)
    if cards.get(s):
        cards[s][1] = True


def print_pick_weights(cube_list):
    sorted_cards = dict(
        sorted(cube_list.items(), key=lambda x: x[1][0], reverse=True)
    )
    for card, info in sorted_cards.items():
        pick_weight = round(info[0] * 100)
        seen = info[1]
        if seen:
            print("{:.<45}{:.>44}".format(card, pick_weight))


def combine_cube_lists(path_to_cubelists):
    cube_list_filenames = os.listdir(path_to_cubelists)
    cube_lists = [
        get_cube_list(os.path.join("cube_lists", filename))
        for filename in cube_list_filenames
    ]
    cube_list = cube_lists[0]
    for c in cube_lists[1:]:
        cube_list.update(c)
    return cube_list


def write_cube_list(cube_list):
    current_date = str(datetime.datetime.now()).split()[0]
    new_cube_list_filename = "cube-list_comprehensive_" + current_date + ".csv"
    qualified_cubelist_path = os.path.join("cube_lists", new_cube_list_filename)
    with open(qualified_cubelist_path, "w") as f:
        csv_writer = csv.writer(f)
        for k, v in cube_list.items():
            csv_writer.writerow([k, v])


def generate_cube_list_from_drafter_picks(drafters):
    drafter_picks = {drafter: [] for drafter in drafters}
    cube_list = combine_cube_lists("./cube_lists")
    valid_draftlogs = get_valid_draftlogs(drafters)
    for draftlog_filename in valid_draftlogs:
        print(f"processing draftlog: {draftlog_filename}" + "...")
        qualified_draftlog_path = os.path.join("draftlogs", draftlog_filename)
        process_draftlog(qualified_draftlog_path, drafter_picks, cube_list)
    draftlogs_processed = len(valid_draftlogs)
    print(f"processed {draftlogs_processed} draftlogs.\n")
    return cube_list
