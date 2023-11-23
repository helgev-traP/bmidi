"""help module"""

import sys

sys.dont_write_bytecode = True
# attr
from attribute_access.attribute_access import *

# object
from object.trailing_object import *

# score
from score.from_score import *
from score.midi_track import *
from score.score import *

# root
from object_score import *
from motion_cut import *

# utl
from inspect import signature


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
    for i in CreateObject.__dict__:
        if type(getattr(CreateObject, i)) == func:
            print("\t", YELLOW + i + END, end="")
            print(
                " ->" + GREEN,
                signature(getattr(CreateObject, i)).return_annotation,
                END,
            )
            for j in signature(getattr(CreateObject, i)).parameters:
                print("\t\t" + CYAN, j, END)
        else:
            print("\t", i)


help()
