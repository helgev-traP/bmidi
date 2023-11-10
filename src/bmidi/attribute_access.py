"""wrapping get/setattr to access to inner class method."""

import re


def getattr_h(instance, attribute_path: str):
    """wrap getattr"""
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
            elif re.fullmatch(R"[a-zA-Z_]+\[[0-9]+\]", i) is not None:
                instance = getattr(instance, re.split(R"[\[\]]", i)[0])
                instance = instance[int(re.split(R"[\[\]]", i)[1])]
            elif re.fullmatch(R"[a-zA-Z_]+\[[\'\"][a-zA-z_][\'\"]\]", i) is not None:
                instance = getattr(instance, re.split(R"[\[\]]", i)[0])
                instance_key = re.split(R"[\[\]]", i)[1]
                instance_key = re.sub(R"[\'\"]", "", instance_key)
                instance = instance[instance_key]
            else:
                print("invalid path at function: getattr_h")
    return instance


def setattr_h(instance, attribute_path: str, value):
    """wrap setattr"""
    attribute = attribute_path.split(".")
    for i in range(len(attribute) - 1):
        # handle head/end/doubled dot
        if attribute[i] != "":
            if re.fullmatch(R"[a-zA-Z_]+", attribute[i]) is not None:
                instance = getattr(instance, attribute[i])
            elif re.fullmatch(R"[a-zA-Z_]+\[[0-9]+\]", attribute[i]) is not None:
                instance = getattr(instance, re.split(R"[\[\]]", attribute[i])[0])
                instance = instance[int(re.split(R"[\[\]]", attribute[i])[1])]
            elif (
                re.fullmatch(R"[a-zA-Z_]+\[[\'\"][a-zA-z_][\'\"]\]", attribute[i])
                is not None
            ):
                instance = getattr(instance, re.split(R"[\[\]]", attribute[i])[0])
                instance_key = re.split(R"[\[\]]", attribute[i])[1]
                instance_key = re.sub(R"[\'\"]", "", instance_key)
                instance = instance[instance_key]
            else:
                print("invalid path at function: setattr_h")
    setattr(instance, attribute[-1], value)
