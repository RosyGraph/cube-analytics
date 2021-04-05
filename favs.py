import os
from mtgsdk import Card

paths = os.listdir("draftlogs")

path = paths[0]
draftlog_path = os.path.join("draftlogs", path)
drafters = ["Jorbas", "RosyGraph", "Waluigi"]


def process_draft(drafter):
    colors = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0, "X": 0}
    total_cmc = 0
    total_cards = 0
    for path in [p for p in os.listdir("draftlogs") if drafter in p]:
        with open(os.path.join("draftlogs", path), "r") as f:
            for line in f.readlines():
                if line.startswith("--> "):
                    cardname = line[4:-1]
                    if cardname == drafter:
                        continue
                    matches = Card.where(name=cardname).all()
                    if len(matches) == 0:
                        print(f"card not found: {cardname}")
                        continue
                    card = matches[0]
                    if card.color_identity:
                        for cid in card.color_identity:
                            colors[cid] += 1
                    else:
                        colors["X"] += 1
                    total_cmc += card.cmc
                    total_cards += 1
    avg_cmc = total_cmc / total_cards
    print(f"drafter: {drafter}")
    print(f"\taverage cmc: {avg_cmc}")
    print(f"\tcolor preferences:")
    for k, v in colors.items():
        p = round(v / total_cards, 2)
        print(f"\t\t{k}: {p}")


for drafter in drafters:
    process_draft(drafter)
