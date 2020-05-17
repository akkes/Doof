from pathlib import Path

import toml

from doof.logging import logger


class SiteConfig(object):
    def __init__(self, path):
        self.path = Path(path)

    @property
    def content_path(self):
        return self.path / "content"

    @property
    def output_path(self):
        return self.path / "output"


class ContentNode(object):
    def __init__(self, path: str, site_config: SiteConfig):
        logger.info("creating {slug} Page node".format(slug=path.name))
        self.site_config = site_config
        self.children = []
        self.source_path = path
        self.parent = None

    @property
    def leaf(self):
        return not self.children

    @property
    def dir(self):
        return bool(self.children)

    @property
    def slug(self):
        if self.source_path.name == "index.md" or self.source_path.name == "index.toml":
            return self.source_path.parent.name
        else:
            return self.source_path.name

    @property
    def site_destination(self):
        if self.dir:
            return self.site_path.parent
        else:
            return self.site_path.parent / self.site_path.stem

    @property
    def file_destination(self):
        return self.site_config.output_path / self.site_destination / Path("index.html")

    @property
    def site_path(self):
        return self.source_path.relative_to(self.site_config.content_path)

    def add_site(self, site_config: SiteConfig):
        self.site_config = site_config

    def add_child(self, child):
        logger.info(
            "adding {child_name} to {self_name}".format(
                child_name=child.name, self_name=self.slug
            )
        )
        self.children += [child]

    def remove_child(self, child):
        logger.info(
            "removing {child_name} to {self_name}".format(
                child_name=child.name, self_name=self.slug
            )
        )
        self.children.remove(child)


class Page(ContentNode):
    @classmethod
    def from_toml(cls, path: str, site_config: SiteConfig):
        pairs = toml.load(path)
        return cls(path, pairs, site_config)

    @classmethod
    def from_md(cls, path: str, site_config: SiteConfig):
        with open(path) as file:
            content = file.readlines()
        return cls(path, {"content": content}, site_config)

    def __init__(self, path: str, pairs: dict, site_config: SiteConfig):
        super().__init__(path, site_config)
        self.pairs = pairs


class Ressource(ContentNode):
    @classmethod
    def from_path(cls, path: str, site_config: SiteConfig):
        return cls(path, site_config)

    def __init__(self, path: str, site_config: SiteConfig):
        super().__init__(path, site_config)
        self.raw = None


class Folder(ContentNode):
    @classmethod
    def from_path(cls, path: str, site_config: SiteConfig):
        return cls(path, site_config)

    def __init__(self, path: str, site_config: SiteConfig):
        super().__init__(path, site_config)


class Site(object):
    def __init__(self, path):
        self.path = path

    @property
    def content_path(self):
        return self.path + "content/"

    @property
    def output_path(self):
        return self.path + "output/"
