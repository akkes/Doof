import sys
import os
from doof import parsing
from doof import rendering
from doof import model
from doof import serve


def make(site_path: str):
    site = model.Site(site_path)
    aft = parsing.parse(site)
    rendering.render(site)


def server(site_path: str):
    site = model.Site(site_path)
    aft = parsing.parse(site)
    site.url = "http://localhost:3663"
    rendering.render(site)
    serve.serve(site)


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
    elif len(sys.argv) >= 2 and sys.argv[1] == "serve":
        print("make website")
        if len(sys.argv) > 2:
            folder_path = sys.argv[2]
        else:
            folder_path = os.getcwd()
        server(folder_path)

    else:
        print("unknown command")
