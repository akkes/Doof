import sys
import os
from doof import parsing
from doof import rendering
from doof import model


def make(site_path: str):
    site_config = model.SiteConfig(site_path)
    aft = parsing.parse(site_config)
    rendering.render(site_config)


def run():
    # action
    print(sys.argv)
    if len(sys.argv) >= 2 and sys.argv[1] == "make":
        print("make website")
        if len(sys.argv) > 2:
            folder_path = sys.argv[2]
        else:
            folder_path = os.getcwd()
        make(folder_path)
    else:
        print("unknown command")
