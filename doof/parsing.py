import os
import cProfile
from pathlib import Path

from doof import model
from doof import helpers


def tree_parse(path: Path, site: model.Site) -> model.ContentNode:
    # print(path)
    if os.path.isfile(path):
        if path.suffix == ".toml":
            return model.Page.from_toml(path, site)
        elif path.suffix == ".md":
            return model.Page.from_md(path, site)
        else:
            return model.Ressource.from_path(path, site)
    else:
        index = model.Folder(path, site)
        children = []
        ressources = []
        # parse children
        for file in path.iterdir():
            child = tree_parse(path / file, site)
            if file.name == "index.toml" or file.name == "index.md":
                index = child
            elif isinstance(child, model.Page) or isinstance(child, model.Folder):
                children += [child]
                site.pages += [child]
            else:
                ressources += [child]
                site.ressources += [child]
        # sort items
        children = sorted(children, key=lambda x: x.date)
        # up the index
        index.children = children
        index.ressources = ressources
        for child in index.children:
            child.parent = index
            child.siblings = children
        return index


def parse(site: model.Site) -> model.ContentNode:
    # walk_parse(path + "/content")

    content_tree = tree_parse(site.content_path, site)
    helpers.display_aft(content_tree)
    site.pages += [content_tree]
    site.root = content_tree
    return content_tree
    # cProfile.runctx("[walk_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
    # cProfile.runctx("[tree_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
