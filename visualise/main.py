import argparse

import matplotlib
from matplotlib import pyplot as plt
from graphs.timeline import plot_timeline


def parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    parser.add_argument("graph_type", type=str, choices=["radar", "timeline", "box", "map", "bar"], help="Graph Type")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parse_args(parser)

    graph_type = args.graph_type

    fm: matplotlib.font_manager.FontManager = matplotlib.font_manager.fontManager
    fm.addfont("./STIXTwoText.ttf")
    plt.rcParams["font.family"] = "STIX Two Text"

    my_color = {
        "red": "#FC8484",
        "dark_red": "#FA5050",
        "light_blue": "#94C4E0",
        "light_green": "#9CDAA0",
        "dark_blue": "#76ABCB",
        "dark_green": "#51BD56",
        "black": "#505050",
        "purple": "#CBA6DD",
        "yellow": "#FFE959",
        "yellow_green": "#C1FF87",
    }

    if graph_type == "timeline":
        plot_timeline(my_color)
