import sys
import doof.parsing as parsing

def run():
    #action
    if len(sys.argv)>1 and sys.argv[1] == "make":
        print("make website")
        parsing.parse(sys.argv[2])
    else:
        print("unknown command")