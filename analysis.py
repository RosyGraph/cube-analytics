import os


def print_quartiles(cards):
    picked_card_weights = []
    unpicked_cards = []
    for cardname, card_info in cards.items():
        seen = card_info[1]
        weight = card_info[0]
        if seen:
            if weight == 0:
                unpicked_cards.append(cardname)
            else:
                picked_card_weights.append(card_info[0])
    median = sum(picked_card_weights) / len(picked_card_weights)
    lower_half = [weight for weight in picked_card_weights if weight < median]
    upper_half = [weight for weight in picked_card_weights if weight >= median]
    lower_median = sum(lower_half) / len(lower_half)
    upper_median = sum(upper_half) / len(upper_half)
    fourths = []
    fourths.append(
        sorted(
            [
                cardname
                for cardname, info in cards.items()
                if info[0] >= upper_median
            ],
            key=lambda item: item[0],
        )
    )
    fourths.append(
        sorted(
            [
                cardname
                for cardname, info in cards.items()
                if median < info[0] < upper_median
            ],
            key=lambda item: item[0],
        )
    )
    fourths.append(
        sorted(
            [
                cardname
                for cardname, info in cards.items()
                if lower_median < info[0] <= median
            ],
            key=lambda item: item[0],
        )
    )
    fourths.append(
        sorted(
            [
                cardname
                for cardname, info in cards.items()
                if info[1] and info[0] < lower_median
            ],
            key=lambda item: item[0],
        )
    )
    print_ranks(cards, fourths)
    print("unpicked cards:")
    for unpicked_card in unpicked_cards:
        print(f"{unpicked_card}")


def print_ranks(cards, fourths):
    rank = 1
    worst_weight = 1
    for i, cardnames in enumerate(fourths):
        tier = i + 1
        print(f"tier {tier} cards:")
        sorted_fourth = sorted(cardnames, key=lambda item: -cards[item][0])
        for cardname in sorted_fourth:
            if cards[cardname][0] < worst_weight:
                rank += 1
                worst_weight = cards[cardname][0]
            print("{:<5}{:<65}".format(str(rank), cardname))
        print()
