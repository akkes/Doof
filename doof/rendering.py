import commonmark
from jinja2 import Template, Environment, FileSystemLoader
from shutil import rmtree, copyfile, copytree
from pathlib import Path

from doof import model


def tree_render(node: model.ContentNode, site: model.Site):
    if isinstance(node, model.Page):
        if node.dir:
            node.destination_path.parent.mkdir()
            for child in node.children:
                tree_render(child, site)
        else:
            node.destination_path.parent.mkdir()
        with open(node.destination_path, "w") as file:
            file_loader = FileSystemLoader(site.templates_path)
            env = Environment(loader=file_loader)
            try:
                template = env.get_template(node.template)
            except AttributeError:
                template = env.get_template("default.html")
            try:
                node.content = commonmark.commonmark(node.content)
            except AttributeError:
                pass
            output = template.render(page=node, site=site)
            file.writelines(output)
    elif isinstance(node, model.Folder):
        node.destination_path.mkdir()
        for child in node.children:
            tree_render(child, site)
    for item in node.ressources:
        copyfile(item.source_path, item.destination_path)


def render(site: model.Site):
    print("render site")
    # try:
    #     site_config.output_path.mkdir()
    # except FileExistsError:
    #     site_config.output_path.mkdir()
    try:
        rmtree(site.output_path)
    except FileNotFoundError:
        pass
    tree_render(site.root, site)
    copytree(site.assets_path, site.output_path / "assets")
