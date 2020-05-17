import sys
from doof import parsing
from doof import rendering


def make(site_path: str):
    aft = parsing.parse(site_path)
    rendering.render(aft, site_path)


def run():
    # action
    print(sys.argv)
    if len(sys.argv) >= 2 and sys.argv[1] == "make":
        print("make website")
        if len(sys.argv) > 2:
            folder_path = sys.argv[2]
        else:
            folder_path = "."
        make(folder_path)
    else:
        print("unknown command")
