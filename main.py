import cardparse
import analysis


def main():
    drafters = ["RosyGraph", "Jorbas", "Waluigi"]
    cube_list = cardparse.generate_cube_list_from_drafter_picks(drafters)
    #  print_picks(drafter_picks)
    #  print_pick_weights(cube_list)
    analysis.print_quartiles(cube_list)


if __name__ == "__main__":
    main()
