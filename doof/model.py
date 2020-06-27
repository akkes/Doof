from pathlib import Path
import datetime

import toml

from doof.logging import logger


class Site(object):
    pages = []
    ressources = []

    def __init__(self, path):
        self.path = Path(path)
        try:
            self.__dict__.update(toml.load(Path(path) / "config.toml"))
        except FileNotFoundError:
            pass

    @property
    def nodes(self):
        return self.pages + self.ressources

    @property
    def content_path(self):
        return self.path / "content"

    @property
    def output_path(self):
        return self.path / "output"

    @property
    def assets_path(self):
        return self.path / "assets"

    @property
    def site_path(self):
        return self.output_path

    @property
    def templates_path(self):
        return self.path / "templates"


class ContentNode(object):
    def __init__(self, path: Path, site: Site):
        logger.info("creating {slug} Page node".format(slug=path.name))
        self.site = site
        self.children = []
        self.ressources = []
        self.siblings = [self]
        self.source_path = path
        self.parent = None
        self.name = self.source_path.stem
        self.title = self.name
        self.date = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        self.hidden = False

    @property
    def prev(self):
        i_self = self.siblings.index(self)
        i_prev = i_self - 1
        if i_prev > 0:
            return self.siblings[i_prev]
        return None

    @property
    def prev_visible(self):
        prev_node = self.prev
        while prev_node is not None and prev_node.hidden:
            prev_node = prev_node.prev
        return prev_node

    @property
    def next(self):
        i_self = self.siblings.index(self)
        i_next = i_self + 1
        if i_next < len(self.siblings):
            return self.siblings[i_next]
        return None

    @property
    def next_visible(self):
        next_node = self.next
        while next_node is not None and next_node.hidden:
            next_node = next_node.next
        return next_node

    @property
    def leaf(self):
        return not self.children

    @property
    def dir(self):
        return bool(self.children)

    @property
    def rel_source_path(self):
        return self.source_path.relative_to(self.site.content_path)

    @property
    def rel_url_path(self):
        return self.rel_source_path

    @property
    def url_path(self):
        return self.site.url + "/" + str(self.rel_url_path)

    url = url_path

    @property
    def rel_destination_path(self):
        return self.rel_url_path

    @property
    def destination_path(self):
        return self.site.output_path / self.rel_destination_path

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.title)


class Page(ContentNode):
    @property
    def rel_url_path(self):
        if self.source_path.name == "index.md" or self.source_path.name == "index.toml":
            return self.rel_source_path.parent
        else:
            return self.rel_source_path.parent / Path(self.source_path.stem)

    @property
    def rel_destination_path(self):
        return self.rel_url_path / Path("index.html")

    @classmethod
    def from_toml(cls, path: str, site: Site):
        pairs = toml.load(path)
        return cls(path, pairs, site)

    @classmethod
    def from_md(cls, path: str, site: Site):
        with open(path) as file:
            first_line = file.readline()
            if first_line.startswith("+++"):
                front_matter = ""
                for line in file:
                    if line.startswith("+++"):
                        break
                    front_matter += line
                pairs = toml.loads(front_matter)
                pairs["content"] = file.read()
            else:
                pairs = {"content": first_line}
                pairs["content"] += file.read()
        return cls(path, pairs, site)

    def __init__(self, path: str, pairs: dict, site: Site):
        super().__init__(path, site)
        if path.name == "index.toml" or path.name == "index.md":
            self.name = path.parent.stem
            self.title = self.name
        self.__dict__.update(pairs)
        self.date = datetime.datetime.combine(self.date, datetime.time(0))


class Ressource(ContentNode):
    @classmethod
    def from_path(cls, path: str, site: Site):
        return cls(path, site)

    def __init__(self, path: str, site: Site):
        super().__init__(path, site)


class Folder(ContentNode):
    @classmethod
    def from_path(cls, path: str, site: Site):
        return cls(path, site)

    def __init__(self, path: str, site: Site):
        super().__init__(path, site)
