'''wrapping get/setattr to access to inner class method.'''

import re

# path無しはgetのみ
def getattr_h(instance, attribute_path: str):
    '''wrap getattr'''
    # trail empty path
    if attribute_path == "":
        return instance
    # split
    attribute = attribute_path.split(".")
    for i in attribute:
        # handle head/end/doubled dot.
        if i != "":
            if re.fullmatch(R"[a-zA-Z_]+", i) is not None:
                instance = getattr(instance, i)
            if re.fullmatch(R"[a-zA-Z_]+\[[0-9]+\]", i) is not None:
                instance = getattr(instance, re.split(R"[\[\]]", i)[0])
                instance = instance[int(re.split(R"[\[\]]", i)[1])]
    return instance


def setattr_h(instance, attribute_path: str, value):
    '''wrap setattr'''
    attribute = attribute_path.split(".")
    for i in range(len(attribute) - 1):
        # handle head/end/doubled dot
        if i != "":
            if re.fullmatch(R"[a-zA-Z_]+", i) is not None:
                instance = getattr(instance, i)
            if re.fullmatch(R"[a-zA-Z_]+\[[0-9]+\]", i) is not None:
                instance = getattr(instance, re.split(R"[\[\]]", i)[0])
                instance = instance[int(re.split(R"[\[\]]", i)[1])]
    setattr(instance, attribute[-1], value)
