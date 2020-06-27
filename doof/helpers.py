from doof import model


def display_aft(aft: model.ContentNode, indent=0):
    indentation = "│  " * max(0, indent - 1)
    if indent >= 1:
        if aft.next is not None:
            indentation += "├─ "
        else:
            indentation += "└─ "
    rpz = aft.rel_url_path.name + ": " + aft.__class__.__name__
    if aft.hidden:
        rpz = "({})".format(rpz)
    print(indentation + rpz)
    for child in aft.children:
        display_aft(child, indent=indent + 1)


def visible(list):
    for item in list:
        try:
            if item.hidden == True:
                continue
        except AttributeError:
            pass
        yield item
