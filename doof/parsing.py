import os
import cProfile

from doof import model
from doof import helpers


def tree_parse(path):
    # print(path)
    if os.path.isfile(path):
        if path.endswith((".toml",)):
            return model.Page.from_toml(path)
        elif path.endswith((".md",)):
            return model.Page.from_md(path)
        else:
            return model.Ressource.from_path(path)
    else:
        index = None
        children = []
        # parse children
        for file in os.listdir(path):
            child = tree_parse(path + "/" + file)
            if file == "index.toml" or file == "index.md":
                index = child
                child.name = path.split("/")[-1]
            else:
                children += [child]
        # up the index
        index.children = children
        return index


def parse(path: str):
    # walk_parse(path + "/content")
    content_tree = tree_parse(path + "/content")
    helpers.display_aft(content_tree)
    return content_tree
    # cProfile.runctx("[walk_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
    # cProfile.runctx("[tree_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
