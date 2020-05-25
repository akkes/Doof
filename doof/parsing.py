import os
import cProfile
from pathlib import Path

from doof import model
from doof import helpers


def tree_parse(path: Path, site_config: model.SiteConfig):
    # print(path)
    if os.path.isfile(path):
        if path.suffix == ".toml":
            return model.Page.from_toml(path, site_config)
        elif path.suffix == ".md":
            return model.Page.from_md(path, site_config)
        else:
            return model.Ressource.from_path(path, site_config)
    else:
        index = None
        children = []
        # parse children
        for file in path.iterdir():
            child = tree_parse(path / file, site_config)
            if file.name == "index.toml" or file.name == "index.md":
                index = child
            else:
                children += [child]
        # up the index
        index.children = children
        for child in index.children:
            child.parent = index
        return index


def parse(site_config: model.SiteConfig):
    # walk_parse(path + "/content")

    content_tree = tree_parse(site_config.content_path, site_config)
    helpers.display_aft(content_tree)
    return content_tree
    # cProfile.runctx("[walk_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
    # cProfile.runctx("[tree_parse('{path}') for _ in range(100000)]".format(path=path), globals(), locals())
