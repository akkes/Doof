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

    @property
    def templates_path(self):
        return self.path / "templates"


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
    def rel_source_path(self):
        return self.source_path.relative_to(self.site_config.content_path)

    @property
    def rel_url_path(self):
        if self.source_path.name == "index.md" or self.source_path.name == "index.toml":
            return self.rel_source_path.parent
        else:
            return self.rel_source_path.parent / Path(self.source_path.stem)

    @property
    def rel_destination_path(self):
        return self.rel_url_path / Path("index.html")

    @property
    def destination_path(self):
        return self.site_config.output_path / self.rel_destination_path


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
        self.template = None


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
