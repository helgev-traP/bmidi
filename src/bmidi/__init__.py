# 開発環境のみ
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

# help
from help_module import *
