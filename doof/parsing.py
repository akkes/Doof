import os
import cProfile

import doof.model as model


def tree_parse(path, indent: int = 0):
    print("----" * indent)
    # print(path)
    if os.path.isfile(path):
        if path.endswith((".toml",)):
            return model.Page.from_toml(path)
        else:
            return model.Ressource.from_path(path)
    else:
        folder = model.Folder.from_path(path)
        for file in os.listdir(path):
            child = tree_parse(path + "/" + file, indent=indent + 1)
            if child is not None:
                folder.add_child(child)
        return folder


def parse(path: str):
    # walk_parse(path + "/content")
    content_tree = tree_parse(path + "/content")
    print(content_tree)
    # cProfile.runctx("[walk_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
    # cProfile.runctx("[tree_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())

