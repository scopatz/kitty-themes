#!/usr/bin/env python3
import os
import re
import math
import array


#
# Color tools
#
RE_RGB3 = re.compile(r"(.)(.)(.)")
RE_RGB6 = re.compile(r"(..)(..)(..)")


def rgb_to_ints(rgb):
    if len(rgb) == 6:
        return tuple([int(h, 16) for h in RE_RGB6.split(rgb)[1:4]])
    else:
        return tuple([int(h * 2, 16) for h in RE_RGB3.split(rgb)[1:4]])

def rgb_to_array(rgb):
    return array.array(rgb_to_ints(rgb))


def color_dist(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2)


def color_diff(x, y):
    xvec = rgb_to_array(x)
    yvec = rgb_to_array(y)
    return x - y


MARGIN_BG_TO_COLOR15 = color_dist("fafbfc", "ffffff")

#
# Config tools
#

def parse_config(filename):
    """Parses a config file and returns a theme dict"""
    with open(filename) as f:
        s = f.read()
    return dict(map(str.split, s.splitlines()))


def generate_diff_config(theme):
    config = {
        "foreground": theme["foreground"],
        "background": theme["background"],
        "title_fg": theme["foreground"],
        "title_bg": theme["background"],
        "search_bg": theme["foreground"],
        "search_fg": theme["background"],
        "margin_bg": theme["color15"] +
    }
    return config


def format_config(theme):
    lines = [k + " " + v for k, v in theme.items()]
    lines.sort()
    return "\n".join(lines) + "\n"


def write_config(config, name):
    s = format_config(config)
    filename = f"{name}.diff.conf"
    with open(filename, "w") as f:
        f.write(s)


def main(args):
    theme = parse_config(args[1])
    config = generate_diff_config(theme)
    write_config(config, os.path.splitext(os.path.basename(args[1]))[0])


if __name__ == "__main__":
    import sys
    main(sys.argv)
