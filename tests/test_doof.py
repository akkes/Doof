from pathlib import Path
from tempfile import TemporaryDirectory
import typing as T
import random

import toml
from doof import __version__, parsing
import doof.model as m

POSSIBLE_NAMES = [
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "iota",
    "sigma",
    "zeta",
    "eta",
    "theta",
    "kappa",
    "lambda",
    "mu",
    "nu",
    "omicron",
    "pi",
    "rho",
    "tau",
    "upsilon",
    "phi",
    "chi",
    "psi",
    "omega",
]


def count_iter(iter: T.Iterable) -> int:
    return sum(1 for _ in iter)


def test_version():
    assert __version__ == "0.1.0"


def test_tree_parse():
    with TemporaryDirectory() as dir_str:
        root_path = Path(dir_str)
        # make structure
        (root_path / "content").mkdir()
        (root_path / "output").mkdir()
        (root_path / "assets").mkdir()
        (root_path / "templates").mkdir()

        # make config
        config: dict[str, str] = {"url": "localhost", "name": "test_doof"}
        with (root_path / "config.toml").open("w", encoding="utf-8") as f:
            toml.dump(config, f)

        # make base content
        content: set[Path] = set()
        ## make index
        fs_path = root_path / "content" / "index.md"
        fs_path.touch()
        content.add(fs_path)

        ## make more content
        for _ in range(10):
            # Select a page and subpage name
            base_content: Path = random.choice(tuple(content))
            new_content_name = random.choice(POSSIBLE_NAMES)

            # Skip if subpage already exist
            if (
                base_content.parent / f"{new_content_name}.md" in content
                or base_content.parent / new_content_name / "index.md" in content
            ):
                continue

            # If content is not an index folder, make it an index so we can create a subpage
            if base_content.name != "index.md":
                # Create subfolder
                new_folder = base_content.parent / base_content.stem
                new_folder.mkdir()
                # move content
                content.remove(base_content)
                base_content = base_content.rename(new_folder / "index.md")
                content.add(base_content)  # This is a side effect
                # I'm feeling dirty writing it
                # It begins. The functional programming virus

            # Create the new subpage
            new_content_path = base_content.parent / f"{new_content_name}.md"
            new_content_path.touch()
            content.add(new_content_path)
            assert fs_path in content

        # Test parsing
        site = m.Site(root_path)
        parsing.parse(site)
        assert set(map(lambda page: page.source_path, site.pages)) == content
        prev_set: set[m.Page] = set()
        next_set: set[m.Page] = set()
        for page in site.pages:
            # count subpages
            if page.source_path.name == "index.md":
                n_subpages = (
                    count_iter(page.source_path.parent.iterdir()) - 1
                )  # do not count index
            else:
                n_subpages = 0
            # assert aft match filesystem
            assert len(page.children) == n_subpages
