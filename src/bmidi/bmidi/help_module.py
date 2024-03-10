"""help module"""

import sys
# utl
from inspect import signature

sys.dont_write_bytecode = True
# attr
from .attribute_access import *

# object
from .object.trailing_object import *

# score
from .score.midi_track import *
from .score.score import *

# root
from .object_score import *
from .motion_cut import *



def help():
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    END = "\033[0m"
    func = type(help)
    # obj score
    print("Object_Score")
    print("\t", "Nothing")

    # motion cut
    print("Motion_Cut")
    print("\t", "Nothing")

    # score
    print("Score")
    for i in Score.__dict__:
        print("\t", i)

    # simple obj
    print("SimpleObject")
    for i in SimpleObject.__dict__:
        print("\t", i)

    # create object
    print("CreateObject")
    for i in Object.__dict__:
        if type(getattr(Object, i)) == func:
            print("\t", YELLOW + i + END, end="")
            print(
                " ->" + GREEN,
                signature(getattr(Object, i)).return_annotation,
                END,
            )
            for j in signature(getattr(Object, i)).parameters:
                print("\t\t" + CYAN, j, END)
        else:
            print("\t", i)

if __name__ == "__main__":
    help()
