import sys
import doof.parsing as parsing


def run():
    # action
    print(sys.argv)
    if len(sys.argv) >= 2 and sys.argv[1] == "make":
        print("make website")
        if len(sys.argv) > 2:
            folder_path = sys.argv[2]
        else:
            folder_path = "."
        parsing.parse(folder_path)
    else:
        print("unknown command")
