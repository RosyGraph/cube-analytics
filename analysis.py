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
