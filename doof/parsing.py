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
        folder = model.Folder.from_path(path)
        for file in os.listdir(path):
            child = tree_parse(path + "/" + file)
            if child is not None:
                folder.add_child(child)
        return folder


def has_index(node: model.ContentNode):
    for child in node.children:
        if child.name == "index.toml":
            return True
        elif child.name == "index.md":
            return True
    return False


def collapse(aft: model.ContentNode):
    if has_index(aft):
        pass
    else:
        pass


def parse(path: str):
    # walk_parse(path + "/content")
    content_tree = tree_parse(path + "/content")
    helpers.display_aft(content_tree)
    return content_tree
    # cProfile.runctx("[walk_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
    # cProfile.runctx("[tree_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
