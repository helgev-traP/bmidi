# 開発環境のみ
import sys

sys.dont_write_bytecode = True
# attr
from bmidi.attribute_access.attribute_access import getattr_h
from bmidi.attribute_access.attribute_access import setattr_h

# object
from bmidi.object.trailing_object import SimpleObjectEndPoint
from bmidi.object.trailing_object import SimpleObject
from bmidi.object.trailing_object import Object

# score
from bmidi.score.midi_track import *
from bmidi.score.score import *

# root
from bmidi.object_score import *
from bmidi.motion_cut import *

# help
from bmidi.help_module import *
