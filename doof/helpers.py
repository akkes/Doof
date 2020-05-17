from doof import model


def display_aft(aft: model.ContentNode, indent=0):
    indentation = "  " * max(0, indent - 1)
    if indent >= 1:
        indentation += "└─ "
    print(indentation + aft.name + ":" + aft.__class__.__name__)
    for child in aft.children:
        display_aft(child, indent=indent + 1)