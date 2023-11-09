'''wrapping get/setattr to access to inner class method.'''

# path無しはgetのみ
def getattr_h(instance, attribute_path: str):
    '''wrap getattr'''
    # trail empty path
    if attribute_path == "":
        return instance
    # split
    attribute = attribute_path.split(".")
    for i in attribute:
        # handle head/end/doubled dot
        if i != "":
            instance = getattr(instance, i)
    return instance


def setattr_h(instance, attribute_path: str, value):
    '''wrap setattr'''
    attribute = attribute_path.split(".")
    for i in range(len(attribute) - 1):
        # handle head/end/doubled dot
        if i != "":
            instance = getattr(instance, attribute[i])
    setattr(instance, attribute[-1], value)
