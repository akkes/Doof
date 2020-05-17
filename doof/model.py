from doof.logging import logger

import toml


class ContentNode(object):
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add_child(self, child):
        logger.info(
            "adding {child_name} to {self_name}".format(
                child_name=child.name, self_name=self.name
            )
        )
        self.children += [child]

    def remove_child(self, child):
        logger.info(
            "removing {child_name} to {self_name}".format(
                child_name=child.name, self_name=self.name
            )
        )
        self.children.remove(child)


class Page(ContentNode):
    @classmethod
    def from_toml(cls, path: str):
        pairs = toml.load(path)
        name = path.split("/")[-1]
        return cls(name, pairs)

    @classmethod
    def from_md(cls, path: str):
        name = path.split("/")[-1]
        with open(path) as file:
            content = file.readlines()
        return cls(name, {"content": content})

    def __init__(self, name: str, pairs: dict):
        logger.info("creating {name} Page node".format(name=name))
        super().__init__(name)
        self.pairs = pairs


class Ressource(ContentNode):
    @classmethod
    def from_path(cls, path: str):
        return cls(path.split("/")[-1], None)

    def __init__(self, name: str, raw):
        logger.info("creating {name} Ressource node".format(name=name))
        super().__init__(name)
        self.raw = raw


class Folder(ContentNode):
    @classmethod
    def from_path(cls, path: str):
        return cls(path.split("/")[-1])

    def __init__(self, name: str):
        super().__init__(name)
        logger.info("creating {name} Folder node".format(name=name))
