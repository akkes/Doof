import commonmark
from jinja2 import Template, Environment, FileSystemLoader
from shutil import rmtree
from pathlib import Path

from doof import model


def tree_render(node: model.ContentNode, site_config: model.SiteConfig):
    if isinstance(node, model.Page):
        if node.dir:
            node.destination_path.parent.mkdir()
            for child in node.children:
                tree_render(child, site_config)
        else:
            node.destination_path.parent.mkdir()
        with open(node.destination_path, "w") as file:
            file_loader = FileSystemLoader(site_config.templates_path)
            env = Environment(loader=file_loader)
            try:
                template = env.get_template(node.template)
            except AttributeError:
                template = env.get_template("default.html")
            try:
                node.pairs["content"] = commonmark.commonmark(node.pairs["content"])
            except KeyError:
                pass
            output = template.render(**node.pairs)
            file.writelines(output)
    elif isinstance(node, model.Ressource):
        node.destination_path.touch()


def render(aft: model.ContentNode, site_config: model.SiteConfig):
    print("render site")
    # try:
    #     site_config.output_path.mkdir()
    # except FileExistsError:
    #     site_config.output_path.mkdir()
    try:
        rmtree(site_config.output_path)
    except FileNotFoundError:
        pass
    tree_render(aft, site_config)
