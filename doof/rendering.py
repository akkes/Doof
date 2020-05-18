import commonmark
from jinja2 import Template
from shutil import rmtree

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
            template = Template("Content: {{content}}")
            output = template.render(node.__dict__)
            file.writelines(output)
    elif isinstance(node, model.Ressource):
        node.file_destination.touch()


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
